# Diagramas de classes de projeto

O modelo de domínio descreve conceitos. Este capítulo descreve as classes que
vão existir no código, com o nome que vão ter, e por isso os identificadores
aparecem em inglês, como manda a convenção de idioma do projeto.

Cada classe pertence a uma de três camadas, marcadas no diagrama:

- **Model**, que guarda o estado e conhece as regras do próprio dado.
- **Form**, que valida o que chega do navegador antes de virar estado.
- **View**, que recebe a requisição, decide o que fazer e escolhe o template.

Um conceito do domínio não vira necessariamente uma classe só. `Usuário` vira o
`User` do Django mais um `Profile`, e `Post` traz junto um gerenciador de
consulta que isola o que é publicado do que é rascunho.

**Tabela 19 — Classes de projeto por aplicação**

| Aplicação | Classe | Camada | Papel |
| --------- | ------ | ------ | ----- |
| `accounts` | `Profile` | Model | Dados públicos do usuário, ligados um a um ao `User` |
| `accounts` | `SignUpForm` | Form | Valida nome de usuário, email e senha no cadastro |
| `accounts` | `SignUpView` | View | Cria conta e perfil e inicia a sessão |
| `accounts` | `ProfileUpdateView` | View | Edição do próprio perfil |
| `posts` | `Post` | Model | Texto, situação e datas |
| `posts` | `PublishedManager` | Model | Consulta que devolve apenas textos publicados |
| `posts` | `PostForm` | Form | Valida título e corpo e monta o slug |
| `posts` | `PostListView` | View | Listagem pública, com busca |
| `posts` | `PostDetailView` | View | Página do texto |
| `posts` | `PostCreateView`, `PostUpdateView`, `PostDeleteView` | View | Manutenção do texto pelo autor |
| `comments` | `Comment` | Model | Comentário, com a marca de aprovado |
| `comments` | `CommentForm` | Form | Valida corpo e tamanho |
| `comments` | `CommentCreateView` | View | Grava o comentário e volta para a página do texto |
| `taxonomy` | `Category`, `Tag` | Model | Termos que classificam o texto |
| `taxonomy` | `TermPostListView` | View | Listagem restrita a uma categoria ou tag |

As três aplicações que têm tela usam as views acima. Moderar comentário, manter
taxonomia e gerenciar usuários passam pelo admin do Django, e por isso aparecem
como classes de `admin` nos diagramas, sem view própria.
