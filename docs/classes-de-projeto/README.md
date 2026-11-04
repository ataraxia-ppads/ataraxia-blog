# Diagramas de classes de projeto

O modelo de domínio descreve conceitos. Este capítulo descreve as classes que existem no código, com o nome que têm, e por isso os identificadores aparecem em inglês, como manda a convenção de idioma do projeto.

Cada classe pertence a uma de três camadas, marcadas no diagrama:

- **Model**, que guarda o estado e conhece as regras do próprio dado.
- **Form**, que valida o que chega do navegador antes de virar estado.
- **View**, que recebe a requisição, decide o que fazer e escolhe o template.

As três aplicações que têm tela usam as views listadas abaixo. Moderar
comentário e gerenciar usuários passam pelo admin do Django, e
por isso aparecem como classes de `admin` nos diagramas, sem view própria.

**Tabela 19 — Classes de projeto por aplicação**

| Aplicação | Classe | Camada | Papel |
| --------------- | ---------------------------- | ---------- | ------------------------------------------- |
| `accounts` | `Profile` | Model | Dados públicos do usuário, ligados ao `User` |
| `accounts` | `SignUpForm` | Form | Valida nome de usuário, email e senha |
| `accounts` | `ProfileForm` | Form | Valida nome de exibição e biografia |
| `accounts` | `SignUpView` | View | Cria a conta e inicia a sessão |
| `accounts` | `ProfileDetailView` | View | Perfil público, com os textos publicados do autor |
| `accounts` | `ProfileUpdateView` | View | Edição do próprio perfil |
| `accounts` | `UserAdmin` | Admin | Gestão de contas pelo moderador, sem acesso a superusuário |
| `posts` | `Post` | Model | Texto, situação e datas; gera o slug ao gravar |
| `posts` | `PublishedManager` | Model | Devolve apenas os textos publicados |
| `posts` | `PostForm` | Form | Valida título e corpo |
| `posts` | `PostListView`, `PostDetailView` | View | Listagem pública, busca e página do texto |
| `posts` | `MyPostsView` | View | Textos do autor, em qualquer situação |
| `posts` | `AuthorRequiredMixin` | View | Confere a autoria antes de alterar um texto |
| `posts` | `PostCreateView`, `PostUpdateView`, `PostDeleteView` | View | Manutenção do texto pelo autor |
| `posts` | `PostStatusView` | View | Publica e despublica |
| `posts` | `PostAdmin` | Admin | Consulta dos textos pelo admin |
| `comments` | `Comment` | Model | Comentário, com a marca de aprovado |
| `comments` | `ApprovedManager` | Model | Devolve apenas os comentários aprovados |
| `comments` | `CommentForm` | Form | Valida corpo e tamanho |
| `comments` | `CommentCreateView` | View | Grava o comentário e volta ao texto |
| `comments` | `CommentAdmin` | Admin | Moderação de comentários |

Duas peças não são classes e completam o caminho. O sinal `create_profile`, em `accounts`, cria o perfil quando uma conta nasce. Os filtros `markdown` e `excerpt`, em `posts`, convertem e higienizam o corpo do texto na exibição.

Um conceito do domínio não vira necessariamente uma classe só. `Usuário` vira o `User` do Django mais um `Profile`, e `Post` traz junto um gerenciador de consulta que isola o que é publicado do que é rascunho.
