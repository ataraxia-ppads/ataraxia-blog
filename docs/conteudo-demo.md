# Conteúdo de demonstração

Os textos de exemplo que povoam o blog. Sem eles a tela inicial aparece vazia:
listagem sem posts e busca sem resultado, e não há como demonstrar o sistema nem
executar o [roteiro de testes](roteiro-de-testes.md).

Este arquivo é a fonte. Depois de preenchido, vira uma *fixture* do Django, que
carrega tudo na base com um comando.

## O que é preciso

| Item | Quantidade |
| ---- | ---------- |
| Posts | 10, sendo 1 em rascunho |

## Quatro exigências de que o roteiro de testes depende

Não são detalhe de estilo. Sem elas, alguns testes não têm como rodar:

1. **Um post precisa ficar em rascunho.** É o que prova que rascunho não vaza
   para o visitante.
2. **Uma palavra incomum no título de um único post.** É o termo que a busca vai
   procurar, e ela precisa retornar exatamente aquele.
3. **Uma palavra incomum no corpo de outro post, e não no título.** Prova que a
   busca olha o corpo, e não só o título.
4. **Datas de publicação diferentes entre si.** A listagem ordena do mais
   recente para o mais antigo, e com datas iguais não dá para conferir a ordem.

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
| Situação | publicado |
| Data | |

---

### Post 3

| Campo | Conteúdo |
| ----- | -------- |
| Título | |
| Autor | |
| Situação | rascunho |
| Data | |

<!--
Repita o bloco até dez. O campo Situação aceita "publicado" ou "rascunho";
rascunho não tem data de publicação.
-->
