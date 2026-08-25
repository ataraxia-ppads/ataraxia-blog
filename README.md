# Ataraxia — Plataforma de Blog Colaborativo

Prática Profissional em Análise e Desenvolvimento de Sistemas
Universidade Presbiteriana Mackenzie

O projeto será publicado em **blog.ataraxia.dev**.

## Integrantes

| Nome | Status |
| ---- | ------ |
| Alan Araujo Paiva | a confirmar |
| Gabriel Vieira Ferreira | a confirmar |
| Pedro Emmanuel Esteves | confirmado |
| Rafaela Rarume Alves Perpetuo | a confirmar |
| Renan Urtado Challó de Oliveira Jordão | confirmado |

## O que vamos construir

Uma plataforma de blog onde qualquer pessoa lê os textos publicados, usuários
cadastrados escrevem e publicam os seus, e moderadores cuidam do que sai do ar.

Essa é a ideia de partida, não um escopo fechado. O recorte definitivo —
interessados, objetivos funcionais e não-funcionais, casos de uso e arquitetura
de solução — sai do levantamento de requisitos, que ainda será feito.

## Estado atual

O repositório tem o projeto Django e a configuração de ambiente, e nada além
disso. As aplicações serão criadas quando a arquitetura de solução estiver
definida, porque a divisão em aplicações é resultado desse desenho.

A hospedagem é tratada fora deste repositório e não interfere no
desenvolvimento: para rodar na sua máquina, basta o passo a passo acima.

## Como rodar

```bash
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

## Stack

| Item | Escolha |
| ---- | ------- |
| Linguagem | Python 3 |
| Framework | Django 6.1 |
| Banco | SQLite em desenvolvimento |
| Front-end | Templates do Django |
| Banco (produção) | PostgreSQL |
| Versionamento | Git e GitHub |
| Publicação | `blog.ataraxia.dev` |

## Documentação

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — como preparar o ambiente e a
  convenção de idioma do código.
- [`docs/design.md`](docs/design.md) — decisões técnicas tomadas, com o custo de
  mudar cada uma, e o que ainda está em aberto.

## Próximos passos

1. Confirmar os três integrantes restantes.
2. Definir o fluxo de trabalho do grupo na primeira reunião.
3. Fazer o levantamento de requisitos e o desenho da arquitetura.
4. Criar as aplicações e distribuir o trabalho.
5. Escrever o documento da primeira entrega.
