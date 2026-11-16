# Conteúdo de demonstração

Os textos de exemplo que povoam o blog. Sem eles a tela inicial aparece vazia:
listagem sem posts e busca sem resultado, e não há como demonstrar o sistema nem
executar o [roteiro de testes](roteiro-de-testes.md).

Os textos estão no comando `python manage.py carregar_demo`, que pode ser rodado
mais de uma vez sem duplicar nada. Os autores de demonstração são os integrantes do
grupo, e os textos tratam, de forma geral, de como se constrói um blog como este. Essas contas não têm senha
utilizável: servem para assinar os textos e ninguém entra com elas.

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
| O que é o Ataraxia e por que um blog | Pedro Emmanuel Esteves | publicado | 24/08/2026 |
| Por que Django para um blog pequeno | Renan Jordão | publicado | 02/09/2026 |
| O ornitorrinco dos casos de uso | Rafaela Rarume | publicado | 12/09/2026 |
| Protótipos em HTML antes de qualquer linha de Python | Rafaela Rarume | publicado | 21/09/2026 |
| O que a revisão por Pull Request ensina | Pedro Emmanuel Esteves | publicado | 01/10/2026 |
| Do caso de uso ao teste: como a busca foi construída | Felipe Amorim | publicado | 14/10/2026 |
| Comentário é texto puro, e isso é uma decisão de segurança | Gabriel Vieira Ferreira | publicado | 23/10/2026 |
| Esconder o botão não é autorização | Pedro Emmanuel Esteves | publicado | 04/11/2026 |
| Testar antes de publicar: o que automatizar e o que olhar | Renan Jordão | publicado | 15/11/2026 |
| Rascunho: ideias para os próximos textos | Felipe Amorim | rascunho | |

O termo incomum do título é **ornitorrinco**, e o do corpo é **quimera**, no
texto "Esconder o botão não é autorização".
