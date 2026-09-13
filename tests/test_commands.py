"""
test_commands.py — Testes unitários para src/commands.py
Cobertura alvo: ≥ 70%

Fluxos testados:
  - /trilha  : buscar Java, tecnologia inexistente, arquivo ausente, formatar plano
  - /desafio : Java iniciante/intermediario/avancado, tecnologia inválida
  - /certificado: com trilha existente, sem trilha, campos de saída
  - Utilitários: salvar_arquivo, parse_frontmatter, listar_tecnologias
"""

import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Garante que src/ está no path independente de onde os testes rodam
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from commands import (
    buscar_trilha,
    formatar_plano_estudos,
    gerar_certificado,
    gerar_desafio,
    listar_tecnologias,
    parse_frontmatter,
    salvar_arquivo,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

TRILHAS_FIXTURE = {
    "trilhas": [
        {
            "tecnologia": "Java",
            "nivel": "Iniciante ao Avançado",
            "descricao": "Aprenda Java com foco em POO e Spring Boot.",
            "modulos": [
                {"ordem": 1, "titulo": "Fundamentos de Java", "topicos": ["Sintaxe", "Tipos"]},
                {"ordem": 2, "titulo": "POO", "topicos": ["Classes", "Herança"]},
                {"ordem": 3, "titulo": "Spring Boot", "topicos": ["REST", "JPA"]},
            ],
        },
        {
            "tecnologia": "Python",
            "nivel": "Iniciante ao Avançado",
            "descricao": "Aprenda Python do zero.",
            "modulos": [
                {"ordem": 1, "titulo": "Fundamentos", "topicos": ["Sintaxe", "Variáveis"]},
            ],
        },
    ]
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def criar_json_fixture(tmp_path: Path) -> str:
    """Escreve o fixture de trilhas em um arquivo temporário e retorna o caminho."""
    caminho = tmp_path / "Trilhas.json"
    caminho.write_text(json.dumps(TRILHAS_FIXTURE), encoding="utf-8")
    return str(caminho)


# ---------------------------------------------------------------------------
# Testes — /trilha : buscar_trilha
# ---------------------------------------------------------------------------

class TestBuscarTrilha(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp()
        self.json_path = str(Path(self.tmp) / "Trilhas.json")
        Path(self.json_path).write_text(json.dumps(TRILHAS_FIXTURE), encoding="utf-8")

    def test_busca_java_exato(self):
        """Deve retornar a trilha Java quando o nome é exato."""
        trilha = buscar_trilha("Java", self.json_path)
        self.assertIsNotNone(trilha)
        self.assertEqual(trilha["tecnologia"], "Java")

    def test_busca_java_case_insensitive(self):
        """Deve encontrar Java independente de maiúsculas/minúsculas."""
        self.assertIsNotNone(buscar_trilha("java", self.json_path))
        self.assertIsNotNone(buscar_trilha("JAVA", self.json_path))
        self.assertIsNotNone(buscar_trilha("jAvA", self.json_path))

    def test_busca_python_retorna_python(self):
        """Deve retornar a trilha Python corretamente."""
        trilha = buscar_trilha("Python", self.json_path)
        self.assertEqual(trilha["tecnologia"], "Python")

    def test_tecnologia_inexistente_retorna_none(self):
        """Tecnologia não cadastrada deve retornar None."""
        self.assertIsNone(buscar_trilha("Kotlin", self.json_path))

    def test_arquivo_inexistente_retorna_none(self):
        """Arquivo JSON inexistente deve retornar None sem lançar exceção."""
        resultado = buscar_trilha("Java", "/nao/existe/Trilhas.json")
        self.assertIsNone(resultado)

    def test_trilha_java_possui_modulos(self):
        """Trilha Java deve ter pelo menos 1 módulo."""
        trilha = buscar_trilha("Java", self.json_path)
        self.assertGreater(len(trilha["modulos"]), 0)

    def test_trilha_java_primeiro_modulo(self):
        """Primeiro módulo de Java deve ter ordem 1."""
        trilha = buscar_trilha("Java", self.json_path)
        self.assertEqual(trilha["modulos"][0]["ordem"], 1)


# ---------------------------------------------------------------------------
# Testes — /trilha : listar_tecnologias
# ---------------------------------------------------------------------------

class TestListarTecnologias(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp()
        self.json_path = str(Path(self.tmp) / "Trilhas.json")
        Path(self.json_path).write_text(json.dumps(TRILHAS_FIXTURE), encoding="utf-8")

    def test_retorna_lista_nao_vazia(self):
        techs = listar_tecnologias(self.json_path)
        self.assertGreater(len(techs), 0)

    def test_contem_java_e_python(self):
        techs = listar_tecnologias(self.json_path)
        self.assertIn("Java", techs)
        self.assertIn("Python", techs)

    def test_arquivo_ausente_retorna_lista_vazia(self):
        self.assertEqual(listar_tecnologias("/nao/existe.json"), [])


# ---------------------------------------------------------------------------
# Testes — /trilha : formatar_plano_estudos
# ---------------------------------------------------------------------------

class TestFormatarPlanoEstudos(unittest.TestCase):

    def setUp(self):
        self.trilha_java = TRILHAS_FIXTURE["trilhas"][0]

    def test_contem_nome_tecnologia(self):
        resultado = formatar_plano_estudos(self.trilha_java)
        self.assertIn("Java", resultado)

    def test_contem_nivel(self):
        resultado = formatar_plano_estudos(self.trilha_java)
        self.assertIn("Iniciante ao Avançado", resultado)

    def test_contem_todos_modulos(self):
        resultado = formatar_plano_estudos(self.trilha_java)
        self.assertIn("Fundamentos de Java", resultado)
        self.assertIn("POO", resultado)
        self.assertIn("Spring Boot", resultado)

    def test_contem_topicos(self):
        resultado = formatar_plano_estudos(self.trilha_java)
        self.assertIn("Sintaxe", resultado)
        self.assertIn("Herança", resultado)

    def test_trilha_none_retorna_mensagem_erro(self):
        resultado = formatar_plano_estudos(None)
        self.assertIn("não encontrada", resultado)

    def test_formato_markdown_cabecalho(self):
        resultado = formatar_plano_estudos(self.trilha_java)
        self.assertTrue(resultado.startswith("# 📚 Trilha de Estudos"))

    def test_contem_mensagem_encorajamento(self):
        resultado = formatar_plano_estudos(self.trilha_java)
        self.assertIn("🚀", resultado)


# ---------------------------------------------------------------------------
# Testes — /desafio : gerar_desafio
# ---------------------------------------------------------------------------

class TestGerarDesafio(unittest.TestCase):

    def test_java_iniciante_retorna_desafio(self):
        resultado = gerar_desafio("java", "iniciante")
        self.assertIn("Calculadora de Notas", resultado)
        self.assertIn("iniciante", resultado.lower())

    def test_java_intermediario_retorna_desafio(self):
        resultado = gerar_desafio("java", "intermediario")
        self.assertIn("Gerenciador de Estudantes", resultado)

    def test_java_avancado_retorna_desafio(self):
        resultado = gerar_desafio("java", "avancado")
        self.assertIn("LRU", resultado)

    def test_case_insensitive_tecnologia(self):
        resultado = gerar_desafio("JAVA", "iniciante")
        self.assertIn("Calculadora", resultado)

    def test_case_insensitive_nivel(self):
        resultado = gerar_desafio("java", "INTERMEDIARIO")
        self.assertIn("Gerenciador", resultado)

    def test_tecnologia_inexistente_retorna_mensagem_erro(self):
        resultado = gerar_desafio("Cobol", "iniciante")
        self.assertIn("não encontrado", resultado)

    def test_nivel_inexistente_retorna_mensagem_erro(self):
        resultado = gerar_desafio("java", "expert")
        self.assertIn("não encontrado", resultado)

    def test_desafio_contem_secao_requisitos(self):
        resultado = gerar_desafio("java", "intermediario")
        self.assertIn("## Requisitos", resultado)

    def test_desafio_contem_secao_exemplos(self):
        resultado = gerar_desafio("java", "intermediario")
        self.assertIn("## Exemplos", resultado)

    def test_desafio_contem_dica(self):
        resultado = gerar_desafio("java", "intermediario")
        self.assertIn("## Dica", resultado)

    def test_desafio_contem_restricoes(self):
        resultado = gerar_desafio("java", "avancado")
        self.assertIn("## Restrições", resultado)


# ---------------------------------------------------------------------------
# Testes — /certificado : gerar_certificado
# ---------------------------------------------------------------------------

class TestGerarCertificado(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp()
        self.json_path = str(Path(self.tmp) / "Trilhas.json")
        Path(self.json_path).write_text(json.dumps(TRILHAS_FIXTURE), encoding="utf-8")

    def test_contem_nome_usuario_maiusculo(self):
        cert = gerar_certificado("Carlos Souza", "Java", self.json_path,
                                 data_emissao="01/01/2025", id_certificado="DIO-TEST-001")
        self.assertIn("CARLOS SOUZA", cert)

    def test_contem_tecnologia(self):
        cert = gerar_certificado("Ana", "Java", self.json_path,
                                 data_emissao="01/01/2025", id_certificado="DIO-TEST-002")
        self.assertIn("Java", cert)

    def test_contem_data_emissao(self):
        cert = gerar_certificado("Ana", "Java", self.json_path,
                                 data_emissao="15/06/2025", id_certificado="DIO-TEST-003")
        self.assertIn("15/06/2025", cert)

    def test_contem_id_certificado(self):
        cert = gerar_certificado("Ana", "Java", self.json_path,
                                 data_emissao="01/01/2025", id_certificado="DIO-BOB-TEST-9999")
        self.assertIn("DIO-BOB-TEST-9999", cert)

    def test_contem_modulos_da_trilha(self):
        cert = gerar_certificado("Ana", "Java", self.json_path,
                                 data_emissao="01/01/2025", id_certificado="DIO-TEST-004")
        self.assertIn("Fundamentos de Java", cert)
        self.assertIn("Spring Boot", cert)

    def test_carga_horaria_baseada_em_modulos(self):
        """3 módulos × 10h = 30h."""
        cert = gerar_certificado("Ana", "Java", self.json_path,
                                 data_emissao="01/01/2025", id_certificado="DIO-TEST-005")
        self.assertIn("30h", cert)

    def test_tecnologia_inexistente_usa_fallback(self):
        cert = gerar_certificado("Ana", "Kotlin", self.json_path,
                                 data_emissao="01/01/2025", id_certificado="DIO-TEST-006")
        self.assertIn("40h", cert)

    def test_id_gerado_automaticamente_quando_nenhum_fornecido(self):
        cert = gerar_certificado("Ana", "Java", self.json_path)
        self.assertIn("DIO-BOB-", cert)

    def test_formato_markdown_cabecalho(self):
        cert = gerar_certificado("Ana", "Java", self.json_path,
                                 data_emissao="01/01/2025", id_certificado="DIO-TEST-007")
        self.assertIn("# 🎓 CERTIFICADO DE CONCLUSÃO", cert)


# ---------------------------------------------------------------------------
# Testes — salvar_arquivo
# ---------------------------------------------------------------------------

class TestSalvarArquivo(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp()

    def test_cria_arquivo_com_conteudo(self):
        caminho = str(Path(self.tmp) / "teste.md")
        resultado = salvar_arquivo("# Olá", caminho)
        self.assertTrue(resultado)
        self.assertEqual(Path(caminho).read_text(encoding="utf-8"), "# Olá")

    def test_cria_diretorios_intermediarios(self):
        caminho = str(Path(self.tmp) / "sub" / "dir" / "arquivo.md")
        resultado = salvar_arquivo("conteudo", caminho)
        self.assertTrue(resultado)
        self.assertTrue(Path(caminho).exists())

    def test_retorna_false_em_caminho_invalido(self):
        resultado = salvar_arquivo("conteudo", "/\x00/invalido/arquivo.md")
        self.assertFalse(resultado)


# ---------------------------------------------------------------------------
# Testes — parse_frontmatter
# ---------------------------------------------------------------------------

class TestParseFrontmatter(unittest.TestCase):

    def test_extrai_description(self):
        texto = "---\ndescription: Meu comando\nargument-hint: <arg>\n---\nCorpo"
        resultado = parse_frontmatter(texto)
        self.assertEqual(resultado["description"], "Meu comando")

    def test_extrai_argument_hint(self):
        texto = "---\ndescription: Teste\nargument-hint: <tecnologia> <nivel>\n---"
        resultado = parse_frontmatter(texto)
        self.assertEqual(resultado["argument-hint"], "<tecnologia> <nivel>")

    def test_sem_frontmatter_retorna_dict_vazio(self):
        resultado = parse_frontmatter("Apenas texto sem frontmatter")
        self.assertEqual(resultado, {})

    def test_frontmatter_sem_fechamento_retorna_dict_vazio(self):
        texto = "---\ndescription: Sem fechamento\n"
        resultado = parse_frontmatter(texto)
        self.assertEqual(resultado, {})

    def test_frontmatter_vazio(self):
        texto = "---\n---\nCorpo do comando"
        resultado = parse_frontmatter(texto)
        self.assertEqual(resultado, {})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
