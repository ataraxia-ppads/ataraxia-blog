# Diagramas de sequência de sistema

Cada diagrama mostra um caso de uso principal com o sistema tratado como caixa
preta: aparecem os eventos que o ator dispara, na ordem em que acontecem, e as
respostas devolvidas. Como o sistema é uma peça só, não há aqui divisão em
telas, views ou modelos. Essa divisão está no capítulo de diagramas de sequência
de projeto.

As operações abaixo são a fronteira do sistema. O que existir fora dessa lista
não é acionável pelo usuário nos casos de uso principais. Quem dispara cada uma
é o ator do caso de uso correspondente: visitante em UC02, UC04 e UC05, autor em
UC08 e UC10.

**Tabela 15 — Operações de sistema**

| Operação | Parâmetros | Caso de uso | Resposta |
| ------------------------------ | -------------------------- | ------------ | -------------------------------- |
| `abrirPost` | slug do texto | UC02 | Post publicado com os comentários aprovados, ou erro 404 |
| `filtrarPorTermo` | tipo do termo, slug, página | UC04 | Listagem restrita ao termo, ou erro 404 |
| `abrirCadastro` | nenhum | UC05 | Formulário de cadastro |
| `cadastrar` | nome de usuário, email, senha | UC05 | Conta criada e sessão iniciada, ou erro de validação |
| `abrirEditor` | nenhum | UC08 | Formulário de texto |
| `salvarPost` | título, corpo, categoria, tags | UC08 | Rascunho gravado, ou campos pendentes |
| `editarPost` | slug e os campos do texto | UC08 | Alteração gravada, ou erro 403 |
| `excluirPost` | slug | UC08 | Pedido de confirmação |
| `confirmarExclusão` | slug | UC08 | Post e comentários excluídos |
| `comentar` | slug do post, corpo | UC10 | Comentário gravado e visível, ou aviso do problema |

## UC02 — Ler post

```mermaid
sequenceDiagram
    actor V as Visitante
    participant S as :Sistema
    V->>S: abrirPost(slug)
    alt post publicado
        S-->>V: título, autor, data, categoria, tags e corpo
        S-->>V: comentários aprovados, do mais antigo ao mais recente
        opt visitante autenticado
            S-->>V: formulário de comentário
        end
    else post inexistente ou em rascunho
        S-->>V: erro 404
    end
```

**Figura 4 — Sequência de sistema do UC02**

O rascunho e o endereço inexistente produzem a mesma resposta, e é o que RN01
exige: um 403 confirmaria que o texto existe.

## UC04 — Filtrar por categoria ou tag

```mermaid
sequenceDiagram
    actor V as Visitante
    participant S as :Sistema
    V->>S: filtrarPorTermo(tipo, slug, página)
    alt termo com posts publicados
        S-->>V: posts do termo, do mais recente ao mais antigo
        S-->>V: filtro aplicado e opção de removê-lo
    else termo sem posts publicados
        S-->>V: aviso de listagem vazia e opção de voltar
    else termo inexistente
        S-->>V: erro 404
    end
```

**Figura 5 — Sequência de sistema do UC04**

O parâmetro `tipo` distingue categoria de tag. A operação é a mesma porque o
comportamento é o mesmo: restringir a listagem a um termo e permitir desfazer.

## UC05 — Cadastrar-se

```mermaid
sequenceDiagram
    actor V as Visitante
    participant S as :Sistema
    V->>S: abrirCadastro()
    S-->>V: formulário com nome de usuário, email e senha
    V->>S: cadastrar(nomeDeUsuário, email, senha)
    alt dados aceitos
        S-->>V: conta e perfil criados, sessão iniciada
        S-->>V: listagem de textos
    else nome de usuário ou email já em uso
        S-->>V: campo em conflito, formulário preservado sem a senha
    else senha recusada
        S-->>V: regra de robustez não atendida
    end
```

**Figura 6 — Sequência de sistema do UC05**

## UC08 — Manter post

```mermaid
sequenceDiagram
    actor A as Autor
    participant S as :Sistema
    A->>S: abrirEditor()
    S-->>A: formulário com título, corpo, categoria e tags
    A->>S: salvarPost(título, corpo, categoria, tags)
    alt título e corpo preenchidos
        S-->>A: rascunho gravado, com slug e autoria
    else campo obrigatório vazio
        S-->>A: campos pendentes, formulário preservado
    end
    A->>S: editarPost(slug, título, corpo, categoria, tags)
    alt post do próprio autor
        S-->>A: alteração gravada, com data de modificação
    else post de outro autor
        S-->>A: erro 403
    end
    A->>S: excluirPost(slug)
    S-->>A: pedido de confirmação, avisando que é irreversível
    A->>S: confirmarExclusão(slug)
    S-->>A: post e comentários vinculados excluídos
```

**Figura 7 — Sequência de sistema do UC08**

Criar, alterar e excluir estão no mesmo diagrama porque são o mesmo caso de uso.
As três operações são independentes entre si, e a ordem em que aparecem é a de
leitura, não uma sequência obrigatória.

## UC10 — Comentar post

```mermaid
sequenceDiagram
    actor U as Autor
    participant S as :Sistema
    U->>S: comentar(slugDoPost, corpo)
    alt comentário aceito
        S-->>U: comentário gravado, aprovado e visível na página
    else corpo vazio ou acima do tamanho máximo
        S-->>U: aviso do problema, texto digitado preservado
    else post despublicado durante a escrita
        S-->>U: gravação recusada, texto indisponível
    end
```

**Figura 8 — Sequência de sistema do UC10**

O visitante não autenticado não aparece no diagrama porque não chega a disparar
a operação: sem sessão, o sistema exibe o convite para entrar no lugar do
formulário, como descrito em UC02.
