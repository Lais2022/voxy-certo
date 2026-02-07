#!/usr/bin/env bash
set -euo pipefail

# Script para preparar Ubuntu 22.04 com Docker, UFW e Fail2ban.
# Execute como root: sudo bash scripts/setup_ubuntu.sh

apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release ufw fail2ban

install -m 0755 -d /etc/apt/keyrings
if [ ! -f /etc/apt/keyrings/docker.gpg ]; then
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg
fi

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Configuração básica do firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

systemctl enable docker
systemctl start docker
systemctl enable fail2ban
systemctl start fail2ban

printf "\nSetup concluído. Reinicie o servidor se necessário.\n"
