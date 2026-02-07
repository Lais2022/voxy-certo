# Guia de implantação (Ubuntu 22.04 LTS)

Este guia descreve uma implantação segura e escalável para o backend de automações (Lovable, WhatsApp, Kommo/ZapSuite) usando Docker.

## 0) Passo a passo bem simples (sem linguagem técnica)

### Parte A — No site da Hostinger (VPS)
1. Entre no site da Hostinger e faça login.
2. Vá em **Hospedagem** → **VPS**.
3. Clique no seu VPS e procure a opção **Acessar via SSH**.
4. Copie os dados de acesso (IP, usuário e senha).
5. Abra um terminal no seu computador:
   - **Windows**: abra o app **PowerShell**.
   - **Mac/Linux**: abra o app **Terminal**.
6. Conecte no VPS com este comando (cole e aperte Enter):
   ```bash
   ssh root@76.13.234.19
   ```
7. Quando pedir senha, cole a senha do VPS (não aparece na tela, é normal) e aperte Enter.

### Parte A2 — Como “mandar os arquivos” para o VPS (duas opções simples)
Você **não precisa enviar arquivo por arquivo**. O jeito mais fácil é baixar tudo direto do repositório no VPS.

**Opção 1 (recomendada): baixar tudo com `git clone`**
1. Depois de entrar no VPS (passos acima), rode:
   ```bash
   git clone <seu-repo> /opt/voxy
   ```
2. Pronto — todos os arquivos já ficam no VPS.

**Opção 2 (se você tem uma pasta no seu computador e quer enviar)**
1. No seu computador, abra o terminal na pasta do projeto.
2. Rode este comando (troque o caminho local):
   ```bash
   scp -r /caminho/da/pasta root@76.13.234.19:/opt/voxy
   ```
3. Aguarde terminar. Isso envia tudo para o VPS.

### Parte B — Dentro do VPS (copiar e colar comandos)
1. Copie e cole este comando para baixar o projeto:
   ```bash
   git clone <seu-repo> /opt/voxy
   ```
2. Copie e cole este comando para entrar na pasta do projeto:
   ```bash
   cd /opt/voxy
   ```
3. Copie e cole este comando para preparar o servidor:
   ```bash
   bash scripts/setup_ubuntu.sh
   ```
4. Copie e cole este comando para criar o arquivo de configuração:
   ```bash
   cp .env.example .env
   ```
5. Agora você precisa **editar o arquivo `.env`**:
   - Se você não sabe editar, use o comando:
     ```bash
     nano .env
     ```
   - Dentro do arquivo, troque os valores de:
     - `API_KEY`
     - `POSTGRES_PASSWORD`
     - `APP_BASE_URL`
   - Para salvar no nano: aperte **Ctrl + O**, depois **Enter**.
   - Para sair: **Ctrl + X**.
6. Copie e cole para ligar tudo:
   ```bash
   docker compose build
   docker compose up -d
   ```
7. Teste se está funcionando:
   ```bash
   curl http://localhost/health
   ```
   - Se aparecer `{"status":"ok"}`, está rodando.

### Parte C — No Lovable (onde você clica)
1. Entre no **Lovable** e abra o seu projeto.
2. Procure a área de **Integrações** ou **API**.
3. Adicione a **URL do seu backend** (exemplo):
   ```
   https://api.seudominio.com
   ```
4. Adicione o **Header** com sua chave:
   - Nome do header: `X-Api-Key`
   - Valor do header: o mesmo `API_KEY` do arquivo `.env`.
5. Quando o Lovable pedir **endpoint**, use um dos exemplos:
   - `GET /health`
   - `GET /dashboard/metrics`
   - `POST /crm/leads`
6. Salve e faça um teste de chamada. Se der erro, verifique:
   - Se o `API_KEY` está igual.
   - Se o domínio/URL está correto.

## 1) Visão geral da arquitetura

- **API FastAPI**: recebe webhooks, valida assinaturas e enfileira eventos.
- **Worker RQ**: processa tarefas em background.
- **PostgreSQL**: persiste dados de CRM, contatos e automações.
- **Redis**: fila e cache.
- **Nginx**: reverse proxy com logging básico.

```
Internet -> Nginx (80/443) -> API FastAPI (8000)
                         -> Redis (fila) -> Worker RQ
                         -> PostgreSQL
```

## 2) Pré-requisitos no VPS

1. Acesse o servidor (root):
   ```bash
   ssh root@76.13.234.19
   ```
2. Clone este repositório em `/opt/voxy` (ou outro diretório):
   ```bash
   git clone <seu-repo> /opt/voxy
   cd /opt/voxy
   ```
3. Rode o script de preparação:
   ```bash
   bash scripts/setup_ubuntu.sh
   ```

## 3) Configuração do ambiente

1. Copie o `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edite as variáveis críticas:
   - `API_KEY`: chave de autenticação para chamadas internas.
   - `LOVABLE_WEBHOOK_SECRET`, `KOMMO_WEBHOOK_SECRET`, `ZAPSUITE_WEBHOOK_SECRET`.
   - `POSTGRES_PASSWORD`.
   - `APP_BASE_URL` (seu domínio).

## 4) Subindo os serviços

```bash
docker compose build
docker compose up -d
```

Verifique:
```bash
curl http://localhost/health
```

## 5) Segurança mínima recomendada

- Firewall (UFW) já configurado no script:
  - libera **SSH**, **80** e **443**.
- Troque senhas e segredos do `.env`.
- Configure um domínio com TLS:
  - **Opção simples**: utilizar Cloudflare e proxyando o DNS para TLS gratuito.
  - **Opção completa**: instalar Certbot no host e montar certificados no Nginx.

## 6) Endpoints principais

- `GET /health` — healthcheck.
- `POST /webhooks/lovable`
- `POST /webhooks/kommo`
- `POST /webhooks/zapsuite`
- `GET /dashboard/metrics` — métricas do CRM.
- `POST /crm/leads` / `GET /crm/leads`
- `POST /crm/stages` / `GET /crm/stages`
- `POST /crm/deals` / `GET /crm/deals`
- `POST /crm/activities` / `GET /crm/activities`
- `GET /agent/state` / `PUT /agent/state` — pausa e controle do agente.
- `POST /agent/scripts` / `GET /agent/scripts` — scripts/customizações controladas.

Todos os endpoints aceitam o header `X-Api-Key` (configurável em `API_KEY_HEADER`).

## 7) Escalabilidade

- Aumente réplicas do worker:
  ```bash
  docker compose up -d --scale worker=3
  ```
- Para scale horizontal da API, considere usar um load balancer (ex: Nginx + upstreams ou HAProxy).

## 8) Backups

Use o script de backup:
```bash
BACKUP_DIR=/var/backups/voxy bash scripts/backup.sh
```

## 9) Customizações rápidas

- Ajuste assinatura HMAC em `app/services/*` para o padrão exato do seu provedor.
- Adicione integrações adicionais nos módulos de serviços.
- Para log avançado, conecte com Sentry via `SENTRY_DSN`.
- O CRM cria automaticamente uma etapa padrão usando `CRM_DEFAULT_STAGE`.
