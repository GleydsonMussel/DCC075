#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import Counter
import os


class ContadorOcorrencias:
    def __init__(self):
        self.texto_completo = ""
        self.palavras = []
        self.caracteres = []
    
    def carregar_arquivo(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                self.texto_completo = arquivo.read()
            return True
        except FileNotFoundError:
            print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            return False
    
    def limpar_texto(self, texto):
        texto = re.sub(r'[^\w\s]', '', texto.lower())
        return texto
    
    def contar_palavras(self):
        texto_limpo = self.limpar_texto(self.texto_completo)
        self.palavras = texto_limpo.split()
        return Counter(self.palavras)
    
    def contar_caracteres(self):
        texto_limpo = re.sub(r'[^a-zA-ZÀ-ÿ]', '', self.texto_completo.lower())
        self.caracteres = list(texto_limpo)
        return Counter(self.caracteres)
    
    def estatisticas_gerais(self):
        caracteres_total = len(self.caracteres) if self.caracteres else 0
        return {
            'total_caracteres': caracteres_total,
            'tamanho_arquivo': len(self.texto_completo)
        }
    
    def caracteres_mais_frequentes(self, top_n=10):
        contador_caracteres = self.contar_caracteres()
        return contador_caracteres.most_common(top_n)
    
    def gerar_relatorio(self, nome_arquivo_saida=None):
        estatisticas = self.estatisticas_gerais()
        palavras_freq = self.palavras_mais_frequentes(20)
        caracteres_freq = self.caracteres_mais_frequentes(10)
        
        relatorio = f"""
RELATÓRIO DE ANÁLISE DE TEXTO
==============================

ESTATÍSTICAS GERAIS:
- Total de caracteres (letras): {estatisticas['total_caracteres']}
- Tamanho do arquivo: {estatisticas['tamanho_arquivo']} caracteres

"""     
        relatorio += "\nTOP 10 CARACTERES MAIS FREQUENTES:\n"
        for i, (caractere, frequencia) in enumerate(caracteres_freq, 1):
            relatorio += f"{i:2d}. '{caractere}': {frequencia} ocorrências\n"
        
        if nome_arquivo_saida:
            with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo:
                arquivo.write(relatorio)
                arquivo.close()
            print(f"Relatório salvo em: {nome_arquivo_saida}")
        else:
            print(relatorio)
    
    def gerar_dicionario_frequencias(self):
        caracteres_freq = self.contar_caracteres()
        total_caracteres = sum(caracteres_freq.values())
        
        if total_caracteres == 0:
            return {}
        
        # Mapeamento de caracteres acentuados para básicos
        mapeamento_acentos = {
            'à': 'A', 'á': 'A', 'â': 'A', 'ã': 'A', 'ä': 'A', 'å': 'A', 'æ': 'A',
            'è': 'E', 'é': 'E', 'ê': 'E', 'ë': 'E',
            'ì': 'I', 'í': 'I', 'î': 'I', 'ï': 'I',
            'ò': 'O', 'ó': 'O', 'ô': 'O', 'õ': 'O', 'ö': 'O', 'ø': 'O',
            'ù': 'U', 'ú': 'U', 'û': 'U', 'ü': 'U',
            'ý': 'Y', 'þ': 'T', 'ÿ': 'Y',
            'ç': 'C', 'ñ': 'N', 'ð': 'D'
        }
        
        frequencias_percentuais = {}
        for caractere, count in caracteres_freq.items():
            # Converte acentos para letras básicas
            if caractere in mapeamento_acentos:
                caractere_final = mapeamento_acentos[caractere]
            else:
                caractere_final = caractere.upper()
            
            # Soma frequências se a letra já existir
            if caractere_final in frequencias_percentuais:
                frequencias_percentuais[caractere_final] += round((count / total_caracteres) * 100, 2)
            else:
                frequencias_percentuais[caractere_final] = round((count / total_caracteres) * 100, 2)
        
        return frequencias_percentuais
    
    def imprimir_dicionario_frequencias(self):
        frequencias = self.gerar_dicionario_frequencias()
        
        print("FREQUÊNCIAS DE CARACTERES (FORMATO DICIONÁRIO):")
        print("=" * 50)
        
        # Ordena por frequência decrescente
        frequencias_ordenadas = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
        
        print("frequencias_caracteres = {")
        for i, (caractere, freq) in enumerate(frequencias_ordenadas):
            if i == len(frequencias_ordenadas) - 1:
                print(f"    '{caractere}': {freq}")
            else:
                print(f"    '{caractere}': {freq},")
        print("}")
        
        return frequencias
    
    def exportar_dicionario_python(self, nome_arquivo="frequencias_caracteres.py"):
        frequencias = self.gerar_dicionario_frequencias()
        
        # Ordena por frequência decrescente
        frequencias_ordenadas = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
        
        codigo_python = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

frequencias_caracteres = {{
'''
        
        for caractere, freq in frequencias_ordenadas:
            codigo_python += f"    '{caractere}': {freq},\n"
        
        codigo_python += '''}
'''
        
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write(codigo_python)
            print(f"Arquivo pronto para importar na Cifra de César!")
            return True
        except Exception as e:
            print(f"✗ Erro ao exportar: {e}")
            return False


def main():
    contador = ContadorOcorrencias()
    
    print("CONTADOR DE OCORRÊNCIAS EM ARQUIVOS DE TEXTO")
    print("=" * 50)
    
    while True:
        print("\nEscolha uma opção:")
        print("1. Carregar arquivo")
        print("2. Contar caracteres")
        print("3. Salvar relatório em arquivo")
        print("4. Gerar dicionário de frequências")
        print("5. Exportar dicionário para arquivo Python")
        print("0. Sair")
        
        escolha = input("\nDigite sua escolha (0-5): ").strip()
        
        if escolha == "0":
            print("Saindo...")
            break
        
        elif escolha == "1":
            nome_arquivo = input("Digite o nome do arquivo .txt: ").strip()
            if contador.carregar_arquivo(nome_arquivo):
                print(f"Arquivo '{nome_arquivo}' carregado com sucesso!")
            else:
                print("Falha ao carregar arquivo.")

        
        elif escolha == "2":
            if not contador.texto_completo:
                print("Nenhum arquivo carregado. Carregue um arquivo primeiro.")
                continue
            
            caracteres_freq = contador.contar_caracteres()
            print(f"\nTotal de caracteres únicos: {len(caracteres_freq)}")
            print("\nTop 10 caracteres mais frequentes:")
            for caractere, freq in caracteres_freq.most_common(10):
                print(f"  '{caractere}': {freq}")
        
        elif escolha == "3":
            if not contador.texto_completo:
                print("Nenhum arquivo carregado. Carregue um arquivo primeiro.")
                continue
            
            nome_saida = input("Digite o nome do arquivo de saída: ").strip()
            if nome_saida:
                contador.gerar_relatorio(nome_saida)
            else:
                print("Nome de arquivo inválido.")
        
        elif escolha == "4":
            if not contador.texto_completo:
                print("Nenhum arquivo carregado. Carregue um arquivo primeiro.")
                continue
            
            contador.imprimir_dicionario_frequencias()
        
        elif escolha == "5":
            if not contador.texto_completo:
                print("Nenhum arquivo carregado. Carregue um arquivo primeiro.")
                continue
            
            nome_arquivo = input("Digite o nome do arquivo Python (ou Enter para 'frequencias_caracteres.py'): ").strip()
            if not nome_arquivo:
                nome_arquivo = "frequencias_caracteres.py"
            
            contador.exportar_dicionario_python(nome_arquivo)
        
        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
