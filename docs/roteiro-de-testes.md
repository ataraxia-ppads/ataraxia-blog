# Roteiro de testes manuais

Verificação feita a mão, percorrendo o sistema como um usuário. Serve para
conferir se cada caso de uso funciona antes de uma entrega.

Preencha a coluna **Resultado** com `OK` ou `Falhou`. Quando falhar, descreva o
que aconteceu na coluna de observação e abra a pendência no quadro.

## Como usar

1. Rode o sistema, ou acesse o endereço publicado.
2. Percorra cada linha na ordem.
3. Anote o resultado.
4. Registre a data e quem executou, no fim do arquivo.

## UC01 — Listar posts publicados

| # | Passo | Esperado | Resultado | Observação |
| - | ----- | -------- | --------- | ---------- |
| 1 | Abrir a página inicial sem estar autenticado | A listagem aparece | | |
| 2 | Conferir a ordem dos textos | Mais recente primeiro | | |
| 3 | Conferir se algum rascunho aparece | Nenhum rascunho na listagem | | |

## UC02 — Ler post

| # | Passo | Esperado | Resultado | Observação |
| - | ----- | -------- | --------- | ---------- |
| 1 | Clicar em um texto da listagem | O texto abre completo | | |
| 2 | Conferir título, autor, data, categoria e tags | Todos presentes | | |
| 3 | Acessar o endereço de um rascunho, deslogado | Erro 404 | | |

## UC03 — Buscar post

| # | Passo | Esperado | Resultado | Observação |
| - | ----- | -------- | --------- | ---------- |
| 1 | Buscar por um termo que existe em um título | O texto aparece | | |
| 2 | Buscar por um termo inexistente | Mensagem de nada encontrado | | |

## UC04 — Filtrar por categoria ou tag

| # | Passo | Esperado | Resultado | Observação |
| - | ----- | -------- | --------- | ---------- |
| 1 | Clicar em uma categoria | Só textos daquela categoria | | |
| 2 | Clicar em uma tag | Só textos com aquela tag | | |
| 3 | Remover o filtro | A listagem completa volta | | |

## UC05 — Cadastrar-se

| # | Passo | Esperado | Resultado | Observação |
| - | ----- | -------- | --------- | ---------- |
| 1 | Cadastrar com dados válidos | Conta criada e sessão iniciada | | |
| 2 | Cadastrar com nome de usuário repetido | Erro indicando o campo | | |
| 3 | Cadastrar com senha `12345678` | Recusa por senha comum | | |

## UC06 — Autenticar-se

| # | Passo | Esperado | Resultado | Observação |
| - | ----- | -------- | --------- | ---------- |
| 1 | Entrar com credenciais corretas | Acesso liberado | | |
| 2 | Entrar com senha errada | Mensagem de erro, sem dizer qual campo falhou | | |
| 3 | Sair | Sessão encerrada | | |

## UC08 — Manter post

| # | Passo | Esperado | Resultado | Observação |
| - | ----- | -------- | --------- | ---------- |
| 1 | Criar um texto | Salvo como rascunho | | |
| 2 | Salvar com título vazio | Recusa indicando o campo | | |
| 3 | Editar o próprio texto | Alteração gravada | | |
| 4 | Tentar editar o texto de outra pessoa pelo endereço direto | Erro 403 | | |
| 5 | Excluir um texto | Pede confirmação e exclui | | |

## UC09 — Publicar post

| # | Passo | Esperado | Resultado | Observação |
| - | ----- | -------- | --------- | ---------- |
| 1 | Publicar um rascunho | Passa a aparecer na listagem pública | | |
| 2 | Despublicar | Some da listagem pública | | |

## UC10 — Comentar post

| # | Passo | Esperado | Resultado | Observação |
| - | ----- | -------- | --------- | ---------- |
| 1 | Comentar autenticado | Comentário aparece | | |
| 2 | Ver o formulário deslogado | Convite para entrar, sem formulário | | |
| 3 | Enviar comentário vazio | Recusa | | |

## UC11 — Moderar comentário

| # | Passo | Esperado | Resultado | Observação |
| - | ----- | -------- | --------- | ---------- |
| 1 | Reprovar um comentário pelo admin | Some da página do texto | | |

## Registro da execução

| Data | Quem executou | Versão testada | Falhas encontradas |
| ---- | ------------- | -------------- | ------------------ |
| | | | |
