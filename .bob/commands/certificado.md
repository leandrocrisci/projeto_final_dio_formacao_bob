---
description: Gera um certificado fictício em Markdown para o usuário que concluiu uma trilha
argument-hint: <seu-nome> <tecnologia-da-trilha>
---

O usuário **$1** concluiu a trilha de **$2** e deseja receber o certificado.

Gere um certificado fictício completo em Markdown, salve-o no diretório `Data/certificados/` com o nome `certificado_$1_$2.md` (em minúsculas e sem espaços, substituindo espaços por underscores) e exiba o conteúdo na conversa.

O certificado deve seguir exatamente este modelo:

---

```markdown
# 🎓 CERTIFICADO DE CONCLUSÃO

---

## DIO — Digital Innovation One
### Formação Bob · Plataforma de Aprendizagem

---

Este certificado é concedido a

# {NOME DO USUÁRIO EM MAIÚSCULAS}

pela conclusão com êxito da trilha de estudos

## {Tecnologia}

---

**Conteúdo concluído:**
Lista dos módulos da trilha de {Tecnologia} (leia do arquivo `Data/Trilhas.json` se disponível, ou liste módulos típicos da tecnologia).

---

**Data de emissão:** {data atual no formato DD/MM/AAAA}

**Carga horária estimada:** {estimativa coerente com a trilha, ex: 40h, 60h, 80h}

**Nível:** {nivel da trilha}

---

> *"A jornada de mil milhas começa com um único passo."*

---

Certificado emitido pela plataforma DIO em parceria com IBM Bob.
ID do Certificado: DIO-BOB-{ANO}{MES}{DIA}-{4 letras iniciais da tecnologia em maiúsculo}{4 dígitos aleatórios}
```

---

Após exibir o certificado, confirme ao usuário o caminho onde o arquivo foi salvo em `Data/certificados/`.
