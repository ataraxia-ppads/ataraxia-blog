# Introdução

Este documento apresenta a análise e o desenho do **Ataraxia**, plataforma de
blog desenvolvida como projeto do componente Prática Profissional em Análise e
Desenvolvimento de Sistemas da Universidade Presbiteriana Mackenzie.

É a segunda versão. A primeira registrou o levantamento: interessados,
objetivos, casos de uso e a decomposição do sistema em aplicações. Esta revisa
aqueles itens e acrescenta o desenho da solução, com modelo de domínio,
diagramas de sequência de sistema, protótipos de tela, diagramas de classes de
projeto e diagramas de sequência de projeto.

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

Registrar o entendimento do problema e o desenho da solução antes de escrever
código: quem são os interessados, o que o sistema precisa fazer, como precisa se
comportar, quais são os casos de uso, que conceitos o domínio tem, como as telas
se organizam e quais classes vão executar cada fluxo.

O que está aqui é ponto de partida para as entregas seguintes, e muda conforme
o desenvolvimento revelar o que não foi previsto.

## Organização do documento

1. **Introdução** — identificação do projeto e dos integrantes, endereços do
   repositório e do quadro de acompanhamento.
2. **Visão geral** — o sistema e os interessados.
3. **Objetivos** — funcionais e não-funcionais.
4. **Casos de uso** — atores, diagrama, relação dos casos de uso e descrição
   detalhada dos principais.
5. **Modelo de domínio** — conceitos do negócio, associações e ciclo de vida do
   texto.
6. **Diagramas de sequência de sistema** — as operações que o usuário dispara,
   com o sistema tratado como caixa preta.
7. **Protótipos de tela** — o que cada tela apresenta e onde.
8. **Arquitetura da solução** — decomposição em aplicações, dependências e
   tecnologias.
9. **Diagramas de classes de projeto** — as classes que vão existir no código,
   por aplicação.
10. **Diagramas de sequência de projeto** — os mesmos fluxos do capítulo 6, agora
    com as classes que os executam.
11. **Próximos passos.**

## Identificação do projeto

- **Título:** Ataraxia
- **Repositório de código-fonte:** `github.com/ataraxia-ppads/ataraxia-blog`
- **Quadro de acompanhamento:** `github.com/orgs/ataraxia-ppads/projects/1`
- **Publicação prevista:** `blog.ataraxia.dev`

## Integrantes do grupo

- Felipe Amorim
- Gabriel Vieira Ferreira
- Pedro Emmanuel Esteves
- Rafaela Rarume Alves Perpetuo
- Renan Urtado Challó de Oliveira Jordão
