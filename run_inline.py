"""
run_inline.py — Executa os testes e grava resultados_testes.txt sem depender do shell do Bob.
Rode diretamente: python run_inline.py  (da raiz do projeto)
"""
import importlib
import io
import json
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC  = ROOT / "src"
TESTS = ROOT / "tests"

for p in (str(SRC), str(TESTS)):
    if p not in sys.path:
        sys.path.insert(0, p)

# ── Importa os módulos que serão testados ────────────────────────────────────
import commands  # noqa: E402  (src/commands.py)

# ── Copia inline dos testes para não depender de arquivo externo ─────────────
spec = importlib.util.spec_from_file_location("test_commands", TESTS / "test_commands.py")
mod  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# ── Execução ─────────────────────────────────────────────────────────────────
loader = unittest.TestLoader()
suite  = loader.loadTestsFromModule(mod)
buf    = io.StringIO()
runner = unittest.TextTestRunner(stream=buf, verbosity=2)
resultado = runner.run(suite)
saida_testes = buf.getvalue()

# ── Métricas ──────────────────────────────────────────────────────────────────
total      = resultado.testsRun
falhas     = len(resultado.failures)
erros      = len(resultado.errors)
aprovados  = total - falhas - erros
pct        = round(aprovados / total * 100, 2) if total else 0
status     = "PASSOU" if resultado.wasSuccessful() else "FALHOU"

# ── Relatório ─────────────────────────────────────────────────────────────────
linhas = [
    "=" * 70,
    "  RELATÓRIO DE TESTES — DIO Bob · Formação Python/Java",
    f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
    "=" * 70,
    "",
    "── SUMÁRIO ────────────────────────────────────────────────────────",
    f"  Status geral     : {status}",
    f"  Total de testes  : {total}",
    f"  Aprovados        : {aprovados}",
    f"  Falhas           : {falhas}",
    f"  Erros            : {erros}",
    f"  Taxa de aprovação: {pct}%  (meta: >= 70%)",
    f"  Meta atingida    : {'SIM' if pct >= 70 else 'NAO'}",
    "",
    "── DETALHAMENTO DOS TESTES ────────────────────────────────────────",
    saida_testes,
]

if resultado.failures:
    linhas.append("── FALHAS ─────────────────────────────────────────────────────")
    for t, tb in resultado.failures:
        linhas += [f"  [FALHA] {t}", tb]

if resultado.errors:
    linhas.append("── ERROS ──────────────────────────────────────────────────────")
    for t, tb in resultado.errors:
        linhas += [f"  [ERRO] {t}", tb]

linhas += [
    "",
    "── CLASSES E CASOS DE TESTE EXECUTADOS ────────────────────────────",
    "  TestBuscarTrilha          — busca Java (exato, case-insensitive, campos)",
    "                               tecnologia inexistente, arquivo ausente",
    "  TestListarTecnologias     — lista completa, contém Java/Python, ausente",
    "  TestFormatarPlanoEstudos  — cabeçalho, nível, módulos, tópicos,",
    "                               trilha=None, encorajamento",
    "  TestGerarDesafio          — Java iniciante/intermediario/avancado,",
    "                               case-insensitive, inválidos, seções",
    "  TestGerarCertificado      — nome maiúsculo, tecnologia, data, ID,",
    "                               módulos, carga horária, fallback, cabeçalho",
    "  TestSalvarArquivo         — cria arquivo, cria dirs, caminho inválido",
    "  TestParseFrontmatter      — description, hint, sem ---,",
    "                               sem fechamento, vazio",
    "",
    "── ARQUIVOS GERADOS NESTA SESSÃO ──────────────────────────────────",
    "  src/commands.py                                  (lógica dos comandos)",
    "  tests/test_commands.py                           (testes unitários)",
    "  tests/runner.py                                  (runner com coverage)",
    "  Data/desafios/desafio_java_intermediario.md      (desafio para o aluno)",
    "  Data/certificados/certificado_aluno_java.md      (certificado Java)",
    "  resultados_testes.txt                            (este arquivo)",
    "",
    "── SLASH COMMANDS LOCAIS (.bob/commands/) ──────────────────────────",
    "  /trilha <tecnologia>                 ex: /trilha Java",
    "  /desafio <tecnologia> <nivel>        ex: /desafio Java intermediario",
    "  /certificado <nome> <tecnologia>     ex: /certificado 'Aluno' Java",
    "",
    "=" * 70,
    "  Fim do relatório",
    "=" * 70,
]

relatorio = "\n".join(linhas)
destino   = ROOT / "resultados_testes.txt"
destino.write_text(relatorio, encoding="utf-8")
print(relatorio)
print(f"\nRelatório salvo em: {destino}")
sys.exit(0 if resultado.wasSuccessful() else 1)
