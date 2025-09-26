#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
from collections import Counter
import re


class CesarCipher:
    
    def __init__(self):
        self.alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alfabeto_minusculo = self.alfabeto.lower()
        
        self.frequencias_ref = {
            'E': 12.1,
            'T': 9.25,
            'O': 8.36,
            'A': 7.65,
            'I': 6.62,
            'R': 6.33,
            'N': 6.23,
            'S': 6.09,
            'H': 6.0,
            'L': 4.51,
            'D': 3.67,
            'U': 3.48,
            'M': 3.01,
            'Y': 2.44,
            'C': 2.42,
            'W': 2.36,
            'F': 1.98,
            'G': 1.87,
            'P': 1.66,
            'B': 1.63,
            'V': 1.01,
            'K': 0.8,
            'J': 0.31,
            'X': 0.13,
            'Q': 0.06,
            'Z': 0.03,
        }
    
    def clean_text(self, text):
        text = re.sub(r'[^a-zA-Z]', '', text)
        return text.upper()
    
    def encrypt(self, plaintext, key):
        if not isinstance(key, int) or key < 1:
            raise ValueError("A chave deve ser um número inteiro positivo")
        
        texto_limpo = self.clean_text(plaintext)
        texto_criptografado = ""
        
        for caractere in texto_limpo:
            if caractere in self.alfabeto:
                posicao = self.alfabeto.find(caractere)
                nova_posicao = (posicao + key) % len(self.alfabeto)
                texto_criptografado += self.alfabeto[nova_posicao]
            else:
                texto_criptografado += caractere
        
        return texto_criptografado
    
    def decrypt(self, ciphertext, key):
        if not isinstance(key, int) or key < 1:
            raise ValueError("A chave deve ser um número inteiro positivo")
        
        texto_criptografado = self.clean_text(ciphertext)
        texto_descriptografado = ""
        
        for caractere in texto_criptografado:
            if caractere in self.alfabeto:
                posicao = self.alfabeto.find(caractere)
                nova_posicao = (posicao - key) % len(self.alfabeto)
                texto_descriptografado += self.alfabeto[nova_posicao]
            else:
                texto_descriptografado += caractere
        
        return texto_descriptografado
    
    def calculate_frequencies(self, text):
        texto_limpo = self.clean_text(text)
        total_letras = len(texto_limpo)
        
        if total_letras == 0:
            return {}
        
        contador_letras = Counter(texto_limpo)
        
        frequencias = {}
        for letra, contagem in contador_letras.items():
            frequencias[letra] = (contagem / total_letras) * 100
        
        return frequencias
    
    def frequency_analysis(self, ciphertext):
        texto_criptografado = self.clean_text(ciphertext)
        frequencias_criptografadas = self.calculate_frequencies(texto_criptografado)
        
        if not frequencias_criptografadas:
            return []
        
        correlacoes = []
        
        for chave in range(0, len(self.alfabeto)):
            pontuacao_correlacao = 0
            
            for letra in frequencias_criptografadas:
                posicao_criptografada = self.alfabeto.find(letra)
                posicao_original = (posicao_criptografada - chave) % len(self.alfabeto)
                letra_original = self.alfabeto[posicao_original]
                
                frequencia_criptografada = frequencias_criptografadas.get(letra, 0)
                frequencia_esperada = self.frequencias_ref.get(letra_original, 0)
                
                pontuacao_correlacao += frequencia_criptografada * frequencia_esperada
            
            correlacoes.append((chave, pontuacao_correlacao))
        
        correlacoes.sort(key=lambda x: x[1], reverse=True)
        
        return correlacoes
    
    def crack_cipher(self, ciphertext, top_n=5):
        correlacoes = self.frequency_analysis(ciphertext)
        candidatos = []
        
        for chave, pontuacao in correlacoes[:top_n]:
            texto_descriptografado = self.decrypt(ciphertext, chave)
            candidatos.append((chave, texto_descriptografado, pontuacao))
        
        return candidatos


def main():
    cifra = CesarCipher()
    
    print("=" * 60)
    print("CIFRA DE CÉSAR - ENCRIPTAÇÃO E CRIPTOANÁLISE")
    print("=" * 60)
    
    while True:
        print("\nEscolha uma opção:")
        print("1. Encriptar texto")
        print("2. Desencriptar texto")
        print("3. Análise de frequência")
        print("4. Quebrar cifra (criptoanálise)")
        print("0. Sair")
        
        escolha = input("\nDigite sua escolha (0-5): ").strip()
        
        if escolha == "0":
            print("Saindo...")
            break
        
        elif escolha == "1":
            texto = input("Digite o texto para encriptar: ")
            try:
                chave = int(input("Digite a chave (número inteiro positivo): "))
                texto_encriptado = cifra.encrypt(texto, chave)
                print(f"\nTexto encriptado: {texto_encriptado}")
                print(f"Chave usada: {chave}")
            except ValueError as e:
                print(f"Erro: {e}")
        
        elif escolha == "2":
            texto = input("Digite o texto encriptado: ")
            try:
                chave = int(input("Digite a chave usada na encriptação: "))
                texto_descriptografado = cifra.decrypt(texto, chave)
                print(f"\nTexto desencriptado: {texto_descriptografado}")
            except ValueError as e:
                print(f"Erro: {e}")
        
        elif escolha == "3":
            texto = input("Digite o texto para análise de frequência: ")
            frequencias = cifra.calculate_frequencies(texto)
            
            print(f"\nAnálise de frequência:")
            print("-" * 40)
            for letra, frequencia in sorted(frequencias.items(), key=lambda x: x[1], reverse=True):
                print(f"{letra}: {frequencia:.2f}%")
        
        elif escolha == "4":
            texto = input("Digite o texto encriptado para quebrar: ")
            candidatos = cifra.crack_cipher(texto, top_n=5)
            
            print(f"\nPossíveis chaves (ordenadas por probabilidade):")
            print("-" * 50)
            for i, (chave, texto_descriptografado, pontuacao) in enumerate(candidatos, 1):
                print(f"{i}. Chave: {chave} (Score: {pontuacao:.2f})")
                print(f"   Texto: {texto_descriptografado}")
                print()
        
        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
