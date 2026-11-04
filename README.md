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

Segunda iteração da construção (tag `v2`). A primeira iteração (tag `v1`)
entregou as três aplicações, `accounts`, `posts` e `comments`: cadastro e
autenticação, perfil, escrita, publicação, leitura, busca e comentários, com a
moderação e a gestão de usuários pelo admin do Django.

A segunda iteração verifica o sistema contra o
[plano de testes](docs/plano-de-testes.md): os casos que eram só manuais e dá
para provar sem navegador viraram testes automatizados, e os objetivos não
funcionais de desempenho, acessibilidade e portabilidade passaram a ter teste.
A suíte foi de 57 para 83 testes. O resultado da execução está em
[`docs/plano-de-testes.md`](docs/plano-de-testes.md).

Os testes automatizados rodam a cada Pull Request, e a documentação de análise e
de desenho está em [`docs/`](docs/).

A hospedagem é tratada fora deste repositório e não interfere no
desenvolvimento: para rodar na sua máquina, basta o passo a passo abaixo.

## Versões e iterações

- Tag `v1`: código-fonte conforme a entrega da Iteração 1 da construção.
- Tag `v2`: código-fonte conforme a entrega da Iteração 2 da construção.
- Branch `iteracao2`: modificação de exercício em dois arquivos, integrada ao
  `main` pelo Pull Request #18 (a branch é mantida para conferência).
- Pull Request #19: código da Iteração 2, integrado ao `main`.

## Como rodar

Passo a passo para rodar o sistema no seu computador. Não é preciso instalar
banco de dados nem criar arquivo de configuração.

### 1. Pré-requisitos

| Item | Versão | Como conferir |
| ---- | ------ | ------------- |
| Python | 3.12 ou mais recente (a verificação contínua usa 3.14) | `python --version` |
| Git | qualquer versão recente | `git --version` |

No Windows, instale o Python em [python.org](https://www.python.org/downloads/)
marcando a opção **Add python.exe to PATH**. No macOS e no Linux, o comando
costuma ser `python3` em vez de `python`.

### 2. Baixar o código

```bash
git clone https://github.com/ataraxia-ppads/ataraxia-blog.git
cd ataraxia-blog
git checkout v2        # a versão da Iteração 2
```

### 3. Criar o ambiente virtual e instalar as dependências

Linux e macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se o PowerShell recusar o `Activate.ps1` por causa da política de execução, rode
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` e tente de
novo. No Prompt de Comando (cmd), use `.venv\Scripts\activate.bat`.

Com o ambiente ativo, o nome `(.venv)` aparece no começo da linha do terminal.

### 4. Preparar o banco e carregar os textos de exemplo

```bash
python manage.py migrate
python manage.py carregar_demo
```

O primeiro comando cria o banco SQLite (`db.sqlite3`, que não é versionado). O
segundo carrega 10 textos de demonstração, sendo 1 rascunho, e pode ser repetido
sem duplicar nada. Ele imprime `9 textos publicados, 1 rascunho(s).`

### 5. Subir o servidor

```bash
python manage.py runserver
```

Abra `http://127.0.0.1:8000/` no navegador. Para encerrar, volte ao terminal e
tecle `Ctrl+C`.

### 6. Experimentar o sistema

- **Ler e buscar:** a página inicial lista os textos publicados; o campo no topo
  busca no título e no corpo (experimente `ornitorrinco`).
- **Escrever:** clique em **Cadastrar-se**, crie uma conta (senha com 8 ou mais
  caracteres, nem só números nem comum) e use **Escrever**. Todo texto nasce
  rascunho; publique em **Meus textos**.
- **Moderar:** crie um administrador com `python manage.py createsuperuser` e
  entre em `http://127.0.0.1:8000/admin/`. Para dar a alguém o papel de
  moderador, marque nele o acesso ao admin e inclua-o no grupo `Moderadores`.

Os autores de demonstração (`helena`, `marcos`, `julia`) não têm senha: servem
só para assinar os textos.

### 7. Rodar os testes e as verificações

```bash
python manage.py test                              # 83 testes automatizados
pip install pycodestyle
python -m pycodestyle accounts posts comments config   # estilo PEP 8
python manage.py makemigrations --check --dry-run      # migrações em dia
```

A suíte leva cerca de meio minuto. O resultado esperado termina em `OK`.

### Problemas comuns

| Sintoma | Causa e solução |
| ------- | --------------- |
| `python` não é reconhecido | Use `python3` (macOS e Linux) ou `py` (Windows), ou reinstale o Python marcando o PATH |
| `No module named django` | O ambiente virtual não está ativo; repita o passo 3 |
| `Port is already in use` | Suba em outra porta: `python manage.py runserver 8001` |
| Página inicial vazia | Falta rodar `python manage.py carregar_demo` |

### Configuração opcional

Nenhuma configuração é obrigatória em desenvolvimento: sem `.env`, o projeto usa
SQLite e `DEBUG` ligado. Para mudar algo, copie `.env.example` para `.env` e
edite. As variáveis estão explicadas dentro do próprio arquivo.

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
| [`docs/construcao.md`](docs/construcao.md) | As duas iterações, as alterações desde a segunda versão e a verificação |
| [`docs/design.md`](docs/design.md) | Decisões técnicas, custo de mudar cada uma e pendências |
| [`docs/plano-de-testes.md`](docs/plano-de-testes.md) | Plano de testes revisado: casos, rastreabilidade e resultado da execução |
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

1. Percurso de fumaça no navegador e testes de usabilidade e portabilidade (CTN01, CTN07 e CTN11), pendentes no plano de testes.
2. Publicar em `blog.ataraxia.dev`.
3. Revisar o código por Pull Request e propor correções.
