# Diagramas de sequência de sistema

Cada diagrama mostra um caso de uso principal com o sistema tratado como caixa
preta: aparecem os eventos que o ator dispara, na ordem em que acontecem, e as
respostas devolvidas. Como o sistema é uma peça só, não há aqui divisão em
telas, views ou modelos. Essa divisão está no capítulo de diagramas de sequência
de projeto.

As operações abaixo são a fronteira do sistema. O que existir fora dessa lista
não é acionável pelo usuário nos casos de uso principais. Quem dispara cada uma
é o ator do caso de uso correspondente: visitante em UC02, UC03 e UC05, autor em
UC08 e UC10.

**Tabela 15 — Operações de sistema**

| Operação | Parâmetros | Caso de uso | Resposta |
| ---------------------------- | -------------------- | ------------------ | -------------------------------------- |
| `abrirPost` | slug do texto | UC02 | Post publicado com os comentários aprovados, ou erro 404 |
| `buscar` | termo, página | UC03 | Listagem com os textos que contêm o termo, ou aviso de nada encontrado |
| `abrirCadastro` | nenhum | UC05 | Formulário de cadastro |
| `cadastrar` | nome de usuário, email, senha | UC05 | Conta criada e sessão iniciada, ou erro de validação |
| `abrirEditor` | nenhum | UC08 | Formulário de texto |
| `salvarPost` | título, corpo, aceita comentários | UC08 | Rascunho gravado, ou campos pendentes |
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
        S-->>V: título, autor, data e corpo
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

## UC03 — Buscar post

```mermaid
sequenceDiagram
    actor V as Visitante
    participant S as :Sistema
    V->>S: buscar(termo, página)
    alt termo vazio
        S-->>V: listagem completa, como em UC01
    else textos encontrados
        S-->>V: posts publicados com o termo, do mais recente ao mais antigo
        S-->>V: quantidade encontrada, termo mantido e opção de limpar
    else nenhum texto encontrado
        S-->>V: aviso de nada encontrado e opção de voltar
    end
```

**Figura 5 — Sequência de sistema do UC03**

A busca é a listagem com um parâmetro a mais, e por isso o termo vazio devolve
a listagem completa, e não um erro.

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
    S-->>A: formulário com título, corpo e opção de aceitar comentários
    A->>S: salvarPost(título, corpo, aceitaComentários)
    alt título e corpo preenchidos
        S-->>A: rascunho gravado, com slug e autoria
    else campo obrigatório vazio
        S-->>A: campos pendentes, formulário preservado
    end
    A->>S: editarPost(slug, título, corpo, aceitaComentários)
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
    else corpo vazio ou acima de 2.000 caracteres
        S-->>U: aviso do problema, texto digitado preservado
    else comentários encerrados pelo autor
        S-->>U: gravação recusada, texto fechado a comentários
    else post despublicado durante a escrita
        S-->>U: gravação recusada, texto indisponível
    end
```

**Figura 8 — Sequência de sistema do UC10**

O visitante não autenticado não aparece no diagrama porque não chega a disparar
a operação: sem sessão, o sistema exibe o convite para entrar no lugar do
formulário, como descrito em UC02.
