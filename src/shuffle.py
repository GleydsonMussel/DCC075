import random
import re
from collections import defaultdict

def get_text(path: str):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def treat_text(text: str):
    """Limpa o texto de forma mais completa"""
    text = re.sub(r'[^a-zA-Z]', '', text)
    return text.lower()

def count_letters_in_text(text: str):
    letters_count = defaultdict(int)
    total_letters = 0
    
    for char in text:
        if char.isalpha():
            letters_count[char] += 1
            total_letters += 1
    
    letters_distribution = {}
    for char, count in letters_count.items():
        letters_distribution[char] = count / total_letters
    
    return letters_distribution, total_letters

def get_ref_letters_distribution(path: str):
    text = get_text(path)
    treated_text = treat_text(text)
    distribution, total = count_letters_in_text(treated_text)
    return distribution, total

def generate_substitution_key(alphabet):
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    encrypt_key = dict(zip(alphabet, shuffled))
    decrypt_key = dict(zip(shuffled, alphabet))
    return encrypt_key, decrypt_key

def encrypt_message(message: str, substitution_key: dict):
    encrypted = ""
    for char in message.lower():
        encrypted += substitution_key.get(char, char)
    return encrypted

def decrypt_message(encrypted_message: str, reverse_key: dict):
    decrypted = ""
    for char in encrypted_message.lower():
        decrypted += reverse_key.get(char, char)
    return decrypted

