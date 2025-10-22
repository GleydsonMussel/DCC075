# Dockerfile: jail dentro do container com npm funcional (heredoc corrigido)
FROM ubuntu:latest

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

# 1) instalar ferramentas
RUN apt update -y && apt install -y --no-install-recommends \
    ca-certificates curl coreutils bash dos2unix \
    git build-essential g++ cmake \
    python3 python3-dev python3-pip \
    nodejs npm util-linux \
 && apt clean && rm -rf /var/lib/apt/lists/*

# 2) criar estrutura da jail (diretórios explícitos)
RUN mkdir -p /opt/jail/bin && \
    mkdir -p /opt/jail/lib && \
    mkdir -p /opt/jail/lib64 && \
    mkdir -p /opt/jail/etc && \
    mkdir -p /opt/jail/var && \
    mkdir -p /opt/jail/tmp && \
    mkdir -p /opt/jail/usr/bin && \
    mkdir -p /opt/jail/usr/lib && \
    mkdir -p /opt/jail/usr/share && \
    mkdir -p /opt/jail/dev && \
    mkdir -p /opt/jail/proc && \
    mkdir -p /opt/jail/sys && \
    mkdir -p /opt/jail/home && \
    chmod 755 /opt/jail

# 3) copiar binários essenciais
RUN cp -v /bin/bash /opt/jail/bin/ || true
RUN cp -v /bin/ls /opt/jail/bin/ || true
RUN cp -v /usr/bin/env /opt/jail/usr/bin/ || true

# 4) copiar node/npm e módulos globais (se existirem)
RUN cp -v /usr/bin/node /opt/jail/usr/bin/ || true
RUN cp -v /usr/bin/npm /opt/jail/usr/bin/ || true
RUN if [[ -d /usr/lib/node_modules ]]; then cp -a /usr/lib/node_modules /opt/jail/usr/lib/; fi || true
RUN if [[ -d /usr/share/nodejs ]]; then cp -a /usr/share/nodejs /opt/jail/usr/share/; fi || true

# 5) PASSO EXTRA (agressivo): copiar praticamente todas as libs do sistema para dentro da jail
RUN set -eux; \
    if [[ -d /lib ]]; then mkdir -p /opt/jail/lib && cp -a /lib/. /opt/jail/lib/; fi; \
    if [[ -d /lib64 ]]; then mkdir -p /opt/jail/lib64 && cp -a /lib64/. /opt/jail/lib64/; fi; \
    if [[ -d /usr/lib ]]; then mkdir -p /opt/jail/usr/lib && cp -a /usr/lib/. /opt/jail/usr/lib/; fi; \
    if [[ -d /usr/lib/x86_64-linux-gnu ]]; then mkdir -p /opt/jail/usr/lib/x86_64-linux-gnu && cp -a /usr/lib/x86_64-linux-gnu/. /opt/jail/usr/lib/x86_64-linux-gnu/; fi

# 6) configurar passwd e resolv dentro da jail (mínimo)
RUN echo "root:x:0:0:root:/root:/bin/bash" > /opt/jail/etc/passwd && \
    echo "nameserver 1.1.1.1" > /opt/jail/etc/resolv.conf

# 7) script de entrada: monta e entra na jail (heredoc corretamente formado)
RUN cat > /usr/local/bin/start-jail <<'EOF'
#!/bin/bash
set -euo pipefail
echo "[INFO] Preparando /opt/jail..."
mkdir -p /opt/jail/proc /opt/jail/dev /opt/jail/sys /opt/jail/tmp

# tenta montar pseudo-filesystems (pode falhar sem CAP_SYS_ADMIN)
mount -t proc proc /opt/jail/proc 2>/dev/null || true
mount --rbind /dev /opt/jail/dev 2>/dev/null || true
mount --rbind /sys /opt/jail/sys 2>/dev/null || true

echo "[INFO] Entrando na jail..."
exec chroot /opt/jail /bin/bash
EOF

RUN dos2unix /usr/local/bin/start-jail && chmod +x /usr/local/bin/start-jail

CMD ["/usr/local/bin/start-jail"]
