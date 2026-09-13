"""
commands.py — Lógica de negócio dos slash commands do projeto DIO/Bob.

Funções públicas:
  - buscar_trilha(tecnologia, caminho_json) -> dict | None
  - formatar_plano_estudos(trilha) -> str
  - gerar_desafio(tecnologia, nivel) -> str
  - gerar_certificado(nome, tecnologia, caminho_json, data_emissao, id_certificado) -> str
  - salvar_arquivo(conteudo, caminho) -> bool
  - parse_frontmatter(texto) -> dict
"""

import json
import os
import re
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# /trilha
# ---------------------------------------------------------------------------

def buscar_trilha(tecnologia: str, caminho_json: str) -> dict | None:
    """Lê Trilhas.json e retorna a trilha que bate com a tecnologia (case-insensitive).
    Retorna None se não encontrar ou se o arquivo não existir."""
    caminho = Path(caminho_json)
    if not caminho.exists():
        return None
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    for trilha in dados.get("trilhas", []):
        if trilha.get("tecnologia", "").lower() == tecnologia.lower():
            return trilha
    return None


def listar_tecnologias(caminho_json: str) -> list[str]:
    """Retorna lista de tecnologias cadastradas no Trilhas.json."""
    caminho = Path(caminho_json)
    if not caminho.exists():
        return []
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    return [t.get("tecnologia", "") for t in dados.get("trilhas", [])]


def formatar_plano_estudos(trilha: dict) -> str:
    """Formata uma trilha como plano de estudos em Markdown."""
    if not trilha:
        return "Trilha não encontrada."
    linhas = [
        f"# 📚 Trilha de Estudos — {trilha['tecnologia']}",
        "",
        f"**Nível:** {trilha['nivel']}",
        f"**Descrição:** {trilha['descricao']}",
        "",
        "---",
        "",
        "## Módulos da Trilha",
        "",
    ]
    for modulo in trilha.get("modulos", []):
        linhas.append(f"**Módulo {modulo['ordem']} — {modulo['titulo']}**")
        for i, topico in enumerate(modulo.get("topicos", []), 1):
            linhas.append(f"  {i}. {topico}")
        linhas.append("")
    linhas.append("---")
    linhas.append("")
    linhas.append("🚀 Bons estudos! Cada módulo concluído é um passo a mais na sua jornada.")
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# /desafio
# ---------------------------------------------------------------------------

DESAFIOS = {
    "java": {
        "iniciante": {
            "titulo": "Calculadora de Notas",
            "descricao": (
                "Crie um programa Java que leia 3 notas de um aluno (doubles), "
                "calcule a média aritmética e exiba se o aluno foi APROVADO (média ≥ 7.0), "
                "em RECUPERAÇÃO (5.0 ≤ média < 7.0) ou REPROVADO (média < 5.0)."
            ),
            "requisitos": [
                "Usar Scanner para ler as notas",
                "Calcular a média com precisão de 2 casas decimais",
                "Exibir o resultado com a situação do aluno",
            ],
            "exemplos": [
                {"entrada": "8.0, 7.5, 9.0", "saida": "Média: 8.17 — APROVADO"},
                {"entrada": "4.0, 6.0, 5.0", "saida": "Média: 5.00 — RECUPERAÇÃO"},
                {"entrada": "2.0, 3.0, 4.0", "saida": "Média: 3.00 — REPROVADO"},
            ],
            "restricoes": ["Não usar bibliotecas externas", "Apenas estruturas básicas de controle"],
            "dica": "Use if/else if/else com as condições de média na ordem certa.",
        },
        "intermediario": {
            "titulo": "Gerenciador de Estudantes com Coleções",
            "descricao": (
                "Implemente uma classe Estudante com nome e lista de notas. "
                "Crie um gerenciador que armazene estudantes em um List<Estudante>, "
                "permita adicionar, remover por nome e listar todos com suas médias "
                "usando Streams e Lambda."
            ),
            "requisitos": [
                "Classe Estudante com encapsulamento (getters/setters)",
                "Método calcularMedia() usando Stream.average()",
                "Listar estudantes ordenados por média decrescente",
                "Remover estudante por nome (case-insensitive)",
            ],
            "exemplos": [
                {"entrada": "add('Ana', [8,9,7])", "saida": "Ana adicionada. Média: 8.00"},
                {"entrada": "listar()", "saida": "Ana — 8.00 | João — 6.50"},
                {"entrada": "remover('ana')", "saida": "Ana removida com sucesso."},
            ],
            "restricoes": ["Usar Stream API obrigatoriamente", "Sem frameworks externos", "O(n) para buscas"],
            "dica": "Explore Comparator.comparingDouble() no sort e filter() com equalsIgnoreCase no remove.",
        },
        "avancado": {
            "titulo": "Sistema de Cache LRU",
            "descricao": (
                "Implemente um cache LRU (Least Recently Used) genérico em Java "
                "com capacidade configurável. O cache deve evictar o item menos "
                "recentemente acessado quando a capacidade for atingida."
            ),
            "requisitos": [
                "Implementar interface Map<K,V> ou criar LRUCache<K,V>",
                "get(key) e put(key, value) em O(1)",
                "Evicção automática do LRU ao atingir capacidade",
                "Thread-safe com synchronized ou ReentrantLock",
            ],
            "exemplos": [
                {"entrada": "cache(2); put(1,'a'); put(2,'b'); get(1); put(3,'c')", "saida": "get(2) → null (evictado)"},
                {"entrada": "cache(3); put(1,'x')×3; get(1); put(4,'d')", "saida": "get(2) → null"},
            ],
            "restricoes": ["get e put devem ser O(1)", "Usar LinkedHashMap ou implementar lista duplamente ligada"],
            "dica": "LinkedHashMap com accessOrder=true e override de removeEldestEntry() resolve em poucas linhas.",
        },
    }
}


