# Ataraxia — Plataforma de Blog Colaborativo

Prática Profissional em Análise e Desenvolvimento de Sistemas
Universidade Presbiteriana Mackenzie

O projeto será publicado em **blog.ataraxia.dev**.

As tarefas são acompanhadas no [quadro do projeto](https://github.com/orgs/ataraxia-ppads/projects/1).

## Integrantes

| Nome | Status |
| ---- | ------ |
| Alan Araujo Paiva | a confirmar |
| Gabriel Vieira Ferreira | confirmado |
| Pedro Emmanuel Esteves | confirmado |
| Rafaela Rarume Alves Perpetuo | confirmado |
| Renan Urtado Challó de Oliveira Jordão | confirmado |

## O que vamos construir

Uma plataforma de blog onde qualquer pessoa lê os textos publicados, usuários
cadastrados escrevem e publicam os seus, e moderadores cuidam do que sai do ar.

O recorte completo está em [`docs/visao-geral.md`](docs/visao-geral.md).

## Estado atual

O repositório tem o projeto Django, a configuração de ambiente e a documentação
de análise: interessados, objetivos, casos de uso e arquitetura.

As quatro aplicações — `accounts`, `posts`, `comments` e `taxonomy` — ainda não
foram criadas. Cada uma tem um dono, e a criação começa depois que o desenho
fechar.

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
python manage.py runserver
```

O painel de administração fica em `http://127.0.0.1:8000/admin/`. Para entrar,
crie um usuário com `python manage.py createsuperuser`.

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
| [`docs/casos-de-uso/`](docs/casos-de-uso/) | Atores, os 13 casos de uso e as descrições detalhadas |
| [`docs/arquitetura.md`](docs/arquitetura.md) | Decomposição em aplicações, dependências e stack |
| [`docs/design.md`](docs/design.md) | Decisões técnicas, custo de mudar cada uma e pendências |
| [`docs/roteiro-de-testes.md`](docs/roteiro-de-testes.md) | Verificação manual de cada caso de uso |

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
| Pedro *(placeholder)* | `taxonomy` | — | UC04 |

`taxonomy` e UC04 passam para o Alan assim que ele confirmar participação.

## Próximos passos

1. Revisar a documentação e propor correções por Pull Request.
2. Confirmar o integrante restante.
3. Definir o modelo de dados de cada aplicação.
4. Criar as quatro aplicações.
5. Escrever o documento da primeira entrega.
