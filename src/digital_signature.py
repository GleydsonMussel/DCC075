import argparse
import json
import os
import base64
import sys
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend


def gen_rsa_keypair(keysize=2048):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=keysize, backend=default_backend())
    public_key = private_key.public_key()
    return private_key, public_key


def save_private_key(private_key, path: Path):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    path.write_bytes(pem)


def save_public_key(public_key, path: Path):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    path.write_bytes(pem)


def load_private_key(path: Path):
    data = path.read_bytes()
    return serialization.load_pem_private_key(data, password=None, backend=default_backend())


def load_public_key(path: Path):
    data = path.read_bytes()
    return serialization.load_pem_public_key(data, backend=default_backend())


# assinatura

def sign_message(private_key, message_bytes: bytes) -> bytes:
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature


def verify_signature(public_key, message_bytes: bytes, signature: bytes) -> bool:
    try:
        # Comparação de Hashes internamente pela bliblioteca do cryptography
        public_key.verify(
            signature,
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False


# cifragem híbrida (AES-GCM + RSA-OAEP)

def hybrid_encrypt(recipient_public_key, plaintext_bytes: bytes) -> bytes:
    # gera chave AES-256
    aes_key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)  # 96-bit nonce para AES-GCM

    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, associated_data=None)

    # cifra a chave AES com RSA-OAEP
    encrypted_key = recipient_public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # monta JSON com base64 para facilitar armazenamento
    package = {
        "enc_key": base64.b64encode(encrypted_key).decode('ascii'),
        "nonce": base64.b64encode(nonce).decode('ascii'),
        "ciphertext": base64.b64encode(ciphertext).decode('ascii'),
    }
    return json.dumps(package).encode('utf-8')


def hybrid_decrypt(recipient_private_key, package_bytes: bytes) -> bytes:
    package = json.loads(package_bytes.decode('utf-8'))
    encrypted_key = base64.b64decode(package['enc_key'])
    nonce = base64.b64decode(package['nonce'])
    ciphertext = base64.b64decode(package['ciphertext'])

    aes_key = recipient_private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    return plaintext


# fluxos principais

def do_gen_keys(name_prefix: str, keysize: int = 2048):
    priv_path = Path(f"{name_prefix}_private.pem")
    pub_path = Path(f"{name_prefix}_public.pem")

    priv, pub = gen_rsa_keypair(keysize=keysize)
    save_private_key(priv, priv_path)
    save_public_key(pub, pub_path)

    return priv_path, pub_path


def do_sign_encrypt(sender_priv_path: Path, recipient_pub_path: Path, infile: Path, outfile: Path):
    sender_priv = load_private_key(sender_priv_path)
    recipient_pub = load_public_key(recipient_pub_path)

    message_bytes = infile.read_bytes()

    signature = sign_message(sender_priv, message_bytes)

    # pacote interno: message mais signature
    inner = {
        "message": base64.b64encode(message_bytes).decode('ascii'),
        "signature": base64.b64encode(signature).decode('ascii'),
    }
    inner_bytes = json.dumps(inner).encode('utf-8')

    encrypted_package = hybrid_encrypt(recipient_pub, inner_bytes)
    outfile.write_bytes(encrypted_package)
    return outfile


def do_decrypt_verify(recipient_priv_path: Path, sender_pub_path: Path, infile: Path, outfile: Path) -> bool:
    recipient_priv = load_private_key(recipient_priv_path)
    sender_pub = load_public_key(sender_pub_path)

    package_bytes = infile.read_bytes()
    inner_bytes = hybrid_decrypt(recipient_priv, package_bytes)

    inner = json.loads(inner_bytes.decode('utf-8'))
    message = base64.b64decode(inner['message'])
    signature = base64.b64decode(inner['signature'])

    ok = verify_signature(sender_pub, message, signature)

    if ok:
        outfile.write_bytes(message)
    return ok


# CLI (mantido)

