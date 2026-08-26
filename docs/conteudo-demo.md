# Conteúdo de demonstração

Os textos de exemplo que povoam o blog. Sem eles a tela inicial aparece vazia:
listagem sem posts, busca sem resultado, filtro sem categoria — e não há como
demonstrar o sistema nem executar o [roteiro de testes](roteiro-de-testes.md).

Este arquivo é a fonte. Depois de preenchido, vira uma *fixture* do Django, que
carrega tudo na base com um comando.

## O que é preciso

| Item | Quantidade |
| ---- | ---------- |
| Categorias | 4 |
| Tags | 8 |
| Posts | 10, sendo 1 em rascunho |

## Quatro exigências que o roteiro de testes depende

Não são detalhe de estilo. Sem elas, alguns testes não têm como rodar:

1. **Um post precisa ficar em rascunho.** É o que prova que rascunho não vaza
   para o visitante.
2. **Pelo menos três posts na mesma categoria.** Filtrar por categoria que só
   tem um post não demonstra filtro nenhum.
3. **Uma palavra incomum no título de um único post.** É o termo que a busca vai
   procurar, e ela precisa retornar exatamente aquele.
4. **Datas de publicação diferentes entre si.** A listagem ordena do mais
   recente para o mais antigo, e com datas iguais não dá para conferir a ordem.

## Sobre o slug

O slug é o endereço do item, e aparece na URL: `blog.ataraxia.dev/categoria/`
**`tecnologia`**. Escreva em minúsculas, sem acento e sem cedilha, trocando
espaço por hífen.

`Programação e Carreira` vira `programacao-e-carreira`.

## Categorias

| Nome | Slug | Descrição |
| ---- | ---- | --------- |
| Tecnologia | `tecnologia` | Ferramentas, linguagens e o que sai de novo |
| | | |
| | | |
| | | |

## Tags

Uma palavra ou duas, minúsculas, sem acento. Tag é assunto transversal — atravessa
categorias, ao contrário da categoria, que é uma só por post.

`python`, `carreira`, ...

## Posts

Um bloco por post, no formato abaixo. O corpo tem de três a cinco parágrafos —
o suficiente para a tela de leitura não parecer um bilhete, sem virar trabalho
de redação.

---

### Post 1

| Campo | Conteúdo |
| ----- | -------- |
| Título | Por que aprendi Python antes de qualquer outra linguagem |
| Autor | pedro |
| Categoria | `tecnologia` |
| Tags | `python`, `carreira` |
| Situação | publicado |
| Data | 2026-03-14 |

Quando decidi mudar de área, a primeira pergunta foi por onde começar. Havia
listas com dez linguagens, e cada uma prometia ser a definitiva.

Escolhi Python por um motivo pouco romântico: era a que tinha mais material em
português. Aprender programação já é difícil o bastante sem somar a barreira do
idioma a cada dúvida.

Dois anos depois a escolha se provou certa por outro motivo. A comunidade é
grande, então toda dúvida que tive alguém já teve antes, e escreveu a resposta.

---

### Post 2

| Campo | Conteúdo |
| ----- | -------- |
| Título | |
| Autor | |
| Categoria | |
| Tags | |
| Situação | publicado |
| Data | |

---

### Post 3

| Campo | Conteúdo |
| ----- | -------- |
| Título | |
| Autor | |
| Categoria | |
| Tags | |
| Situação | rascunho |
| Data | |

<!--
Repita o bloco até dez. O campo Situação aceita "publicado" ou "rascunho";
rascunho não tem data de publicação.
-->
