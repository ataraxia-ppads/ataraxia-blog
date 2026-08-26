# Introdução

Este documento apresenta a análise inicial do **Ataraxia**, plataforma de blog
desenvolvida como projeto do componente Prática Profissional em Análise e
Desenvolvimento de Sistemas da Universidade Presbiteriana Mackenzie.

## Contexto

Publicar textos na internet hoje passa, quase sempre, por plataformas de
terceiros. Quem escreve aceita as regras de quem hospeda: o alcance depende de
um algoritmo que não controla, o endereço do texto pertence a outra empresa, e
o conteúdo pode ser removido ou tornado inacessível sem aviso.

O Ataraxia é uma plataforma de blog em que a equipe mantém a hospedagem, o
domínio e as regras de moderação. Qualquer pessoa lê os textos publicados sem
precisar de conta; usuários cadastrados escrevem, editam e publicam os seus; e
moderadores cuidam do que permanece no ar.

## Objetivo do documento

Registrar o entendimento do problema antes de escrever código: quem são os
interessados, o que o sistema precisa fazer, como precisa se comportar, quais
são os casos de uso e como o sistema se divide em partes.

O que está aqui é ponto de partida para as entregas seguintes, e muda conforme
o desenvolvimento revelar o que não foi previsto.

## Organização do documento

1. **Introdução** — identificação do projeto e dos integrantes, endereços do
   repositório e do quadro de acompanhamento.
2. **Visão geral** — o sistema, os interessados e a delimitação do escopo.
3. **Objetivos** — funcionais e não-funcionais.
4. **Casos de uso** — atores, diagrama, relação dos casos de uso e descrição
   detalhada dos principais.
5. **Arquitetura da solução** — decomposição em aplicações, dependências e
   tecnologias.
6. **Próximos passos.**

## Identificação do projeto

- **Título:** Ataraxia
- **Repositório de código-fonte:** `github.com/ataraxia-ppads/ataraxia-blog`
- **Quadro de acompanhamento:** `github.com/orgs/ataraxia-ppads/projects/1`
- **Publicação prevista:** `blog.ataraxia.dev`
