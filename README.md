# Ataraxia — Plataforma de Blog Colaborativo

Prática Profissional em Análise e Desenvolvimento de Sistemas
Universidade Presbiteriana Mackenzie

O projeto será publicado em **blog.ataraxia.dev**.

As tarefas são acompanhadas no [quadro do projeto](https://github.com/orgs/ataraxia-ppads/projects/1).

## Integrantes

| Nome |
| ---- |
| Felipe Amorim |
| Gabriel Vieira Ferreira |
| Pedro Emmanuel Esteves |
| Rafaela Rarume Alves Perpetuo |
| Renan Urtado Challó de Oliveira Jordão |

## O que vamos construir

Uma plataforma de blog onde qualquer pessoa lê os textos publicados, usuários
cadastrados escrevem e publicam os seus, e moderadores cuidam do que sai do ar.

O recorte completo está em [`docs/visao-geral.md`](docs/visao-geral.md).

## Estado atual

Primeira iteração da construção. As três aplicações, `accounts`, `posts` e
`comments`, estão implementadas: cadastro e autenticação, perfil, escrita,
publicação, leitura, busca e comentários, com a moderação e a gestão de usuários
pelo admin do Django.

Os testes automatizados rodam a cada Pull Request, e a documentação de análise e
de desenho está em [`docs/`](docs/).

A hospedagem é tratada fora deste repositório e não interfere no
desenvolvimento: para rodar na sua máquina, basta o passo a passo abaixo.

## Como rodar

```bash
git clone https://github.com/ataraxia-ppads/ataraxia-blog.git
cd ataraxia-blog

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py carregar_demo   # textos de exemplo, opcional
python manage.py runserver
```

O site abre em `http://127.0.0.1:8000/`. Para rodar os testes:

```bash
python manage.py test
```

O painel de administração fica em `http://127.0.0.1:8000/admin/`. Para entrar,
crie um usuário com `python manage.py createsuperuser`. Para dar a alguém o papel
de moderador, marque nele o acesso ao admin e inclua-o no grupo `Moderadores`.

Nenhuma configuração é obrigatória em desenvolvimento. Se precisar mudar algo,
copie `.env.example` para `.env` e edite.

Para contribuir sem instalar nada, editando texto pelo navegador, veja o
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Documentação

| Arquivo | Conteúdo |
| ------- | -------- |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Fluxo de trabalho, revisão de PR e convenção de idioma |
| [`docs/introducao.md`](docs/introducao.md) | Contexto, objetivo do documento e identificação do projeto |
| [`docs/visao-geral.md`](docs/visao-geral.md) | O sistema, os interessados e o que está fora do escopo |
| [`docs/objetivos.md`](docs/objetivos.md) | Objetivos funcionais e não-funcionais |
| [`docs/casos-de-uso/`](docs/casos-de-uso/) | Atores, os 11 casos de uso e as descrições detalhadas |
| [`docs/modelo-de-dominio.md`](docs/modelo-de-dominio.md) | Conceitos do negócio, associações e ciclo de vida do texto |
| [`docs/sequencia-de-sistema.md`](docs/sequencia-de-sistema.md) | Operações de sistema de cada caso de uso principal |
| [`docs/prototipos/`](docs/prototipos/) | Wireframes das cinco telas, com a fonte em HTML |
| [`docs/arquitetura.md`](docs/arquitetura.md) | Decomposição em aplicações, dependências e stack |
| [`docs/classes-de-projeto/`](docs/classes-de-projeto/) | As classes de cada aplicação, por camada |
| [`docs/sequencia-de-projeto/`](docs/sequencia-de-projeto/) | Os mesmos fluxos, com as classes que os executam |
| [`docs/design.md`](docs/design.md) | Decisões técnicas, custo de mudar cada uma e pendências |
| [`docs/roteiro-de-testes.md`](docs/roteiro-de-testes.md) | Verificação manual de cada caso de uso |
| [`docs/conteudo-demo.md`](docs/conteudo-demo.md) | Textos de exemplo que povoam o blog para demonstração e teste |

## Stack

| Item | Escolha |
| ---- | ------- |
| Linguagem | Python 3 |
| Framework | Django 6.1 |
| Banco | SQLite em desenvolvimento |
| Banco (produção) | PostgreSQL |
| Front-end | Templates do Django |
| Versionamento | Git e GitHub |
| Publicação | `blog.ataraxia.dev` |

## Divisão do trabalho

| Pessoa | Aplicação | Fora do código | Caso de uso |
| ------ | --------- | -------------- | ----------- |
| Pedro | `posts` | Configuração, template base, documento | UC08 |
| Renan | `accounts` | Arquitetura e conteúdo dos diagramas | UC05 |
| Gabriel | `comments` | — | UC10 |
| Rafaela | — | Diagramas, quadro, roteiro de testes, conteúdo de demonstração | UC02 |
| Felipe | `posts` | Busca | UC03 |

## Próximos passos

1. Executar o roteiro de testes manuais sobre a versão publicada.
2. Publicar em `blog.ataraxia.dev`.
3. Revisar o código por Pull Request e propor correções.
