# Construção

A construção foi feita em duas iterações, cada uma identificada por uma tag no repositório de código-fonte. O passo a passo para executar o sistema em Windows, macOS e Linux está no `README.md` do repositório.

**Tabela 20 — Iterações da construção**

| Tag | O que entregou | Testes |
| ------ | ------------------------------------------------------------ | ---------- |
| `v1` | As três aplicações e os onze casos de uso, com as telas do caminho de visitante e de autor e a moderação pelo admin | 57 |
| `v2` | Verificação contra o plano de testes: os 23 casos que eram manuais viraram testes automatizados, e os objetivos ONF02 e ONF07 ganharam teste. README com instruções detalhadas de execução | 83 |

## Alterações desde a segunda versão

A segunda versão foi escrita antes do código. Parte das alterações veio de decisões de projeto, tomadas ao escrever o plano de testes. A outra parte apareceu na construção, quando o código tomou um caminho melhor que o desenho, e nesses casos o documento foi corrigido para descrever o que existe.

**Tabela 21 — Alterações registradas nesta versão**

| Origem | Alteração | Motivo |
| ---------------- | ---------------------------------------- | ---------------------------------------- |
| Decisão de projeto | Categorias e tags saem do escopo: saem o objetivo de organizar por categoria, UC04, UC12 e a aplicação `taxonomy`, e UC03 passa a ter descrição detalhada | A busca no título e no corpo cobre a navegação, e classificar o conteúdo exigiria um cadastro que nenhum outro caso de uso aproveitaria. Os identificadores de caso de uso não foram renumerados |
| Decisão de projeto | `allow_comments` em `Post`, com a regra RN17 | O fluxo A2 de UC10 previa comentários encerrados, mas nenhum campo os representava |
| Decisão de projeto | `UserAdmin` restrito, com a regra RN18 | No admin padrão, quem altera usuários pode tornar-se superusuário |
| Decisão de projeto | Busca no título e no corpo, e limite de 2.000 caracteres no comentário | Os dois valores estavam indefinidos, e sem eles não havia como escrever o caso de teste |
| Construção | UC02 ganha o fluxo A3: o autor lê o próprio rascunho. `PostDetailView` parte de `Post.objects` e confere `is_visible_to()` | Consultar só `Post.published` impediria o autor de pré-visualizar o rascunho |
| Construção | Novas classes: `ProfileForm`, `ProfileDetailView`, `MyPostsView`, `AuthorRequiredMixin`, `PostStatusView` e `PostAdmin` | Atendem UC07, UC08 e UC09, que não têm diagrama detalhado. O mixin concentra a verificação de autoria em um só lugar |
| Construção | O perfil nasce pelo sinal `create_profile`, e não pelo formulário de cadastro | Vale também para contas criadas pelo admin e pelo `createsuperuser` |
| Construção | O slug é gerado em `Post.save()`, e não no formulário | A regra fica no modelo e vale para qualquer gravação |
| Construção | `CommentCreateView` é uma `View` com `post()`, e não uma `CreateView` | O erro de validação reexibe a página do texto, que pertence a outra aplicação |
| Construção | `ApprovedManager` é exposto como `Comment.visible` | O nome `approved` já é o do campo |
| Construção | Dependências entre aplicações redesenhadas | As views importam modelos e formulários de outras aplicações, o que a figura anterior não mostrava |
| Construção | Corpo do texto em markdown, higienizado com `nh3` | O autor formata sem editor visual, e nenhuma marcação fora de uma lista fechada chega à página |
| Construção | Telas sem protótipo e aparência definida | Entrada, perfil, confirmação de exclusão e páginas de erro entraram na construção, e os estilos estão em `static/css/ataraxia.css` |

## Verificação

O plano de testes revisado, com os casos, a rastreabilidade e o registro completo da execução, está em `docs/plano-de-testes.md` no repositório.

**Tabela 22 — Resultado das verificações na tag `v2`**

| Verificação | Resultado |
| ------------------------------ | ------------------------------------------------------------ |
| Testes automatizados | 83 testes, todos aprovados, em Windows 11 e em Linux |
| Estilo PEP 8 | Nenhuma violação |
| Migrações em dia | Nenhuma alteração pendente |
| Verificação contínua | Testes, estilo e migrações aprovados no GitHub Actions, em Ubuntu com Python 3.14 |
| Instruções do `README.md` | Seguidas em clone novo e ambiente virtual novo, com o sistema respondendo no navegador |

Continuam pendentes os casos que dependem de um navegador real: CTN01 (tela de 360 pixels), CTN11 (contraste e teclado), a parte de macOS e Firefox do CTN07 e o percurso de fumaça.
