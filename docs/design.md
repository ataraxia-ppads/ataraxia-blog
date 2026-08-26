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

O projeto Django em `config/`, a configuração de ambiente e a documentação de
análise.

As quatro aplicações ainda não foram criadas. A ordem prevista é o desenho
fechar, cada dono criar a sua e os modelos entrarem em seguida.

## O que não foi decidido

- Modelo de dados detalhado: campos, tipos e restrições de cada modelo.
- Aparência: layout, paleta, tipografia.
- Estratégia de testes automatizados.
- Como e quando o sistema vai ao ar.

## O que a primeira entrega exige

| Item | Situação |
| ---- | -------- |
| Título do projeto | Ataraxia |
| Nomes dos integrantes | Quatro confirmados de cinco |
| URL do repositório de código-fonte | `github.com/ataraxia-ppads/ataraxia-blog` |
| URL do quadro de acompanhamento | A criar |
| Interessados | [`visao-geral.md`](visao-geral.md) |
| Objetivos funcionais | [`objetivos.md`](objetivos.md) |
| Objetivos não-funcionais | [`objetivos.md`](objetivos.md) |
| Diagrama de casos de uso | [`casos-de-uso/`](casos-de-uso/) |
| Descrição detalhada dos casos de uso principais | [`casos-de-uso/`](casos-de-uso/) |

## Como comentar

Discordância é bem-vinda, principalmente nas linhas de custo baixo da tabela
acima. Comente no Pull Request, na linha exata do trecho, e não em conversa
paralela — comentário preso ao texto fica registrado e não se perde.
