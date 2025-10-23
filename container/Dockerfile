# ===============================
# IMAGEM BASE
# ===============================
FROM ubuntu:latest

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

# ===============================
# INSTALAR DEPENDÊNCIAS ESSENCIAIS
# ===============================
RUN apt update -y && apt install -y --no-install-recommends \
    curl ca-certificates gnupg git build-essential \
    nodejs npm \
    python3 python3-pip \
    nano vim less unzip zip wget jq tree \
 && apt clean && rm -rf /var/lib/apt/lists/*

# ===============================
# INSTALAR FERRAMENTAS DE ANÁLISE NODE
# ===============================
RUN npm install -g \
    eslint \
    eslint-plugin-security \
    retire \
    npm-audit-resolver \
    semgrep \
    snyk

# ===============================
# CRIAR DIRETÓRIO DE ANÁLISE
# ===============================
WORKDIR /opt/analysis

# Criar usuário não-root
RUN useradd -m analyst && chown -R analyst:analyst /opt/analysis
USER analyst

CMD ["/bin/bash"]
