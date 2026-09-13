# DIO Bob — MCP Server

Servidor MCP que expõe as ferramentas do projeto DIO + IBM Bob como tools consumíveis
por qualquer cliente MCP — incluindo o IBM Bob, Cursor, VS Code e conexões HTTP remotas.

## Ferramentas disponíveis

| Tool | Parâmetros | Descrição |
|---|---|---|
| `trilha` | `tecnologia: string` | Retorna o plano de estudos completo de uma trilha |
| `desafio` | `tecnologia: string`, `nivel: iniciante\|intermediario\|avancado` | Gera um desafio de código |
| `certificado` | `nome: string`, `tecnologia: string` | Gera e salva um certificado fictício em Markdown |

---

## Instalação

```bash
cd Mcp
npm install
npm run build
```

Pré-requisito: **Node.js >= 18**

---

## Modos de transporte

### 1. stdio — uso local com IBM Bob (padrão)

O modo stdio é o padrão. O IBM Bob inicia o servidor como processo filho e se comunica via stdin/stdout.

```bash
node build/index.js
```

Registre no Bob adicionando ao `.bob/mcp.json` do projeto (veja seção abaixo).

---

### 2. HTTP — conexões remotas via API

Ideal para equipes que querem compartilhar o servidor via rede ou expô-lo como API REST/MCP.

```bash
# Porta padrão: 3333
MCP_TRANSPORT=http node build/index.js

# Porta customizada
MCP_TRANSPORT=http PORT=8080 node build/index.js

# Restringir origem (CORS)
MCP_TRANSPORT=http PORT=3333 ALLOWED_ORIGIN=https://meuapp.com node build/index.js
```

Endpoints disponíveis:

| Endpoint | Método | Descrição |
|---|---|---|
| `/health` | GET | Health check — retorna `{"status":"ok"}` |
| `/mcp` | POST | Endpoint MCP Streamable HTTP (protocolo MCP sobre HTTP) |

#### Exemplo de health check

```bash
curl http://localhost:3333/health
# {"status":"ok","server":"dio-bob-mcp-server","version":"1.0.0"}
```

#### Registrar no Bob via HTTP (remoto)

No `.bob/mcp.json` do projeto:

```json
{
  "mcpServers": {
    "dio-bob-remote": {
      "url": "http://localhost:3333/mcp"
    }
  }
}
```

---

## Registro local no IBM Bob (stdio)

Crie ou edite `.bob/mcp.json` na raiz do projeto:

```json
{
  "mcpServers": {
    "dio-bob": {
      "command": "node",
      "args": ["C:/Users/Crisci/Documents/projeto_final_dio_formacao_bob/Mcp/build/index.js"]
    }
  }
}
```

> Ajuste o caminho absoluto de `args` para o seu ambiente.

Após salvar, o Bob recarrega automaticamente e as tools `trilha`, `desafio` e `certificado`
ficam disponíveis para qualquer conversa neste projeto.

---

## Exemplos de uso no Bob (após registro)

```
Use a tool trilha com tecnologia=Java
Use a tool desafio com tecnologia=python e nivel=intermediario
Use a tool certificado com nome="Maria Souza" e tecnologia=React
```

---

## Estrutura do projeto

```
Mcp/
├── src/
│   └── index.ts        ← implementação do servidor
├── build/              ← gerado por: npm run build
│   └── index.js
├── package.json
├── tsconfig.json
└── README.md
```

---

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `MCP_TRANSPORT` | `stdio` | Transporte: `stdio` ou `http` |
| `PORT` | `3333` | Porta HTTP (apenas quando `MCP_TRANSPORT=http`) |
| `ALLOWED_ORIGIN` | `*` | Cabeçalho CORS `Access-Control-Allow-Origin` |

---

## Desenvolvimento

```bash
# Compilar e observar mudanças
npm run dev

# Testar em modo stdio (simula o Bob)
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | node build/index.js
```