def frequency_attack(encrypted_message: str, ref_distribution: dict, alphabet):
    """Ataque de frequência melhorado"""
    # Limpa e analisa apenas o texto cifrado
    cleaned_encrypted = treat_text(encrypted_message)
    encrypted_freq, _ = count_letters_in_text(cleaned_encrypted)
    
    # Preenche frequências zero para letras não encontradas
    for char in alphabet:
        if char not in encrypted_freq:
            encrypted_freq[char] = 0.0
    
    # Ordena por frequência (mais comum primeiro)
    ref_sorted = sorted(ref_distribution.items(), key=lambda x: x[1], reverse=True)
    encrypted_sorted = sorted(encrypted_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Cria mapeamento baseado na ordem de frequência
    frequency_key = {}
    for i, (encrypted_char, _) in enumerate(encrypted_sorted):
        if i < len(ref_sorted):
            ref_char, _ = ref_sorted[i]
            frequency_key[encrypted_char] = ref_char
        else:
            frequency_key[encrypted_char] = encrypted_char
    
    # Aplica o mapeamento
    attempted_decrypt = ""
    for char in encrypted_message.lower():
        attempted_decrypt += frequency_key.get(char, char)
    
    return attempted_decrypt, frequency_key

def calculate_accuracy(original, attempted):
    correct = 0
    total = 0
    for orig, att in zip(original.lower(), attempted):
        if orig.isalpha() and att.isalpha():
            total += 1
            if orig == att:
                correct += 1
    return (correct / total * 100) if total > 0 else 0

def main():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    reference_file = "./texts/kafka.txt"
    message = get_text("./texts/far_far_away.txt")
    
    # Abrir arquivo de output para salvar o log completo
    with open("./output/teste.txt", 'w', encoding='utf-8') as output_file:
        
        print("=== SISTEMA DE CRIPTOGRAFIA POR SUBSTITUIÇÃO ===\n")
        print("=== SISTEMA DE CRIPTOGRAFIA POR SUBSTITUIÇÃO ===\n", file=output_file)
        
        # 1. Obter distribuição de referência
        print("1. Analisando distribuição de letras...")
        print("1. Analisando distribuição de letras...", file=output_file)
        try:
            ref_distribution, total_ref = get_ref_letters_distribution(reference_file)
            print(f"   Total de letras: {total_ref}")
            print(f"   Total de letras: {total_ref}", file=output_file)
            
            top_10 = sorted(ref_distribution.items(), key=lambda x: x[1], reverse=True)[:10]
            print("   Top 10 letras mais comuns:")
            print("   Top 10 letras mais comuns:", file=output_file)
            
            for char, freq in top_10:
                print(f"     '{char}': {freq:.6f} ({freq*100:.2f}%)")
                print(f"     '{char}': {freq:.6f} ({freq*100:.2f}%)", file=output_file)
                
        except FileNotFoundError:
            print(f"   Arquivo não encontrado!")
            print(f"   Arquivo não encontrado!", file=output_file)
            return
        
        # 2. Gerar chave
        print("\n2. Gerando chave de criptografia...")
        print("\n2. Gerando chave de criptografia...", file=output_file)
        
        encrypt_key, decrypt_key = generate_substitution_key(alphabet)
        print(f"   Chave: {encrypt_key}")
        print(f"   Chave: {encrypt_key}", file=output_file)
        
        # 3. Criptografar
        print(f"\n3. Criptografando: '{message}'")
        print(f"\n3. Criptografando: '{message}'", file=output_file)
        
        encrypted = encrypt_message(message, encrypt_key)
        print(f"   Criptografado: '{encrypted}'")
        print(f"   Criptografado: '{encrypted}'", file=output_file)
        
        # 4. Descriptografar com chave correta
        print("\n4. Descriptografando com chave...")
        print("\n4. Descriptografando com chave...", file=output_file)
        
        decrypted = decrypt_message(encrypted, decrypt_key)
        print(f"   Descriptografado: '{decrypted}'")
        print(f"   Descriptografado: '{decrypted}'", file=output_file)
        
        # 5. Ataque de frequência
        print("\n5. Tentativa por análise de frequência...")
        print("\n5. Tentativa por análise de frequência...", file=output_file)
        
        attempted, freq_key = frequency_attack(encrypted, ref_distribution, alphabet)
        
        print("   Mapeamento completo:")
        print("   Mapeamento completo:", file=output_file)
        
        for char in sorted(alphabet):
            mapping_line = f"     {char} -> {freq_key.get(char, '?')}"
            print(mapping_line)
            print(mapping_line, file=output_file)
        
        print(f"   Tentativa: '{attempted}'")
        print(f"   Tentativa: '{attempted}'", file=output_file)
        
        # 6. Avaliação
        print(f"\n6. Resultados:")
        print(f"\n6. Resultados:", file=output_file)
        
        accuracy = calculate_accuracy(message, attempted)
        print(f"   Taxa de acerto: {accuracy:.1f}%")
        print(f"   Taxa de acerto: {accuracy:.1f}%", file=output_file)
        
        # Mostrar comparação lado a lado
        print(f"\n   Original:  '{message}'")
        print(f"\n   Original:  '{message}'", file=output_file)
        
        print(f"   Tentativa: '{attempted}'")
        print(f"   Tentativa: '{attempted}'", file=output_file)
        
        print(f"   Diferenças: ", end="")
        print(f"   Diferenças: ", end="", file=output_file)
        
        differences = []
        for orig, att in zip(message.lower(), attempted):
            if orig.isalpha() and att.isalpha() and orig != att:
                diff_str = f"{orig}({att})"
                print(f"{diff_str} ", end="")
                print(f"{diff_str} ", end="", file=output_file)
                differences.append(diff_str)
        
        print()
        print(file=output_file)
        
        # Escrever diferenças de forma organizada
        print("\n   Lista completa de diferenças:")
        print("\n   Lista completa de diferenças:", file=output_file)
        
        for i, diff in enumerate(differences, 1):
            diff_line = f"   {i:2d}. {diff}"
            print(diff_line)
            print(diff_line, file=output_file)
    
    # SALVAR A TENTATIVA DE DESCRIPTOGRAFIA EM ARQUIVO SEPARADO
    with open("./output/tentativa_descriptografia.txt", 'w', encoding='utf-8') as attempt_file:
        attempt_file.write("=== TENTATIVA DE DESCRIPTOGRAFIA POR ANÁLISE DE FREQUÊNCIA ===\n\n")
        attempt_file.write(f"Texto original: {message}\n\n")
        attempt_file.write(f"Texto criptografado: {encrypted}\n\n")
        attempt_file.write(f"Tentativa de descriptografia: {attempted}\n\n")
        attempt_file.write(f"Taxa de acerto: {accuracy:.1f}%\n\n")
        attempt_file.write("Mapeamento utilizado:\n")

if __name__ == "__main__":
    main()