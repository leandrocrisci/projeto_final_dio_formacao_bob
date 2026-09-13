# ⚔️ Desafio de Código — Java · Nível Intermediário

**Aluno:** (preencha seu nome)
**Data:** 09/07/2025
**Trilha:** Java — Formação DIO com IBM Bob

---

## Título
Gerenciador de Estudantes com Coleções

## Descrição

Implemente uma classe `Estudante` com nome e lista de notas.
Crie um gerenciador que armazene estudantes em um `List<Estudante>`,
permita adicionar, remover por nome e listar todos com suas médias
usando **Streams** e **Lambda**.

---

## Requisitos

- [ ] Classe `Estudante` com encapsulamento (getters/setters)
- [ ] Método `calcularMedia()` usando `Stream.average()`
- [ ] Listar estudantes ordenados por média decrescente
- [ ] Remover estudante por nome (case-insensitive)
- [ ] Exibir situação: APROVADO (≥7.0), RECUPERAÇÃO (5.0–6.9), REPROVADO (<5.0)

---

## Exemplos de Entrada e Saída

| Operação | Entrada | Saída esperada |
|---|---|---|
| Adicionar | `add("Ana", [8.0, 9.0, 7.0])` | `Ana adicionada. Média: 8.00 — APROVADO` |
| Listar | `listar()` | `Ana — 8.00 \| João — 6.50` (ordem decrescente) |
| Remover | `remover("ana")` | `Ana removida com sucesso.` |
| Inválido | `remover("xyz")` | `Estudante não encontrado.` |

---

## Restrições

- Usar **Stream API** obrigatoriamente no cálculo de média e na listagem
- Sem frameworks externos — apenas `java.util.*`
- Busca/remoção deve ser O(n)
- Sem uso de loops `for`/`while` onde Streams forem aplicáveis

---

## Dica

> Explore `Comparator.comparingDouble()` no sort e `filter()` com
> `equalsIgnoreCase()` no remove. Para a média, `mapToDouble()` +
> `average().orElse(0.0)` resolve de forma elegante.

---

## Template de Solução

```java
import java.util.*;
import java.util.stream.*;

public class Estudante {
    private String nome;
    private List<Double> notas;

    public Estudante(String nome, List<Double> notas) {
        // TODO
    }

    public double calcularMedia() {
        // TODO: usar Stream.average()
        return 0;
    }

    public String getSituacao() {
        // TODO: APROVADO / RECUPERAÇÃO / REPROVADO
        return "";
    }

    // getters e setters
}

public class GerenciadorEstudantes {
    private List<Estudante> estudantes = new ArrayList<>();

    public void adicionar(String nome, List<Double> notas) {
        // TODO
    }

    public void remover(String nome) {
        // TODO: case-insensitive
    }

    public void listar() {
        // TODO: ordenado por média decrescente com Streams
    }
}
```

---

**Submeta sua solução no chat com `/desafio Java intermediario` para revisão!**
