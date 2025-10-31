# 🔐 TVC01 - Assinatura Digital + Criptografia

Sistema completo de **assinatura digital** e **criptografia híbrida** implementado em Python, seguindo o **Esquema (b)** de criptografia com autenticação.

## 📋 O que este programa faz?

Este programa implementa um sistema de comunicação segura que garante:

- ✅ **Confidencialidade**: Apenas o destinatário pode ler a mensagem (criptografia AES-256-GCM)
- ✅ **Autenticidade**: Confirma quem enviou a mensagem (assinatura RSA-PSS)
- ✅ **Integridade**: Detecta qualquer alteração na mensagem (hash SHA-256)
- ✅ **Não-repúdio**: O remetente não pode negar que enviou (assinatura digital)

## 🔬 Como funciona (resumo técnico)

### **Envio de mensagem (Origem A):**

1. Calcula hash SHA-256 da mensagem → `H(M)`
2. Assina o hash com chave privada do remetente → `E(PR_a, H(M))`
3. Empacota mensagem + assinatura → `[M || assinatura]`
4. Gera chave AES-256 aleatória e cifra o pacote → `E(K, [M || assinatura])`
5. Cifra a chave AES com chave pública do destinatário → `E(PU_b, K)`
6. Envia pacote cifrado completo

### **Recebimento de mensagem (Destino B):**

1. Decifra a chave AES com sua chave privada → `D(PR_b, E(PU_b, K))`
2. Decifra o pacote com a chave AES → `D(K, pacote)`
3. Extrai mensagem e assinatura
4. Calcula hash da mensagem recebida → `H(M)_novo`
5. Verifica assinatura com chave pública do remetente → `D(PU_a, assinatura)`
6. Compara os hashes: se iguais, a mensagem é autêntica e íntegra! ✅

## 🚀 Instalação

### **Requisitos:**

- Python 3.7 ou superior
- Biblioteca `cryptography`

### **Instalar dependências:**

```bash
pip install cryptography
```

## 📖 Como usar

### **Modo 1: Demo Automática (Recomendado para teste)**

Execute o programa sem argumentos para ver uma demonstração completa:

```bash
python src/digital_signature.py
```

**O que a demo faz:**

1. Gera chaves para remetente e destinatário
2. Cria uma mensagem de teste
3. Assina e criptografa a mensagem
4. Decriptografa e verifica a assinatura
5. Mostra os resultados na tela

**Arquivos gerados pela demo:**

```
sender_private.pem           # Chave privada do remetente
sender_public.pem            # Chave pública do remetente
recipient_private.pem        # Chave privada do destinatário
recipient_public.pem         # Chave pública do destinatário
mensagem_demo.txt            # Mensagem original
pacote_demo.bin              # Mensagem cifrada + assinada
mensagem_decryptada_demo.txt # Mensagem recuperada
```

---

### **Modo 2: Uso Manual (CLI)**

Para uso em cenários reais, o programa oferece 3 comandos:

#### **1️⃣ Gerar chaves RSA**

```bash
python src/digital_signature.py gen-keys --name alice
python src/digital_signature.py gen-keys --name bob
```

- Gera `alice_private.pem` e `alice_public.pem`
- Gera `bob_private.pem` e `bob_public.pem`
- **Importante**: Compartilhe apenas as chaves públicas!

#### **2️⃣ Assinar e criptografar mensagem**

```bash
python src/digital_signature.py sign-encrypt \
  --sender-priv alice_private.pem \
  --recipient-pub bob_public.pem \
  --in minha_mensagem.txt \
  --out pacote_seguro.bin
```

- Alice assina a mensagem com sua chave privada
- Criptografa para Bob usando a chave pública dele
- Gera arquivo `pacote_seguro.bin` (pode ser enviado por e-mail, USB, etc.)

#### **3️⃣ Decriptografar e verificar assinatura**

```bash
python src/digital_signature.py decrypt-verify \
  --recipient-priv bob_private.pem \
  --sender-pub alice_public.pem \
  --in pacote_seguro.bin \
  --out mensagem_recuperada.txt
```

- Bob decripta com sua chave privada
- Verifica assinatura usando chave pública de Alice
- Se válido, salva mensagem em `mensagem_recuperada.txt`
- Se inválido, retorna erro (mensagem foi adulterada ou não é de Alice)

## 💡 Exemplo Prático Completo

Imagine que Alice quer enviar uma mensagem secreta para Bob:

```bash
# Passo 1: Gerar chaves para Alice e Bob
python src/digital_signature.py gen-keys --name alice
python src/digital_signature.py gen-keys --name bob

# Passo 2: Alice cria uma mensagem
echo "Reunião secreta às 15h" > mensagem_secreta.txt

# Passo 3: Alice assina e criptografa para Bob
python src/digital_signature.py sign-encrypt \
  --sender-priv alice_private.pem \
  --recipient-pub bob_public.pem \
  --in mensagem_secreta.txt \
  --out para_bob.bin

# Passo 4: Alice envia 'para_bob.bin' para Bob (e-mail, USB, etc.)

# Passo 5: Bob recebe e decripta
python src/digital_signature.py decrypt-verify \
  --recipient-priv bob_private.pem \
  --sender-pub alice_public.pem \
  --in para_bob.bin \
  --out mensagem_de_alice.txt

# Passo 6: Bob lê a mensagem
cat mensagem_de_alice.txt
# Saída: "Reunião secreta às 15h"
```

## 🔒 Segurança Implementada

| Tecnologia      | Uso                                 | Segurança                   |
| --------------- | ----------------------------------- | --------------------------- |
| **RSA-2048**    | Assinatura digital e troca de chave | Padrão moderno              |
| **RSA-PSS**     | Esquema de padding para assinatura  | Mais seguro que PKCS#1 v1.5 |
| **RSA-OAEP**    | Padding para criptografia de chave  | Resistente a ataques        |
| **AES-256-GCM** | Criptografia simétrica              | Nível militar               |
| **SHA-256**     | Função hash                         | Resistente a colisões       |

## 📂 Estrutura do Projeto

```
tvc1-final/
├── src/
│   ├── digital_signature.py    # Programa principal
│   └── README.md
├── docker-compose.yml
└── README.md                    # Este arquivo
```

## ⚠️ Avisos Importantes

1. **Chaves privadas**: NUNCA compartilhe suas chaves privadas! Mantenha-as em segredo.
2. **Chaves públicas**: Podem ser compartilhadas livremente.
3. **Produção**: Para uso em produção, proteja chaves privadas com senha.
4. **Tamanho de mensagem**: RSA tem limite de tamanho. Este programa usa criptografia híbrida, então aceita mensagens de qualquer tamanho.

## 🎓 Contexto Acadêmico

Este projeto implementa o **Esquema (b)** de assinatura digital com criptografia, conforme especificação do trabalho de Segurança da Informação (TVC01).

**Referências:**

- Diagrama de assinatura digital com criptografia
- Hash SHA-256 para integridade
- Criptografia híbrida (AES + RSA) para eficiência

---

**Desenvolvido para**: Trabalho de Verificação Contínua 01 (TVC01)  
**Disciplina**: Segurança da Informação  
**Tecnologia**: Python 3 + biblioteca cryptography