def gerar_desafio(tecnologia: str, nivel: str) -> str:
    """Retorna o desafio formatado em Markdown para a tecnologia e nível dados."""
    tec = tecnologia.lower()
    niv = nivel.lower()
    if tec not in DESAFIOS or niv not in DESAFIOS[tec]:
        return f"Desafio não encontrado para tecnologia='{tecnologia}' e nível='{nivel}'."
    d = DESAFIOS[tec][niv]
    linhas = [
        f"# ⚔️ Desafio de Código — {tecnologia.title()} · Nível {nivel.title()}",
        "",
        f"## Título\n{d['titulo']}",
        "",
        f"## Descrição\n{d['descricao']}",
        "",
        "## Requisitos",
    ]
    for r in d["requisitos"]:
        linhas.append(f"- {r}")
    linhas += ["", "## Exemplos de Entrada e Saída"]
    for ex in d["exemplos"]:
        linhas.append(f"- **Entrada:** `{ex['entrada']}` → **Saída:** `{ex['saida']}`")
    linhas += ["", "## Restrições"]
    for r in d["restricoes"]:
        linhas.append(f"- {r}")
    linhas += ["", f"## Dica\n> {d['dica']}"]
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# /certificado
# ---------------------------------------------------------------------------

def gerar_certificado(
    nome: str,
    tecnologia: str,
    caminho_json: str,
    data_emissao: str = None,
    id_certificado: str = None,
) -> str:
    """Gera o conteúdo Markdown do certificado."""
    if data_emissao is None:
        data_emissao = date.today().strftime("%d/%m/%Y")
    if id_certificado is None:
        hoje = date.today()
        sufixo = tecnologia[:4].upper().ljust(4, "X")
        id_certificado = f"DIO-BOB-{hoje.strftime('%Y%m%d')}-{sufixo}0001"

    trilha = buscar_trilha(tecnologia, caminho_json)
    if trilha:
        carga = f"{len(trilha.get('modulos', [])) * 10}h"
        nivel = trilha.get("nivel", "N/A")
        modulos_texto = "\n".join(
            f"  {m['ordem']}. {m['titulo']}" for m in trilha.get("modulos", [])
        )
    else:
        carga = "40h"
        nivel = "N/A"
        modulos_texto = "  (módulos não encontrados)"

    return f"""# 🎓 CERTIFICADO DE CONCLUSÃO

---

## DIO — Digital Innovation One
### Formação Bob · Plataforma de Aprendizagem

---

Este certificado é concedido a

# {nome.upper()}

pela conclusão com êxito da trilha de estudos

## {tecnologia.title()}

---

**Conteúdo concluído:**

{modulos_texto}

---

**Data de emissão:** {data_emissao}
**Carga horária estimada:** {carga}
**Nível:** {nivel}

---

> *"A jornada de mil milhas começa com um único passo."*

---

Certificado emitido pela plataforma DIO em parceria com IBM Bob.
ID do Certificado: {id_certificado}
"""


# ---------------------------------------------------------------------------
# Utilitário — salvar arquivo
# ---------------------------------------------------------------------------

def salvar_arquivo(conteudo: str, caminho: str) -> bool:
    """Salva conteúdo em arquivo, criando diretórios necessários. Retorna True em sucesso."""
    try:
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Utilitário — parse frontmatter
# ---------------------------------------------------------------------------

def parse_frontmatter(texto: str) -> dict:
    """Extrai campos YAML do frontmatter (bloco --- ... ---) de um arquivo Markdown."""
    resultado = {}
    linhas = texto.splitlines()
    if not linhas or linhas[0].strip() != "---":
        return resultado
    fim = None
    for i, linha in enumerate(linhas[1:], 1):
        if linha.strip() == "---":
            fim = i
            break
    if fim is None:
        return resultado
    for linha in linhas[1:fim]:
        if ": " in linha:
            chave, valor = linha.split(": ", 1)
            resultado[chave.strip()] = valor.strip()
    return resultado
