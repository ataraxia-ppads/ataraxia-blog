# Conteúdo de demonstração

Os textos de exemplo que povoam o blog. Sem eles a tela inicial aparece vazia:
listagem sem posts e busca sem resultado, e não há como demonstrar o sistema nem
executar o [roteiro de testes](roteiro-de-testes.md).

Os textos estão no comando `python manage.py carregar_demo`, que pode ser rodado
mais de uma vez sem duplicar nada. Os autores de demonstração não têm senha
utilizável: servem para assinar os textos e ninguém entra com eles.

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

| Título | Autor | Situação | Publicado em |
| ------ | ----- | -------- | ------------ |
| Por que aprendi Python antes de qualquer outra linguagem | Helena Prado | publicado | 14/03/2026 |
| O que o ornitorrinco ensina sobre classificar as coisas | Marcos Tavares | publicado | 02/04/2026 |
| Três livros que mudaram meu jeito de ler dados | Júlia Nogueira | publicado | 20/04/2026 |
| Testes automatizados não são burocracia | Helena Prado | publicado | 09/05/2026 |
| Aprender a programar depois dos quarenta | Marcos Tavares | publicado | 27/05/2026 |
| Gráfico de pizza quase nunca é a melhor escolha | Júlia Nogueira | publicado | 15/06/2026 |
| Como escrevo mensagens de commit | Helena Prado | publicado | 03/07/2026 |
| Matemática para quem programa | Marcos Tavares | publicado | 12/08/2026 |
| Dados abertos e o que fazer com eles | Júlia Nogueira | publicado | 01/09/2026 |
| Rascunho: notas sobre revisão de código | Helena Prado | rascunho | |

O termo incomum do título é **ornitorrinco**, e o do corpo é **quimera**, no
texto "Matemática para quem programa".
