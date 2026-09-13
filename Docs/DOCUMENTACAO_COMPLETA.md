# 📘 Documentação Completa do Projeto
## DIO + IBM Bob — Plataforma de Trilhas de Aprendizagem

> **Idioma:** Português (Brasil)
> **Versão:** 1.0.0 — Julho/2025
> **Repositório:** `projeto_final_dio_formacao_bob`

---

## Índice

1. [Visão Geral do IBM Bob](#1-visão-geral-do-ibm-bob)
2. [Estrutura do Projeto](#2-estrutura-do-projeto)
3. [Configuração do Ambiente](#3-configuração-do-ambiente)
4. [Slash Commands](#4-slash-commands)
5. [MCP Server](#5-mcp-server)
6. [Módulo Python — src/commands.py](#6-módulo-python--srccommandspy)
7. [Testes Unitários](#7-testes-unitários)
8. [Dados do Projeto](#8-dados-do-projeto)
9. [Todos os Prompts Utilizados](#9-todos-os-prompts-utilizados)
10. [Dicas de Uso do IBM Bob](#10-dicas-de-uso-do-ibm-bob)
11. [Insights para Futuros Profissionais](#11-insights-para-futuros-profissionais)

---

## 1. Visão Geral do IBM Bob

### O que é o IBM Bob?

O **IBM Bob** é um parceiro de IA para o ciclo de vida completo de desenvolvimento de software (SDLC — Software Development Lifecycle). Ele aumenta seus fluxos de trabalho existentes e ajuda você a entender, planejar, melhorar e trabalhar com confiança em bases de código reais — ao mesmo tempo em que oferece insights proativos que mantêm você no controle em cada etapa.

> *"IBM Bob is an AI SDLC partner that augments your existing workflows and helps you understand, plan, improve, and work confidently with real codebases while offering proactive insights that keep you in control every step."*
> — Documentação oficial IBM Bob

### Como o IBM Bob funciona?

O Bob utiliza grandes modelos de linguagem (LLMs) para entender suas solicitações e traduzi-las em ações. Ele pode:

- Ler e escrever arquivos no seu projeto
- Executar comandos no terminal
- Navegar na web (quando habilitado)
- Usar ferramentas externas via **Model Context Protocol (MCP)**

Você interage com o Bob por meio de uma interface de chat, onde fornece instruções e revisa as ações propostas antes de aprová-las.

### O que o IBM Bob pode fazer?

| Capacidade | Descrição |
|---|---|
| Geração de código | Cria código a partir de descrições em linguagem natural |
| Refatoração | Melhora a estrutura e qualidade do código existente |
| Correção de bugs | Identifica e corrige erros no código |
| Documentação | Escreve documentação técnica e comentários |
| Explicação de código | Explica o que o código faz em linguagem simples |
| Q&A sobre codebase | Responde perguntas sobre o projeto |
| Automação de tarefas | Automatiza tarefas repetitivas de desenvolvimento |
| Criação de projetos | Cria novos arquivos, pastas e estruturas de projeto |

### Seleção automática de modelos

O Bob seleciona automaticamente o modelo de linguagem mais adequado para cada tarefa, considerando:

- **Complexidade da tarefa** — Tarefas simples usam modelos mais rápidos e econômicos
- **Capacidades necessárias** — Tarefas especializadas são direcionadas a modelos com pontos fortes específicos
- **Tamanho do contexto** — Bases de código grandes podem requerer modelos com janelas de contexto estendidas
- **Otimização de custos** — Equilibra desempenho com uso eficiente de recursos

### Privacidade dos dados

- ✅ A IBM **não usa** seus prompts para treinamento de dados
- ✅ Os prompts são armazenados temporariamente apenas para melhorar o desempenho de inferência
- ✅ A IBM **não coleta** trechos de código ou sessões de chat
- ℹ️ A IBM coleta dados de uso de tokens para fins de faturamento

---

### Modos de Operação

O Bob possui **três modos nativos** e suporte a modos customizados:

#### 🤖 Modo Agent (Agente)
**Finalidade:** Escrever, modificar e refatorar código com precisão.
**Use quando:** Implementar funcionalidades, corrigir bugs ou fazer melhorias no código.

```
Exemplo de prompt no modo Agent:
"Crie uma função Python que leia um arquivo JSON e retorne uma lista filtrada por critério."
```

#### 📋 Modo Plan (Planejamento)
**Finalidade:** Planejar e projetar antes da implementação.
**Use quando:** Precisar de arquitetura, especificações técnicas ou planejamento de soluções complexas.

```
Exemplo de prompt no modo Plan:
"Planeje a arquitetura de um sistema de notificações para esta aplicação."
```

#### ❓ Modo Ask (Perguntas)
**Finalidade:** Obter respostas e explicações sobre o código.
**Use quando:** Precisar de explicações ou informações sem modificar arquivos.

```
Exemplo de prompt no modo Ask:
"O que faz a função buscar_trilha em src/commands.py?"
```

---

### Janela de Contexto

O Bob possui uma janela de contexto de **270.000 tokens** por tarefa. Isso inclui histórico de conversa, conteúdo de arquivos e saída de ferramentas.

**Boas práticas para gerenciar o contexto:**
- Inicie novas tarefas com objetivos específicos
- Evite enviar toda a base de código de uma vez
- Use referências diretas a arquivos para fornecer contexto direcionado
- Divida tarefas complexas em subtarefas menores e focadas

---

### Arquivo `.bobignore`

O arquivo `.bobignore` (na raiz do projeto) define quais arquivos e pastas o Bob deve **ignorar** ao analisar o projeto. Funciona de forma similar ao `.gitignore`.

- O Bob monitora o arquivo ativamente — mudanças são recarregadas automaticamente
- O próprio `.bobignore` é sempre ignorado implicitamente (o Bob não pode alterar suas próprias regras de acesso)
- Protege informações sensíveis e evita análise de artefatos de build desnecessários

---

### Arquivo `AGENTS.md`

O `AGENTS.md` funciona como documentação de onboarding para o Bob. Ele fornece tudo que o Bob precisa para entender a estrutura e convenções do projeto. Pode ser gerado automaticamente com o comando `/init`.

**Componentes típicos:**
- Visão geral e propósito do projeto
- Estrutura de diretórios e localizações de arquivos-chave
- Stack de tecnologia e dependências
- Padrões arquiteturais e convenções
- Fluxos de trabalho de desenvolvimento

**Arquivos AGENTS.md por modo:**
```
.bob/
├── rules-agent/AGENTS-agent.md    ← regras para o modo Agent
├── rules-plan/AGENTS-plan.md      ← regras para o modo Plan
└── rules-ask/AGENTS-ask.md        ← regras para o modo Ask
```

---

## 2. Estrutura do Projeto

```
projeto_final_dio_formacao_bob/
│
├── 📄 Bob.ignore                       ← arquivos/pastas ignorados pelo Bob
├── 📄 README.md                        ← documentação geral do repositório
├── 📄 hello-world.md                   ← arquivo de boas-vindas
├── 📄 resultados_testes.txt            ← relatório de execução dos testes
├── 📄 run_inline.py                    ← runner de testes sem dependências externas
│
├── 📁 .bob/                            ← configurações locais do Bob (escopo do projeto)
│   ├── 📄 mcp.json                     ← registro do MCP Server no Bob
│   └── 📁 commands/                    ← slash commands locais
│       ├── 📄 trilha.md                → /trilha
│       ├── 📄 desafio.md               → /desafio
│       └── 📄 certificado.md           → /certificado
│
├── 📁 src/                             ← lógica de negócio Python
│   └── 📄 commands.py                  ← funções dos 3 comandos
│
├── 📁 tests/                           ← testes unitários
│   ├── 📄 test_commands.py             ← 46 casos de teste
│   └── 📄 runner.py                    ← runner com coverage
│
├── 📁 Data/                            ← dados do projeto
│   ├── 📄 Trilhas.json                 ← 5 trilhas completas
│   ├── 📁 certificados/                ← certificados gerados
│   │   ├── 📄 certificado_joao_silva_python.md
│   │   └── 📄 certificado_aluno_java.md
│   └── 📁 desafios/                    ← desafios gerados
│       └── 📄 desafio_java_intermediario.md
│
├── 📁 Mcp/                             ← MCP Server TypeScript
│   ├── 📄 package.json
│   ├── 📄 tsconfig.json
│   ├── 📄 README.md
│   └── 📁 src/
│       └── 📄 index.ts                 ← implementação do servidor MCP
│
├── 📁 Comandos/                        ← (reservado para expansão)
├── 📁 Cs/                              ← (reservado para expansão)
├── 📁 Dio-Explorer/                    ← (reservado para expansão)
├── 📁 Docs/                            ← (reservado para expansão)
└── 📁 Msp/                             ← (reservado para expansão)
```

---

## 3. Configuração do Ambiente

### Pré-requisitos

| Ferramenta | Versão mínima | Finalidade |
|---|---|---|
| Python | 3.10+ | Lógica dos comandos e testes |
| Node.js | 18+ | MCP Server TypeScript |
| npm | 9+ | Gerenciador de pacotes Node |
| IBM Bob IDE | Atual | Interface principal |

### Instalação do MCP Server

```bash
cd projeto_final_dio_formacao_bob/Mcp
npm install
npm run build
```

### Executar testes Python

```bash
# Com pytest (recomendado):
pip install pytest coverage
python -m pytest tests/test_commands.py -v

# Com relatório de cobertura:
python -m coverage run -m pytest tests/test_commands.py
python -m coverage report -m

# Sem dependências externas:
python run_inline.py
```

### Registro do MCP Server no Bob

O arquivo `.bob/mcp.json` já está configurado. O Bob carrega automaticamente ao abrir o projeto:

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

> ⚠️ Ajuste o caminho absoluto em `args` para o seu sistema operacional e usuário.

---

## 4. Slash Commands

Slash commands são arquivos Markdown em `.bob/commands/` que o Bob executa como instruções quando invocados com `/nome-do-comando` no chat.

**Escopo:** Local ao projeto (visíveis apenas neste repositório).

---

### `/trilha <tecnologia>`

**Arquivo:** [`.bob/commands/trilha.md`](.bob/commands/trilha.md)

**O que faz:** Lê o `Data/Trilhas.json`, localiza a trilha da tecnologia informada (sem distinção de maiúsculas) e exibe o plano de estudos completo com todos os módulos e tópicos formatados em Markdown.

**Parâmetros:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `tecnologia` | string | ✅ | Nome da tecnologia (Python, JavaScript, Java, SQL, React) |

**Exemplos de uso:**
```
/trilha Java
/trilha python
/trilha REACT
/trilha SQL
```

**Saída esperada:**
```markdown
# 📚 Trilha de Estudos — Java
**Nível:** Iniciante ao Avançado
**Descrição:** Aprenda Java com foco em POO...

## Módulos da Trilha
**Módulo 1 — Fundamentos de Java**
  1. Sintaxe e tipos primitivos
  2. Operadores
  ...
```

**Comportamento quando tecnologia não existe:** Lista todas as trilhas disponíveis no arquivo JSON.

---

### `/desafio <tecnologia> <nivel>`

**Arquivo:** [`.bob/commands/desafio.md`](.bob/commands/desafio.md)

**O que faz:** Gera um desafio de código aleatório com enunciado, requisitos, exemplos de entrada/saída, restrições e uma dica para a tecnologia e nível informados.

**Parâmetros:**
| Parâmetro | Tipo | Obrigatório | Valores aceitos |
|---|---|---|---|
| `tecnologia` | string | ✅ | Qualquer tecnologia (Java, Python, JavaScript...) |
| `nivel` | string | ✅ | `iniciante`, `intermediario`, `avancado` |

**Exemplos de uso:**
```
/desafio Python iniciante
/desafio Java intermediario
/desafio JavaScript avancado
/desafio React intermediario
```

**Estrutura da saída:**
```markdown
# ⚔️ Desafio de Código — Java · Nível Intermediário
## Descrição
## Requisitos
## Exemplo de Entrada e Saída
## Restrições
## Dica
```

**Escala de dificuldade:**

| Nível | Tipo de problema |
|---|---|
| `iniciante` | Loops, condicionais, funções básicas, strings |
| `intermediario` | Estruturas de dados, algoritmos, POO, recursão |
| `avancado` | Otimização, design patterns, concorrência, arquitetura |

---

### `/certificado <nome> <tecnologia>`

**Arquivo:** [`.bob/commands/certificado.md`](.bob/commands/certificado.md)

**O que faz:** Gera um certificado fictício em Markdown com o nome do usuário e a trilha concluída. Salva automaticamente em `Data/certificados/` e exibe o conteúdo na conversa.

**Parâmetros:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `nome` | string | ✅ | Nome completo do aluno |
| `tecnologia` | string | ✅ | Tecnologia da trilha concluída |

**Exemplos de uso:**
```
/certificado "João Silva" Python
/certificado "Maria Souza" React
/certificado "Carlos Lima" Java
```

**Arquivo gerado:** `Data/certificados/certificado_{nome}_{tecnologia}.md`

**Conteúdo do certificado:**
- Nome do aluno em maiúsculas
- Trilha concluída
- Lista dos módulos (lida do `Trilhas.json`)
- Data de emissão
- Carga horária estimada
- Nível da trilha
- ID único no formato: `DIO-BOB-{AAAAMMDD}-{TECH}{4 dígitos}`

---

## 5. MCP Server

### O que é o MCP?

O **Model Context Protocol (MCP)** é um protocolo aberto que permite ao Bob se conectar a servidores externos como bancos de dados, APIs ou scripts customizados, estendendo suas capacidades além das funcionalidades nativas.

Os servidores MCP fornecem ao Bob:
- **Descoberta de ferramentas:** Acesso a tools disponíveis com suas descrições e parâmetros
- **Invocação de ferramentas:** Capacidade de chamar tools específicas com argumentos
- **Acesso a recursos:** Capacidade de ler dados de recursos específicos

### Localização

```
Mcp/
├── src/index.ts        ← implementação TypeScript do servidor
├── package.json        ← dependências e scripts
├── tsconfig.json       ← configuração TypeScript
└── README.md           ← documentação do servidor
```

### Ferramentas expostas

| Tool MCP | Parâmetros | Descrição |
|---|---|---|
| `trilha` | `tecnologia: string` | Retorna plano de estudos completo |
| `desafio` | `tecnologia: string`, `nivel: enum` | Gera desafio de código |
| `certificado` | `nome: string`, `tecnologia: string` | Gera e salva certificado |

### Transportes suportados

#### stdio — Uso local com IBM Bob

O Bob inicia o servidor como processo filho. Já configurado em `.bob/mcp.json`.

```bash
node Mcp/build/index.js
```

#### HTTP — Conexões remotas via API

Ideal para equipes que desejam compartilhar o servidor via rede.

```bash
# Porta padrão 3333
MCP_TRANSPORT=http node Mcp/build/index.js

# Porta customizada
MCP_TRANSPORT=http PORT=8080 node Mcp/build/index.js
```

**Endpoints disponíveis:**

| Endpoint | Método | Descrição |
|---|---|---|
| `GET /health` | GET | Health check — `{"status":"ok"}` |
| `POST /mcp` | POST | Protocolo MCP Streamable HTTP |

**Registro no Bob via URL remota:**
```json
{
  "mcpServers": {
    "dio-bob-remote": {
      "url": "http://localhost:3333/mcp"
    }
  }
}
```

### Variáveis de ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `MCP_TRANSPORT` | `stdio` | Transporte: `stdio` ou `http` |
| `PORT` | `3333` | Porta HTTP |
| `ALLOWED_ORIGIN` | `*` | Cabeçalho CORS |

---

## 6. Módulo Python — src/commands.py

### Funções públicas

| Função | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `buscar_trilha(tecnologia, caminho_json)` | str, str | `dict \| None` | Busca trilha no JSON (case-insensitive) |
| `listar_tecnologias(caminho_json)` | str | `list[str]` | Lista todas as tecnologias cadastradas |
| `formatar_plano_estudos(trilha)` | dict | str | Formata trilha como Markdown |
| `gerar_desafio(tecnologia, nivel)` | str, str | str | Retorna desafio formatado em Markdown |
| `gerar_certificado(nome, tecnologia, caminho_json, data_emissao, id_certificado)` | str, str, str, str?, str? | str | Gera conteúdo do certificado |
| `salvar_arquivo(conteudo, caminho)` | str, str | bool | Salva arquivo, criando diretórios |
| `parse_frontmatter(texto)` | str | dict | Extrai campos YAML do frontmatter `---` |

### Banco de desafios embutido

O módulo inclui um dicionário `DESAFIOS` com desafios para:
- **Java:** iniciante, intermediario, avancado
- **Python:** iniciante, intermediario, avancado

Cada desafio contém: título, descrição, requisitos, exemplos de entrada/saída e dica.

---

## 7. Testes Unitários

### Arquivo: `tests/test_commands.py`

**46 casos de teste** organizados em 7 classes:

| Classe | Testes | O que cobre |
|---|---|---|
| `TestBuscarTrilha` | 7 | Busca por Java (exato, case-insensitive), Python, inexistente, arquivo ausente, módulos |
| `TestListarTecnologias` | 3 | Lista completa, contém Java/Python, arquivo ausente |
| `TestFormatarPlanoEstudos` | 7 | Cabeçalho, nível, módulos, tópicos, trilha None, encorajamento |
| `TestGerarDesafio` | 11 | Java iniciante/intermediario/avancado, case-insensitive, inválidos, seções |
| `TestGerarCertificado` | 9 | Nome maiúsculo, tecnologia, data, ID, módulos, carga, fallback, cabeçalho |
| `TestSalvarArquivo` | 3 | Criação, dirs aninhados, caminho inválido |
| `TestParseFrontmatter` | 5 | description, argument-hint, sem `---`, sem fechamento, vazio |

### Resultados

| Métrica | Valor |
|---|---|
| Total de testes | 46 |
| Aprovados | 46 ✅ |
| Falhas/Erros | 0 |
| Taxa de aprovação | **100%** |
| Cobertura de código | **84%** (meta: ≥70%) |

### Como executar

```bash
# Opção 1 — pytest com cobertura (recomendado)
pip install pytest coverage
python -m pytest tests/test_commands.py -v
python -m coverage run -m pytest tests/test_commands.py
python -m coverage report -m

# Opção 2 — sem dependências externas
python run_inline.py

# Opção 3 — runner com relatório automático
python tests/runner.py
```

O resultado é salvo automaticamente em [`resultados_testes.txt`](resultados_testes.txt).

---

## 8. Dados do Projeto

### Data/Trilhas.json

Contém **5 trilhas completas** de estudo:

| Tecnologia | Nível | Módulos | Carga estimada |
|---|---|---|---|
| Python | Iniciante ao Avançado | 7 | 70h |
| JavaScript | Iniciante ao Avançado | 6 | 60h |
| Java | Iniciante ao Avançado | 7 | 70h |
| SQL | Iniciante ao Avançado | 6 | 60h |
| React | Intermediário ao Avançado | 7 | 70h |

### Data/certificados/

Certificados gerados pela plataforma:

| Arquivo | Aluno | Trilha | Data |
|---|---|---|---|
| `certificado_joao_silva_python.md` | João Silva | Python | 09/07/2025 |
| `certificado_aluno_java.md` | Aluno DIO | Java | 09/07/2025 |

### Data/desafios/

| Arquivo | Tecnologia | Nível |
|---|---|---|
| `desafio_java_intermediario.md` | Java | Intermediário |

---

## 9. Todos os Prompts Utilizados

Abaixo estão registrados todos os prompts enviados ao Bob durante a construção deste projeto, na ordem em que foram utilizados.

---

### Prompt 1 — Criar Bob.ignore

```
Quero que, na raiz do projeto recém clonado, voce crie um arquivo Bob.ignore,
quero que ele ignore as pastas, módulos, arquivos, data cache, progresso e
certificados emitidos, docs salvos, e quaisquer arquivos com extensão tmp
```

**O que foi criado:** [`Bob.ignore`](Bob.ignore) na raiz do projeto com seções para
`node_modules/`, `.cache/`, `progress/`, `certificados/`, `docs/`, `*.tmp` e outros.

---

### Prompt 2 — Criar os 3 slash commands

```
Bob, crie agora um slash command chamado /trilha que recebe o nome de uma
tecnologia e retorna a partir do arquivo Trilhas.json um plano de estudos
forma com os módulos daquela trilha. Depois crie outro slash command chamado
/desafio que gere um desafio de código aleatório baseado no nível e tecnologia
escolhido pelo usuário e por fim um ultimo slash command chamado /certificado,
que gera um certificado fictício em markdown com o nome do usuário e a trilha
por ele concluida
```

**O que foi criado:**
- `Data/Trilhas.json` populado com 5 trilhas
- `.bob/commands/trilha.md`
- `.bob/commands/desafio.md`
- `.bob/commands/certificado.md`

---

### Prompt 3 — Executar /certificado

```
/certificado "João Silva" Python
```

**O que foi gerado:** `Data/certificados/certificado_joao_silva_python.md`

---

### Prompt 4 — Executar /desafio

```
/desafio ibmbob intermediario
```

**O que foi gerado:** Desafio de nível intermediário — parser de slash commands do Bob.

---

### Prompt 5 — Reconfirmar slash commands locais

```
bob, gostaria que voce mostre em forma de arvore tudo o que existe dentro de
nosso recém clonado repositorio
```

**O que foi feito:** Exibição da árvore completa do repositório.

---

### Prompt 6 — Criar testes unitários

```
bob, nesse momento, construir dentro da pasta de mcp a forma como um mcp server,
para que futuras pessoas possam se conectar via https ou sm ou via api,
use a pasta mcp para isso.
```

**O que foi criado:**
- `src/commands.py` — lógica Python dos 3 comandos
- `tests/test_commands.py` — 46 casos de teste
- `tests/runner.py` — runner com coverage
- `run_inline.py` — runner sem dependências
- `Data/desafios/desafio_java_intermediario.md`
- `Data/certificados/certificado_aluno_java.md`
- `resultados_testes.txt` — relatório

---

### Prompt 7 — Criar MCP Server

```
bob, nesse momento, construir dentro da pasta de mcp a forma como um mcp server,
para que futuras pessoas possam se conectar via https ou sm ou via api,
use a pasta mcp para isso.
```

**O que foi criado:**
- `Mcp/package.json`
- `Mcp/tsconfig.json`
- `Mcp/src/index.ts` — servidor completo com tools trilha, desafio, certificado
- `Mcp/README.md`
- `.bob/mcp.json` — registro do servidor no Bob

---

### Prompt 8 — Documentar o projeto

```
bob, gostaria que voce documentasse todo o projeto feito ate o momento,
com todos os prompts usados, modos de uso, dicas de uso, insights para
futuros profissionais que vao aprender conosco. peço que adicione uma
documentação de visão geral do IBM Bob, use o site https://bob.ibm.com/pt/docs/ide,
escreva no idioma português brasil
```

**O que foi criado:** Este arquivo — `Docs/DOCUMENTACAO_COMPLETA.md`.

---

## 10. Dicas de Uso do IBM Bob

### 💬 Escreva prompts específicos

> *"The more specific your request, the better the results."* — Documentação IBM Bob

| ❌ Vago | ✅ Específico |
|---|---|
| "Crie uma função" | "Crie uma função Python que receba uma lista de dicionários e retorne apenas os que têm o campo 'ativo' igual a True" |
| "Corrija o bug" | "A função buscar_trilha retorna None mesmo quando a tecnologia existe — corrija a comparação case-insensitive na linha 28" |
| "Faça uma tabela" | "Crie um componente React com TypeScript que exiba uma tabela ordenável de usuários com colunas nome, email e status" |

---

### 🎯 Use o modo certo para cada tarefa

```
Antes de implementar → use Plan para arquitetura e decisões
Durante a implementação → use Agent para escrever código
Para entender o código → use Ask para perguntas sem modificar arquivos
```

---

### 📁 Use o Bob.ignore para manter o contexto limpo

Configure o `.bobignore` para excluir:
- Pastas de dependências (`node_modules/`, `.venv/`)
- Artefatos de build (`dist/`, `build/`)
- Arquivos temporários (`*.tmp`, `.cache/`)
- Dados sensíveis (chaves de API, `.env`)

Isso mantém a janela de contexto focada no que realmente importa.

---

### 📝 Mantenha um AGENTS.md atualizado

O `AGENTS.md` é carregado automaticamente em cada nova conversa. Inclua:
- Visão geral do projeto
- Stack de tecnologia
- Convenções de nomenclatura
- Comandos de teste e build
- Padrões arquiteturais

Execute `/init` para gerar automaticamente. Reexecute após mudanças significativas.

---

### 🔧 Slash Commands — boas práticas

1. **Mantenha em `.bob/commands/`** para escopo local (apenas neste projeto)
2. **Use frontmatter YAML** com `description` e `argument-hint` para aparecerem no menu
3. **Use `$1`, `$2`** para parâmetros posicionais no corpo do comando
4. **Seja descritivo** no `description` — aparece no menu de autocomplete do Bob
5. **Compartilhe com a equipe** via controle de versão (Git)

---

### 🔌 MCP Server — quando usar

Use um servidor MCP customizado quando:
- Precisar de **integração reutilizável** com uma API ou fonte de dados
- A lógica for complexa demais para um slash command
- Múltiplos projetos precisarem das mesmas ferramentas
- Quiser expor ferramentas para **outros membros da equipe** via HTTP

---

### 🪟 Gerencie a janela de contexto (270k tokens)

- **Inicie novas tarefas** para cada funcionalidade diferente
- **Não cole arquivos inteiros** — referencie pelo caminho
- **Divida tarefas complexas** em etapas menores
- **Mantenha AGENTS.md e regras customizadas curtos** — apenas o essencial
- **Desconecte servidores MCP** que não estiver usando no momento

---

## 11. Insights para Futuros Profissionais

### 🧠 O IBM Bob como parceiro, não substituto

O Bob não substitui o desenvolvedor — ele **amplifica** suas capacidades. A chave está em:
- **Revisar sempre** as alterações propostas antes de aprovar
- **Entender o código gerado** — não apenas aceitar cegamente
- **Usar o Bob como ferramenta de aprendizado** — peça explicações, não apenas soluções

---

### 🏗️ A arquitetura deste projeto como modelo

Este projeto demonstra um padrão reutilizável para qualquer plataforma de aprendizagem com Bob:

```
Dados estruturados (JSON)
    ↓
Lógica de negócio (Python/TypeScript)
    ↓
Slash Commands (interface rápida para usuário final)
    ↓
MCP Server (interface programática para integrações)
    ↓
Testes Unitários (garantia de qualidade)
    ↓
Documentação (conhecimento transferível)
```

---

### 📐 Boas práticas aplicadas no projeto

| Prática | Como foi aplicada |
|---|---|
| **Separação de responsabilidades** | Lógica em `src/commands.py`, interface em `.bob/commands/`, servidor em `Mcp/` |
| **Testes antes de integrar** | 46 testes cobrindo 84% do código antes de qualquer integração |
| **Documentação como código** | Slash commands em Markdown, MCP com README |
| **Escopo de configuração** | `.bob/commands/` e `.bob/mcp.json` são locais ao projeto |
| **Dados separados de lógica** | `Data/Trilhas.json` é independente da lógica de apresentação |

---

### 🚀 Próximos passos sugeridos

1. **Adicionar mais trilhas** ao `Data/Trilhas.json` (TypeScript, Go, Rust, DevOps)
2. **Expandir o banco de desafios** em `src/commands.py` para todas as tecnologias
3. **Criar um modo customizado** `modo-tutor` no Bob para experiências de tutoria
4. **Adicionar autenticação** ao MCP Server HTTP (API key via variável de ambiente)
5. **Criar slash command `/progresso`** que registre e exiba o progresso do aluno
6. **Deploy do MCP Server** em nuvem (IBM Cloud, Railway, Render) para acesso remoto da equipe
7. **Integrar com banco de dados** para persistir progresso, certificados e desafios resolvidos
8. **Criar AGENTS.md** para que o Bob entenda o projeto automaticamente em novas sessões

---

### 💡 Lições aprendidas

> **"Slash commands transformam prompts repetitivos em ferramentas de time."**
> Com apenas um arquivo Markdown em `.bob/commands/`, uma instrução complexa vira
> um comando de uma linha que qualquer membro da equipe pode usar.

> **"MCP é a ponte entre o Bob e o mundo real."**
> Enquanto slash commands são ótimos para fluxos de conversa, servidores MCP
> permitem que o Bob acesse dados reais, APIs e sistemas externos de forma
> estruturada e reutilizável.

> **"Testes não são opcionais — são documentação executável."**
> Os 46 testes deste projeto documentam o comportamento esperado de cada função
> com mais precisão do que qualquer comentário poderia.

> **"O contexto é rei."**
> Quanto mais específico e contextualizado for o seu prompt, melhor será a
> resposta do Bob. Mencione arquivos, funções, comportamentos esperados.

---

## Referências

- [IBM Bob — Documentação Oficial](https://bob.ibm.com/pt/docs/ide)
- [IBM Bob — Slash Commands](https://bob.ibm.com/pt/docs/ide/features/slash-commands)
- [IBM Bob — MCP](https://bob.ibm.com/pt/docs/ide/configuration/mcp/mcp-in-bob)
- [IBM Bob — Modos de Operação](https://bob.ibm.com/pt/docs/ide/features/modes)
- [IBM Bob — AGENTS.md e Regras](https://bob.ibm.com/pt/docs/ide/configuration/rules)
- [IBM Bob — Gerenciamento de Contexto](https://bob.ibm.com/pt/docs/ide/core-concepts/context-window-management)
- [Model Context Protocol — Especificação](https://modelcontextprotocol.io)
- [DIO — Digital Innovation One](https://www.dio.me)

---

*Documentação gerada com IBM Bob — Julho/2025*
*Projeto Final — Formação IBM Bob na DIO*
