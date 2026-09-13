#!/usr/bin/env node
/**
 * dio-bob-mcp-server — src/index.ts
 *
 * MCP Server que expõe as ferramentas do projeto DIO + IBM Bob:
 *   - trilha     : retorna plano de estudos a partir de Data/Trilhas.json
 *   - desafio    : gera um desafio de código por tecnologia e nível
 *   - certificado: gera e salva um certificado fictício em Markdown
 *
 * Transportes suportados:
 *   - stdio  (padrão)  — para uso direto com IBM Bob localmente
 *   - HTTP/SSE         — para conexões remotas via API (MCP_TRANSPORT=http)
 *
 * Uso:
 *   node build/index.js                        # stdio
 *   MCP_TRANSPORT=http PORT=3333 node build/index.js  # HTTP
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------
const __dirname = path.dirname(fileURLToPath(import.meta.url));
// O servidor vive em Mcp/build/, então sobe dois níveis para a raiz do projeto
const PROJECT_ROOT = path.resolve(__dirname, "..", "..");
const TRILHAS_JSON = path.join(PROJECT_ROOT, "Data", "Trilhas.json");
const CERTIFICADOS_DIR = path.join(PROJECT_ROOT, "Data", "certificados");

// ---------------------------------------------------------------------------
// Tipos
// ---------------------------------------------------------------------------
interface Modulo {
  ordem: number;
  titulo: string;
  topicos: string[];
}

interface Trilha {
  tecnologia: string;
  nivel: string;
  descricao: string;
  modulos: Modulo[];
}

interface TrilhasJson {
  trilhas: Trilha[];
}

// ---------------------------------------------------------------------------
// Helpers de domínio
// ---------------------------------------------------------------------------

function carregarTrilhas(): TrilhasJson | null {
  try {
    const raw = fs.readFileSync(TRILHAS_JSON, "utf-8");
    return JSON.parse(raw) as TrilhasJson;
  } catch {
    return null;
  }
}

function buscarTrilha(tecnologia: string): Trilha | undefined {
  const dados = carregarTrilhas();
  if (!dados) return undefined;
  return dados.trilhas.find(
    (t) => t.tecnologia.toLowerCase() === tecnologia.toLowerCase()
  );
}

function formatarPlano(trilha: Trilha): string {
  const linhas: string[] = [
    `# 📚 Trilha de Estudos — ${trilha.tecnologia}`,
    "",
    `**Nível:** ${trilha.nivel}`,
    `**Descrição:** ${trilha.descricao}`,
    "",
    "---",
    "",
    "## Módulos da Trilha",
    "",
  ];
  for (const mod of trilha.modulos) {
    linhas.push(`**Módulo ${mod.ordem} — ${mod.titulo}**`);
    mod.topicos.forEach((t, i) => linhas.push(`  ${i + 1}. ${t}`));
    linhas.push("");
  }
  linhas.push("---");
  linhas.push("🚀 Bons estudos! Cada módulo concluído é um passo a mais na sua jornada.");
  return linhas.join("\n");
}

// Banco de desafios embutido
const DESAFIOS: Record<string, Record<string, object>> = {
  java: {
    iniciante: {
      titulo: "Calculadora de Notas",
      descricao:
        "Leia 3 notas de um aluno, calcule a média e exiba APROVADO (≥7.0), RECUPERAÇÃO (5–6.9) ou REPROVADO (<5.0).",
      requisitos: ["Usar Scanner", "Calcular média com 2 casas decimais", "Exibir situação"],
      exemplos: [
        { entrada: "8.0, 7.5, 9.0", saida: "Média: 8.17 — APROVADO" },
        { entrada: "4.0, 6.0, 5.0", saida: "Média: 5.00 — RECUPERAÇÃO" },
      ],
      dica: "Use if/else if/else com as condições de média na ordem certa.",
    },
    intermediario: {
      titulo: "Gerenciador de Estudantes com Coleções",
      descricao:
        "Implemente Estudante + GerenciadorEstudantes usando List<Estudante>, Stream API e Lambda.",
      requisitos: [
        "Classe Estudante com getters/setters",
        "calcularMedia() com Stream.average()",
        "Listar ordenado por média decrescente",
        "Remover por nome case-insensitive",
      ],
      exemplos: [
        { entrada: "add('Ana', [8,9,7])", saida: "Ana adicionada. Média: 8.00" },
        { entrada: "remover('ana')", saida: "Ana removida com sucesso." },
      ],
      dica: "Explore Comparator.comparingDouble() e filter() com equalsIgnoreCase().",
    },
    avancado: {
      titulo: "Cache LRU Genérico Thread-Safe",
      descricao:
        "Implemente LRUCache<K,V> com get/put O(1) e evicção automática do item menos recentemente usado.",
      requisitos: [
        "get e put em O(1)",
        "Evicção automática ao atingir capacidade",
        "Thread-safe (synchronized ou ReentrantLock)",
      ],
      exemplos: [
        { entrada: "cache(2); put(1,'a'); put(2,'b'); get(1); put(3,'c')", saida: "get(2) → null" },
      ],
      dica: "LinkedHashMap com accessOrder=true e override de removeEldestEntry() resolve em poucas linhas.",
    },
  },
  python: {
    iniciante: {
      titulo: "Verificador de Palíndromo",
      descricao: "Dado uma string, verifique se ela é um palíndromo ignorando espaços e maiúsculas.",
      requisitos: ["Ignorar espaços e pontuação", "Case-insensitive", "Retornar True/False"],
      exemplos: [
        { entrada: "'A man a plan a canal Panama'", saida: "True" },
        { entrada: "'hello'", saida: "False" },
      ],
      dica: "Limpe a string com re.sub(), converta para lower e compare com [::-1].",
    },
    intermediario: {
      titulo: "Parser de Frontmatter Markdown",
      descricao:
        "Leia um arquivo .md, extraia campos YAML do bloco --- ... --- sem usar bibliotecas externas.",
      requisitos: [
        "Detectar bloco --- ... ---",
        "Extrair chave: valor sem yaml lib",
        "Retornar dict com os campos",
        "Retornar {} se não houver frontmatter",
      ],
      exemplos: [
        { entrada: "---\\ndescription: Teste\\n---\\nCorpo", saida: "{'description': 'Teste'}" },
      ],
      dica: "splitlines() + índice do segundo --- resolve sem regex.",
    },
    avancado: {
      titulo: "Servidor HTTP Minimalista sem Frameworks",
      descricao:
        "Construa um servidor HTTP usando apenas socket que responda GET /status com JSON e POST /echo devolvendo o body.",
      requisitos: [
        "Usar apenas socket e threading da stdlib",
        "Responder GET /status → {status: 'ok'}",
        "Responder POST /echo → body recebido",
        "Encerrar com CTRL+C limpo",
      ],
      exemplos: [
        { entrada: "GET /status", saida: '{"status":"ok"}' },
        { entrada: "POST /echo body=hello", saida: "hello" },
      ],
      dica: "socket.bind + socket.listen + threading.Thread por conexão. Parse HTTP manualmente pela primeira linha.",
    },
  },
};

function formatarDesafio(tecnologia: string, nivel: string): string {
  const tec = tecnologia.toLowerCase();
  const niv = nivel.toLowerCase();
  const d = DESAFIOS[tec]?.[niv] as
    | {
        titulo: string;
        descricao: string;
        requisitos: string[];
        exemplos: { entrada: string; saida: string }[];
        dica: string;
      }
    | undefined;

  if (!d) {
    const disponiveis = Object.keys(DESAFIOS).join(", ");
    return `❌ Desafio não encontrado para tecnologia='${tecnologia}' e nível='${nivel}'.\nTecnologias disponíveis: ${disponiveis}`;
  }

  const linhas: string[] = [
    `# ⚔️ Desafio de Código — ${tecnologia} · Nível ${nivel}`,
    "",
    `## ${d.titulo}`,
    "",
    `### Descrição\n${d.descricao}`,
    "",
    "### Requisitos",
    ...d.requisitos.map((r) => `- ${r}`),
    "",
    "### Exemplos",
    ...d.exemplos.map((e) => `- **Entrada:** \`${e.entrada}\` → **Saída:** \`${e.saida}\``),
    "",
    `### Dica\n> ${d.dica}`,
  ];
  return linhas.join("\n");
}

function gerarCertificado(nome: string, tecnologia: string): string {
  const trilha = buscarTrilha(tecnologia);
  const hoje = new Date();
  const data = hoje.toLocaleDateString("pt-BR");
  const anoMesDia = hoje.toISOString().slice(0, 10).replace(/-/g, "");
  const idSufixo = tecnologia.slice(0, 4).toUpperCase().padEnd(4, "X");
  const idRandom = String(Math.floor(1000 + Math.random() * 9000));
  const id = `DIO-BOB-${anoMesDia}-${idSufixo}${idRandom}`;

  const carga = trilha ? `${trilha.modulos.length * 10}h` : "40h";
  const nivel = trilha?.nivel ?? "N/A";
  const modulosTexto = trilha
    ? trilha.modulos.map((m) => `  ${m.ordem}. ${m.titulo}`).join("\n")
    : "  (módulos não encontrados)";

  return `# 🎓 CERTIFICADO DE CONCLUSÃO

---

## DIO — Digital Innovation One
### Formação Bob · Plataforma de Aprendizagem

---

Este certificado é concedido a

# ${nome.toUpperCase()}

pela conclusão com êxito da trilha de estudos

## ${tecnologia}

---

**Conteúdo concluído:**

${modulosTexto}

---

**Data de emissão:** ${data}
**Carga horária estimada:** ${carga}
**Nível:** ${nivel}

---

> *"A jornada de mil milhas começa com um único passo."*

---

Certificado emitido pela plataforma DIO em parceria com IBM Bob.
ID do Certificado: ${id}
`;
}

function salvarCertificado(nome: string, tecnologia: string, conteudo: string): string {
  const nomeArq = `certificado_${nome.toLowerCase().replace(/\s+/g, "_")}_${tecnologia.toLowerCase()}.md`;
  const destino = path.join(CERTIFICADOS_DIR, nomeArq);
  fs.mkdirSync(CERTIFICADOS_DIR, { recursive: true });
  fs.writeFileSync(destino, conteudo, "utf-8");
  return destino;
}

// ---------------------------------------------------------------------------
// Servidor MCP
// ---------------------------------------------------------------------------

const server = new McpServer({
  name: "dio-bob-mcp-server",
  version: "1.0.0",
});

// ── Tool: trilha ─────────────────────────────────────────────────────────────
server.registerTool(
  "trilha",
  {
    description:
      "Retorna o plano de estudos completo de uma tecnologia a partir de Data/Trilhas.json. " +
      "Tecnologias disponíveis: Python, JavaScript, Java, SQL, React.",
    inputSchema: z.object({
      tecnologia: z
        .string()
        .describe("Nome da tecnologia (ex: Java, Python, React, SQL, JavaScript)"),
    }),
  },
  async ({ tecnologia }) => {
    const trilha = buscarTrilha(tecnologia);
    if (!trilha) {
      const dados = carregarTrilhas();
      const disponiveis = dados
        ? dados.trilhas.map((t) => t.tecnologia).join(", ")
        : "arquivo Trilhas.json não encontrado";
      return {
        content: [
          {
            type: "text",
            text: `❌ Trilha '${tecnologia}' não encontrada.\nTrilhas disponíveis: ${disponiveis}`,
          },
        ],
        isError: true,
      };
    }
    return {
      content: [{ type: "text", text: formatarPlano(trilha) }],
    };
  }
);

// ── Tool: desafio ─────────────────────────────────────────────────────────────
server.registerTool(
  "desafio",
  {
    description:
      "Gera um desafio de código para a tecnologia e nível informados. " +
      "Tecnologias: java, python. Níveis: iniciante, intermediario, avancado.",
    inputSchema: z.object({
      tecnologia: z.string().describe("Tecnologia do desafio (ex: java, python)"),
      nivel: z
        .enum(["iniciante", "intermediario", "avancado"])
        .describe("Nível de dificuldade"),
    }),
  },
  async ({ tecnologia, nivel }) => {
    const conteudo = formatarDesafio(tecnologia, nivel);
    return {
      content: [{ type: "text", text: conteudo }],
      isError: conteudo.startsWith("❌"),
    };
  }
);

// ── Tool: certificado ─────────────────────────────────────────────────────────
server.registerTool(
  "certificado",
  {
    description:
      "Gera um certificado fictício em Markdown para o usuário que concluiu uma trilha. " +
      "Salva automaticamente em Data/certificados/ e retorna o conteúdo.",
    inputSchema: z.object({
      nome: z.string().describe("Nome completo do aluno"),
      tecnologia: z.string().describe("Tecnologia da trilha concluída (ex: Java, Python)"),
    }),
  },
  async ({ nome, tecnologia }) => {
    const conteudo = gerarCertificado(nome, tecnologia);
    let caminhoSalvo: string;
    try {
      caminhoSalvo = salvarCertificado(nome, tecnologia, conteudo);
    } catch (err) {
      return {
        content: [
          {
            type: "text",
            text: `❌ Erro ao salvar certificado: ${err instanceof Error ? err.message : String(err)}`,
          },
        ],
        isError: true,
      };
    }
    return {
      content: [
        {
          type: "text",
          text: `${conteudo}\n\n---\n📄 **Certificado salvo em:** \`${caminhoSalvo}\``,
        },
      ],
    };
  }
);

// ---------------------------------------------------------------------------
// Transport — stdio (padrão) ou HTTP
// ---------------------------------------------------------------------------

async function main() {
  const transport = process.env.MCP_TRANSPORT;

  if (transport === "http") {
    // HTTP/SSE — para conexões remotas via API
    // Requer: npm install @modelcontextprotocol/sdk (inclui StreamableHTTPServerTransport)
    const { default: http } = await import("http");
    const { StreamableHTTPServerTransport } = await import(
      "@modelcontextprotocol/sdk/server/streamableHttp.js"
    );

    const PORT = parseInt(process.env.PORT ?? "3333", 10);

    const httpServer = http.createServer(async (req, res) => {
      // CORS — permite conexão de qualquer origem (ajuste em produção)
      res.setHeader("Access-Control-Allow-Origin", process.env.ALLOWED_ORIGIN ?? "*");
      res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
      res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

      if (req.method === "OPTIONS") {
        res.writeHead(204);
        res.end();
        return;
      }

      if (req.url === "/health" && req.method === "GET") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ status: "ok", server: "dio-bob-mcp-server", version: "1.0.0" }));
        return;
      }

      if (req.url === "/mcp") {
        const httpTransport = new StreamableHTTPServerTransport({
          sessionIdGenerator: () => crypto.randomUUID(),
        });
        await server.connect(httpTransport);
        await httpTransport.handleRequest(req, res);
        return;
      }

      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Not found", endpoints: ["/health", "/mcp"] }));
    });

    httpServer.listen(PORT, () => {
      console.error(`[dio-bob-mcp] HTTP server listening on http://localhost:${PORT}`);
      console.error(`[dio-bob-mcp] MCP endpoint: http://localhost:${PORT}/mcp`);
      console.error(`[dio-bob-mcp] Health check: http://localhost:${PORT}/health`);
    });
  } else {
    // Modo padrão: stdio (para IBM Bob local)
    const stdioTransport = new StdioServerTransport();
    await server.connect(stdioTransport);
    console.error("[dio-bob-mcp] Running on stdio — ready for IBM Bob");
  }
}

main().catch((err) => {
  console.error("[dio-bob-mcp] Fatal error:", err);
  process.exit(1);
});
