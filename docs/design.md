# Decisões técnicas e pendências

Prática Profissional em Análise e Desenvolvimento de Sistemas
Universidade Presbiteriana Mackenzie

Registro do que já foi decidido, com o custo de voltar atrás em cada ponto, e do
que continua em aberto. A análise do sistema está nos documentos vizinhos:
[`visao-geral.md`](visao-geral.md), [`objetivos.md`](objetivos.md),
[`casos-de-uso/`](casos-de-uso/) e [`arquitetura.md`](arquitetura.md).

## Decisões tomadas

A coluna da direita indica onde a discussão ainda vale o tempo.

| Decisão | Motivo | Custo de mudar |
| ------- | ------ | -------------- |
| Python com Django 6.1 | Domínio de blog é onde o framework tem mais material pronto e documentação em português | Alto — é a base de tudo |
| Templates do Django, sem front-end separado | Evita que o grupo precise aprender um segundo framework | Médio, enquanto não houver telas |
| Quatro aplicações: `accounts`, `posts`, `comments`, `taxonomy` | Cada integrante é dono de uma; conflito de merge fica raro por construção | Médio |
| Referência entre aplicações por string | Permite escrever as quatro em paralelo, sem ordem imposta | Baixo |
| Moderação pelo admin do Django | Três casos de uso atendidos sem escrever tela | Baixo — os modelos já existem |
| SQLite em desenvolvimento, PostgreSQL em produção | Cada integrante roda sem instalar banco | Baixo — é uma variável de ambiente |
| Configuração por variáveis de ambiente | Permite publicar sem alterar código versionado | Baixo |
| Identificadores em inglês, prosa em português | Consistência; o código estava misturando os dois | Baixo, enquanto o código é pequeno |
| Publicar em `blog.ataraxia.dev` | Domínio já pertence à equipe, sem custo adicional | Baixo — é um subdomínio |
| `main` protegida, alteração só por Pull Request | Registra revisão e participação de cada integrante | Baixo |

Python 3.14 exige Django 6.x; as séries 5.x não o suportam. A versão está
fixada no `requirements.txt`.

Sobre a configuração: `SECRET_KEY`, `DEBUG`, hosts permitidos e origens
confiáveis vêm do ambiente, com valores de desenvolvimento como padrão. Sem
`DEBUG`, a `SECRET_KEY` passa a ser obrigatória e o projeto se recusa a subir
sem ela. Locale em `pt-br`, fuso `America/Sao_Paulo`.

## O que já existe no repositório

O projeto Django em `config/`, a configuração de ambiente, a documentação de
análise e a de desenho: modelo de domínio, diagramas de sequência de sistema,
protótipos de tela, classes de projeto e diagramas de sequência de projeto.

As quatro aplicações ainda não foram criadas. O desenho fechou, e a ordem
prevista agora é cada dono criar a sua aplicação e implementar os modelos como
descritos em `classes-de-projeto/`.

## Fora do escopo

Fica registrado aqui, e não no documento da entrega, porque o enunciado não
pede delimitação de escopo. Serve ao grupo: evita cobrança futura sobre o que
nunca foi prometido.

- Editor de texto rico com formatação visual. Os textos são escritos em
  markdown.
- Notificações por e-mail.
- Aplicativo móvel. O acesso é pelo navegador, com layout responsivo.
- Múltiplos blogs ou múltiplos autores por texto.
- Métricas e painéis de audiência.

## O que não foi decidido

- Aparência: paleta, tipografia e espaçamento. Os protótipos definem estrutura
  de tela, não desenho visual.
- Estratégia de testes automatizados. Hoje há apenas o roteiro manual.
- Tamanho máximo do corpo do comentário, que RN15 exige mas ainda não fixa.
- Como e quando o sistema vai ao ar.

## O que a primeira entrega exige

| Item | Situação |
| ---- | -------- |
| Título do projeto | Ataraxia |
| Nomes dos integrantes | Cinco |
| URL do repositório de código-fonte | `github.com/ataraxia-ppads/ataraxia-blog` |
| URL do quadro de acompanhamento | [`orgs/ataraxia-ppads/projects/1`](https://github.com/orgs/ataraxia-ppads/projects/1) |
| Interessados | [`visao-geral.md`](visao-geral.md) |
| Objetivos funcionais | [`objetivos.md`](objetivos.md) |
| Objetivos não-funcionais | [`objetivos.md`](objetivos.md) |
| Diagrama de casos de uso | [`casos-de-uso/`](casos-de-uso/) |
| Descrição detalhada dos casos de uso principais | [`casos-de-uso/`](casos-de-uso/) |

## O que a segunda entrega exige

Além dos itens acima, já revisados:

| Item | Situação |
| ---- | -------- |
| Protótipos de tela | [`prototipos/`](prototipos/) |
| Modelo de domínio | [`modelo-de-dominio.md`](modelo-de-dominio.md) |
| Diagramas de classes de projeto | [`classes-de-projeto/`](classes-de-projeto/) |
| Diagramas de sequência de projeto | [`sequencia-de-projeto/`](sequencia-de-projeto/) |

Os diagramas de sequência de sistema, em
[`sequencia-de-sistema.md`](sequencia-de-sistema.md), não constam da lista da
entrega escrita, e estão aqui porque são o que a atividade de modelagem pede e
porque sem eles os diagramas de sequência de projeto não teriam de onde sair.

## Como comentar

Discordância é bem-vinda, principalmente nas linhas de custo baixo da tabela
acima.

Para propor uma mudança, abra um Pull Request alterando o trecho. Para discutir
antes de alterar, comente na linha exata dentro de um Pull Request que toque
nela. Nos dois casos a conversa fica presa ao texto e registrada com nome e
data, o que não acontece em conversa paralela.
