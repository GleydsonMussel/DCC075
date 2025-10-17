import string

# ==============================
# Configurações básicas
# ==============================
ALPHABET = string.ascii_uppercase + "0123456789"
BLOCK_SIZE = 5

# Últimos 5 caracteres da matrícula
MATRICULA = "202265556C"
KEY = MATRICULA[-5:].upper()  # "5556C"

# Texto de exemplo (12 caracteres)
PLAINTEXT = "CRYPTOGRAPHY".upper()

# ==============================
# Funções utilitárias
# ==============================
def pad_text(text):
    """Adiciona padding com 'X' para múltiplo de BLOCK_SIZE."""
    while len(text) % BLOCK_SIZE != 0:
        text += "X"
    return text

def vigenere_encrypt_block(block, key):
    result = ""
    for i in range(len(block)):
        p = ALPHABET.index(block[i])
        k = ALPHABET.index(key[i])
        result += ALPHABET[(p + k) % len(ALPHABET)]
    return result

def vigenere_decrypt_block(block, key):
    result = ""
    for i in range(len(block)):
        c = ALPHABET.index(block[i])
        k = ALPHABET.index(key[i])
        result += ALPHABET[(c - k) % len(ALPHABET)]
    return result

# ==============================
# ECB mode
# ==============================
def encrypt_ecb(plaintext, key):
    plaintext = pad_text(plaintext)
    ciphertext = ""
    print("\n=== Modo ECB: Criptografia ===")
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        encrypted = vigenere_encrypt_block(block, key)
        print(f"Bloco {i//BLOCK_SIZE + 1}: {block} -> {encrypted}")
        ciphertext += encrypted
    return ciphertext

def decrypt_ecb(ciphertext, key):
    plaintext = ""
    print("\n=== Modo ECB: Decriptografia ===")
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        decrypted = vigenere_decrypt_block(block, key)
        print(f"Bloco {i//BLOCK_SIZE + 1}: {block} -> {decrypted}")
        plaintext += decrypted
    return plaintext

# ==============================
# CFB mode
# ==============================
def encrypt_cfb(plaintext, key, iv):
    plaintext = pad_text(plaintext)
    ciphertext = ""
    prev = iv
    print("\n=== Modo CFB: Criptografia ===")
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        s = vigenere_encrypt_block(prev, key)
        encrypted = ""
        for j in range(BLOCK_SIZE):
            p = ALPHABET.index(block[j])
            s_val = ALPHABET.index(s[j])
            encrypted += ALPHABET[(p + s_val) % len(ALPHABET)]
        print(f"Bloco {i//BLOCK_SIZE + 1}: P={block}, S={s}, C={encrypted}")
        ciphertext += encrypted
        prev = encrypted
    return ciphertext

def decrypt_cfb(ciphertext, key, iv):
    plaintext = ""
    prev = iv
    print("\n=== Modo CFB: Decriptografia ===")
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        s = vigenere_encrypt_block(prev, key)
        decrypted = ""
        for j in range(BLOCK_SIZE):
            c = ALPHABET.index(block[j])
            s_val = ALPHABET.index(s[j])
            decrypted += ALPHABET[(c - s_val) % len(ALPHABET)]
        print(f"Bloco {i//BLOCK_SIZE + 1}: C={block}, S={s}, P={decrypted}")
        plaintext += decrypted
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

    print("\nCiphertext (ECB):", cipher_ecb)
    print("Texto decifrado (ECB):", plain_ecb)

    # CFB
    IV = "ABCDE"
    cipher_cfb = encrypt_cfb(PLAINTEXT, KEY, IV)
    plain_cfb = decrypt_cfb(cipher_cfb, KEY, IV)

    print("\nCiphertext (CFB):", cipher_cfb)
    print("Texto decifrado (CFB):", plain_cfb)

    # Cabeçalhos simulados
    print("\n=== Cabeçalhos simulados ===")
    print("ECB HEADER:", f"MODE=ECB|KEY={KEY}|BLOCK_SIZE={BLOCK_SIZE}")
    print("CFB HEADER:", f"MODE=CFB|KEY={KEY}|BLOCK_SIZE={BLOCK_SIZE}|IV={IV}")
