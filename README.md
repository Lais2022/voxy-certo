# Voxy Backend

Backend modular para Lovable, WhatsApp e CRM próprio com FastAPI, Redis, PostgreSQL e Nginx. Inclui APIs para controle do agente e scripts.

## Como começar

1. Configure o Ubuntu 22.04:
   ```bash
   bash scripts/setup_ubuntu.sh
   ```
2. Copie o `.env.example` para `.env` e ajuste as variáveis.
3. Suba os serviços:
   ```bash
   bash scripts/deploy.sh
   ```

Consulte o guia completo em [`docs/SETUP.md`](docs/SETUP.md).
