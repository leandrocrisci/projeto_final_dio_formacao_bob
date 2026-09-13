"""
runner.py — Executa os testes unitários, coleta cobertura e grava resultados_testes.txt
Execute com:  python tests/runner.py  (a partir da raiz do projeto)
"""

import io
import json
import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

# ── Tenta instalar coverage se ainda não estiver disponível ─────────────────
try:
    import coverage
    HAS_COVERAGE = True
except ImportError:
    HAS_COVERAGE = False

# ── Execução dos testes ──────────────────────────────────────────────────────

def executar_testes():
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromName("test_commands")

    buffer = io.StringIO()
    runner = unittest.TextTestRunner(stream=buffer, verbosity=2)

    if HAS_COVERAGE:
        cov = coverage.Coverage(source=[str(ROOT / "src")])
        cov.start()

    resultado = runner.run(suite)

    if HAS_COVERAGE:
        cov.stop()
        cov.save()

    saida_testes = buffer.getvalue()

    # ── Cobertura ────────────────────────────────────────────────────────────
    cobertura_str = "coverage não instalado — execute: pip install coverage"
    cobertura_pct = None

    if HAS_COVERAGE:
        buf_cov = io.StringIO()
        total = cov.report(file=buf_cov, show_missing=True)
        cobertura_str = buf_cov.getvalue()
        cobertura_pct = round(total, 2)

    # ── Montagem do relatório ─────────────────────────────────────────────────
    total_tests  = resultado.testsRun
    falhas       = len(resultado.failures)
    erros        = len(resultado.errors)
    aprovados    = total_tests - falhas - erros
    pct_aprovacao = round((aprovados / total_tests * 100), 2) if total_tests else 0
    status_geral  = "✅ PASSOU" if resultado.wasSuccessful() else "❌ FALHOU"

    linhas = [
        "=" * 70,
        "  RELATÓRIO DE TESTES — DIO Bob · Formação Python/Java",
        f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        "=" * 70,
        "",
        "── SUMÁRIO ────────────────────────────────────────────────────────",
        f"  Status geral    : {status_geral}",
        f"  Total de testes : {total_tests}",
        f"  Aprovados       : {aprovados}",
        f"  Falhas          : {falhas}",
        f"  Erros           : {erros}",
        f"  Taxa de aprovação: {pct_aprovacao}%",
    ]

    if cobertura_pct is not None:
        meta_ok = "✅" if cobertura_pct >= 70 else "⚠️ ABAIXO DA META"
        linhas.append(f"  Cobertura de código: {cobertura_pct}% {meta_ok} (meta: ≥70%)")

    linhas += [
        "",
        "── SAÍDA DETALHADA DOS TESTES ─────────────────────────────────────",
        saida_testes,
    ]

    if HAS_COVERAGE:
        linhas += [
            "── RELATÓRIO DE COBERTURA ─────────────────────────────────────────",
            cobertura_str,
        ]

    if resultado.failures:
        linhas += ["── FALHAS ─────────────────────────────────────────────────────────"]
        for test, tb in resultado.failures:
            linhas.append(f"\n[FALHA] {test}")
            linhas.append(tb)

    if resultado.errors:
        linhas += ["── ERROS ──────────────────────────────────────────────────────────"]
        for test, tb in resultado.errors:
            linhas.append(f"\n[ERRO] {test}")
            linhas.append(tb)

    linhas += [
        "",
        "── ARQUIVOS GERADOS ───────────────────────────────────────────────",
        "  Data/desafios/desafio_java_intermediario.md",
        "  Data/certificados/certificado_aluno_java.md",
        "",
        "── SLASH COMMANDS DISPONÍVEIS ─────────────────────────────────────",
        "  /trilha <tecnologia>",
        "  /desafio <tecnologia> <nivel>",
        "  /certificado <nome> <tecnologia>",
        "",
        "=" * 70,
        "  Fim do relatório",
        "=" * 70,
    ]

    relatorio = "\n".join(linhas)

    saida = ROOT / "resultados_testes.txt"
    saida.write_text(relatorio, encoding="utf-8")
    print(relatorio)
    print(f"\n📄 Relatório salvo em: {saida}")
    return resultado


if __name__ == "__main__":
    res = executar_testes()
    sys.exit(0 if res.wasSuccessful() else 1)