def build_parser():
    p = argparse.ArgumentParser(description="TVC01 - Assinatura digital + Criptografia (demo automática se sem args)")
    sub = p.add_subparsers(dest='cmd')

    g = sub.add_parser('gen-keys', help='Gerar par de chaves RSA')
    g.add_argument('--name', required=True, help='Prefixo de nome para arquivos (ex: sender, recipient)')
    g.add_argument('--keysize', type=int, default=2048, help='Tamanho da chave RSA (default: 2048)')
    g.set_defaults(func=lambda a: do_gen_keys(a.name, a.keysize))

    s = sub.add_parser('sign-encrypt', help='Assinar mensagem e cifrar para destinatário')
    s.add_argument('--sender-priv', required=True, help='arquivo PEM da chave privada do remetente')
    s.add_argument('--recipient-pub', required=True, help='arquivo PEM da chave pública do destinatário')
    s.add_argument('--in', dest='infile', required=True, help='arquivo de entrada (mensagem)')
    s.add_argument('--out', dest='outfile', required=True, help='arquivo de saída (pacote cifrado)')
    s.set_defaults(func=lambda a: do_sign_encrypt(Path(a.sender_priv), Path(a.recipient_pub), Path(a.infile), Path(a.outfile)))

    d = sub.add_parser('decrypt-verify', help='Decifrar pacote e verificar assinatura')
    d.add_argument('--recipient-priv', required=True, help='arquivo PEM da chave privada do destinatário')
    d.add_argument('--sender-pub', required=True, help='arquivo PEM da chave pública do remetente')
    d.add_argument('--in', dest='infile', required=True, help='arquivo de entrada (pacote cifrado)')
    d.add_argument('--out', dest='outfile', required=True, help='arquivo de saída (mensagem decifrada)')
    d.set_defaults(func=lambda a: do_decrypt_verify(Path(a.recipient_priv), Path(a.sender_pub), Path(a.infile), Path(a.outfile)))

    return p


# Demo automática

def demo_run():
    base = Path('.')
    # nomes de arquivo usados na demo
    sender_priv = base / 'sender_private.pem'
    sender_pub = base / 'sender_public.pem'
    recipient_priv = base / 'recipient_private.pem'
    recipient_pub = base / 'recipient_public.pem'
    mensagem_file = base / 'mensagem_demo.txt'
    pacote_file = base / 'pacote_demo.bin'
    mensagem_out = base / 'mensagem_decryptada_demo.txt'

    print('=== Demo TVC01 - Assinatura + Criptografia ===')

    # Gera chaves
    print('Gerando chaves para sender...')
    do_gen_keys('sender')
    print('Gerando chaves para recipient...')
    do_gen_keys('recipient')

    # Mensagem de teste
    mensagem_text = b"Mensagem de teste TVC01 - ola mundo (demo)"
    mensagem_file.write_bytes(mensagem_text)
    print(f'Mensagem de teste salva em: {mensagem_file}')

    # Assinar mais a cifragem
    print('Assinando e cifrando o pacote...')
    do_sign_encrypt(sender_priv, recipient_pub, mensagem_file, pacote_file)
    print(f'Pacote cifrado salvo em: {pacote_file}')

    # Decifrar mais verificação
    print('Decifrando e verificando assinatura...')
    ok = do_decrypt_verify(recipient_priv, sender_pub, pacote_file, mensagem_out)

    if ok:
        print('Assinatura válida! Mensagem decifrada salva em:', mensagem_out)
        recovered = mensagem_out.read_bytes()
        print('Conteúdo recuperado:', recovered.decode('utf-8', errors='replace'))
    else:
        print('Assinatura inválida. Falha na verificação.')

    print('\nDemo concluída.')


def main():
    # Se houver argumentos na linha de comando, use o CLI; caso contrário rode a demo automática
    if len(sys.argv) > 1:
        parser = build_parser()
        args = parser.parse_args()
        if not hasattr(args, 'func'):
            parser.print_help()
            return
        result = args.func(args)
        # se a função retornar um booleano de sucesso (decrypt-verify), mostra feedback
        if isinstance(result, bool):
            print('Operação retornou:', result)
    else:
        demo_run()


if __name__ == '__main__':
    main()
