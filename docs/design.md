# Ataraxia — ponto de partida técnico

Prática Profissional em Análise e Desenvolvimento de Sistemas
Universidade Presbiteriana Mackenzie

> Documento de partida, aberto a revisão. Foi escrito antes de o grupo se
> formar, para que houvesse algo concreto de onde discutir. O que está
> implementado é pouco e barato de refazer — se alguma decisão aqui atrapalhar
> o desenho da solução, ela muda.

## O projeto

Uma plataforma de blog: qualquer pessoa lê os textos publicados sem precisar de
conta, usuários cadastrados escrevem e publicam os seus, e moderadores cuidam
do que permanece no ar. Publicação em **blog.ataraxia.dev**, domínio que já
pertence à equipe.

Isso é a ideia de partida, não um escopo fechado. O recorte definitivo sai do
levantamento de requisitos.

## O que já existe no repositório

Um projeto Django em `config/` e a configuração de ambiente. Nada além disso.

Não há aplicações, modelos, telas nem rotas fora do admin. As pastas `static/`
e `templates/` estão vazias, apenas registradas na configuração.

A ausência de aplicações é deliberada: a decomposição do sistema em aplicações
é resultado do desenho de arquitetura, e desenhar isso é a próxima etapa.

## Decisões tomadas

A coluna da direita indica o custo de voltar atrás, para saber onde a discussão
vale o tempo.

| Decisão | Motivo | Custo de mudar |
| ------- | ------ | -------------- |
| Python com Django 6.1 | Domínio de blog é onde o framework tem mais material pronto e documentação em português | Alto — é a base de tudo |
| Templates do Django, sem front-end separado | Evita que o grupo precise aprender um segundo framework | Médio, enquanto não houver telas |
| SQLite em desenvolvimento | Acompanha o Django, dispensa instalação | Baixo |
| Configuração por variáveis de ambiente | Permite publicar sem alterar código versionado | Baixo |
| Identificadores em inglês, prosa em português | Consistência; o código estava misturando os dois | Baixo, enquanto o código é pequeno |
| Publicar em `blog.ataraxia.dev` | Domínio já pertence à equipe, sem custo adicional | Baixo — é um subdomínio |
| PostgreSQL em produção, SQLite em desenvolvimento | Cada integrante roda sem instalar banco; a produção não fica presa aos limites do SQLite | Baixo — é uma variável de ambiente |

Python 3.14 exige Django 6.x; as séries 5.x não o suportam. A versão está
fixada no `requirements.txt`.

Sobre a configuração: `SECRET_KEY`, `DEBUG`, hosts permitidos e origens
confiáveis vêm do ambiente, com valores de desenvolvimento como padrão. Sem
`DEBUG`, a `SECRET_KEY` passa a ser obrigatória e o projeto se recusa a subir
sem ela. Locale em `pt-br`, fuso `America/Sao_Paulo`.

## O que não foi decidido

Nada abaixo tem resposta ainda, e nenhuma delas está pré-julgada por este
documento:

- Interessados
- Objetivos funcionais e não-funcionais
- Casos de uso e o diagrama correspondente
- Decomposição do sistema em aplicações
- Modelo de dados
- Fluxo de trabalho do grupo: tarefas, branches, revisão e merge

## O que a primeira entrega exige

Para referência de quem for produzir a documentação:

| Item | Situação |
| ---- | -------- |
| Título do projeto | Definido: Ataraxia |
| Nomes dos integrantes | Dois confirmados de cinco |
| URL do repositório de código-fonte | A publicar |
| URL do quadro de acompanhamento | A criar |
| Interessados | Em aberto |
| Objetivos funcionais | Em aberto |
| Objetivos não-funcionais | Em aberto |
| Diagrama de casos de uso | Em aberto |
| Descrição detalhada dos casos de uso principais | Em aberto |

O documento também precisa de capa, sumário, lista de figuras, lista de tabelas
e introdução, organizado em capítulos.

## Como comentar

Discordância sobre qualquer ponto deste documento é bem-vinda, principalmente
nas linhas de custo baixo da tabela de decisões. O que estiver errado se muda
agora, enquanto custa pouco.
