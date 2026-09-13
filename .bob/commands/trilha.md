---
description: Gera um plano de estudos completo a partir de uma trilha no arquivo Trilhas.json
argument-hint: <tecnologia>
---

O usuário quer ver o plano de estudos da trilha de **$1**.

Leia o arquivo `Data/Trilhas.json` do projeto atual e localize a trilha cuja tecnologia corresponda a "$1" (faça a busca sem distinção de maiúsculas/minúsculas).

Se a trilha for encontrada, apresente o plano de estudos no seguinte formato:

---

# 📚 Trilha de Estudos — {tecnologia}

**Nível:** {nivel}
**Descrição:** {descricao}

---

## Módulos da Trilha

Para cada módulo, exiba:

**Módulo {ordem} — {titulo}**
Lista de tópicos como itens numerados.

---

Ao final, inclua uma mensagem de encorajamento curta para o usuário começar a trilha.

Se a tecnologia informada não existir no arquivo, informe quais trilhas estão disponíveis listando as tecnologias cadastradas em `Data/Trilhas.json`.
