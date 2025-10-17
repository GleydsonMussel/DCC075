import string

# ==============================
# Configurações básicas
# ==============================
BLOCK_SIZE = 5
MATRICULA = "202265556C"
KEY = MATRICULA[-5:].encode()  # bytes, ex: b"5556C"
PLAINTEXT = b"CRYPTOGRAPHY"    # bytes também
IV = b"ABCDE"                  # vetor de inicialização (bytes)
TAM_ALFABETO = 256             # Tamanho do alfabeto, como está em bytes considerando a tabela ASCII, usa-se 256

# ==============================
# Funções utilitárias
# ==============================
def pad_bytes(data: bytes)->bytes:
    """Adiciona padding com b'X' até múltiplo de BLOCK_SIZE."""
    while len(data) % BLOCK_SIZE != 0:
        data += b"X"
    return data

def vigenere_encrypt_block(block: bytes, key: bytes) -> bytes:
    """Cifra tipo Vigenère byte a byte"""
    result = []
    for i in range(len(block)):
        soma = (block[i] + key[i % len(key)]) % TAM_ALFABETO
        result.append(soma)
    return bytes(result)

def vigenere_decrypt_block(block: bytes, key: bytes):
    result = []
    for i in range(len(block)):
        soma = (block[i] - key[i % len(key)]) % TAM_ALFABETO
        result.append(soma)
    return bytes(result)

def xor_bytes(block1: bytes, block2: bytes):
    """Aplica XOR bit a bit entre dois blocos de bytes."""
    return bytes([x ^ y for x, y in zip(block1, block2)])

# ==============================
# ECB mode
# ==============================
def encrypt_ecb(plaintext, key):
    plaintext = pad_bytes(plaintext)
    ciphertext = b""
    print("\n=== Modo ECB: Criptografia ===")
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        encrypted = vigenere_encrypt_block(block, key)
        print(f"Bloco {i//BLOCK_SIZE + 1}: {block} -> {encrypted.hex().upper()}")
        ciphertext += encrypted
    return ciphertext

def decrypt_ecb(ciphertext, key):
    plaintext = b""
    print("\n=== Modo ECB: Decriptografia ===")
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        decrypted = vigenere_decrypt_block(block, key)
        print(f"Bloco {i//BLOCK_SIZE + 1}: {block.hex().upper()} -> {decrypted}")
        plaintext += decrypted
    return plaintext

# ==============================
# CFB mode (com XOR bit a bit)
# ==============================
def encrypt_cfb(plaintext, key, iv):
    plaintext = pad_bytes(plaintext)
    ciphertext = b""
    prev = iv
    print("\n=== Modo CFB: Criptografia (bit a bit real) ===")
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        # 1. XOR entre plaintext e bloco anterior (feedback)
        xor_result = xor_bytes(block, prev)
        # 2. Cifra o resultado do XOR
        encrypted = vigenere_encrypt_block(xor_result, key)
        print(f"Bloco {i//BLOCK_SIZE + 1}:")
        print(f"  P = {block} ({block.hex().upper()})")
        print(f"  IV/Cprev = {prev} ({prev.hex().upper()})")
        print(f"  XOR = {xor_result.hex().upper()}")
        print(f"  C = {encrypted.hex().upper()}\n")
        ciphertext += encrypted
        prev = encrypted  # feedback
    return ciphertext

def decrypt_cfb(ciphertext, key, iv):
    plaintext = b""
    prev = iv
    print("\n=== Modo CFB: Decriptografia (bit a bit real) ===")
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        # 1. Decifra o bloco atual
        decrypted_block = vigenere_decrypt_block(block, key)
        # 2. XOR com o bloco anterior para recuperar o plaintext
        plain_block = xor_bytes(decrypted_block, prev)
        print(f"Bloco {i//BLOCK_SIZE + 1}:")
        print(f"  C = {block.hex().upper()}")
        print(f"  IV/Cprev = {prev.hex().upper()}")
        print(f"  D(C) = {decrypted_block.hex().upper()}")
        print(f"  P = {plain_block} ({plain_block.hex().upper()})\n")
        plaintext += plain_block
        prev = block
    return plaintext

# ==============================
# Execução principal
# ==============================
if __name__ == "__main__":
    print("Chave usada:", KEY)
    print("Texto original:", PLAINTEXT)

    # ECB
    cipher_ecb = encrypt_ecb(PLAINTEXT, KEY)
    plain_ecb = decrypt_ecb(cipher_ecb, KEY)
    print("\nCiphertext (ECB):", cipher_ecb.hex().upper())
    print("Texto decifrado (ECB):", plain_ecb)

    # CFB
    cipher_cfb = encrypt_cfb(PLAINTEXT, KEY, IV)
    plain_cfb = decrypt_cfb(cipher_cfb, KEY, IV)
    print("\nCiphertext (CFB):", cipher_cfb.hex().upper())
    print("Texto decifrado (CFB):", plain_cfb)

    print("\n=== Cabeçalhos simulados ===")
    print("ECB HEADER:", f"MODE=ECB|FILE_SIZE={len(PLAINTEXT)}|BLOCK_SIZE={BLOCK_SIZE}")
    print("CFB HEADER:", f"MODE=CFB|FILE_SIZE={len(PLAINTEXT)}|BLOCK_SIZE={BLOCK_SIZE}|IV={IV.decode()}\n")
