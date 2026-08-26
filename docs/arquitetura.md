# Arquitetura da solução

## Decomposição em aplicações

O sistema é dividido em quatro aplicações Django. A fronteira de cada uma é o
conjunto de modelos que ela é dona.

**Tabela 12 — Aplicações**

| Aplicação | Modelos | Casos de uso |
| --------- | ------- | ------------ |
| `accounts` | `Profile` | UC05, UC06, UC07, UC13 |
| `posts` | `Post` | UC01, UC02, UC03, UC08, UC09 |
| `comments` | `Comment` | UC10, UC11 |
| `taxonomy` | `Category`, `Tag` | UC04, UC12 |

Não há uma aplicação separada para leitura. Ler um texto publicado é a face
pública de `posts`, e uma aplicação sem modelo próprio seria apenas uma pasta de
views importando os modelos de outra.

`accounts` não define um usuário próprio: usa o `User` do `django.contrib.auth`
e estende com um `Profile` ligado a ele. Substituir o modelo de usuário do
Django é decisão cara e irreversível depois da primeira migração, e nada no
escopo exige isso.

## Dependências

```
comments  ──▶  posts, accounts
posts     ──▶  taxonomy
accounts  ──▶  (nenhuma)
```

As referências entre aplicações são feitas por string, sem `import`:

```python
class Post(models.Model):
    category = models.ForeignKey('taxonomy.Category', on_delete=models.PROTECT)
    tags = models.ManyToManyField('taxonomy.Tag', blank=True)
```

Com `import`, a ordem do grafo viraria ordem de trabalho e as pessoas ficariam
em fila. Com string, as quatro aplicações são escritas em paralelo.

## Interface de moderação

UC11, UC12 e UC13 — moderar comentário, manter taxonomia e gerenciar usuários —
usam o **admin do Django**, sem telas próprias.

É registrado aqui porque é uma decisão, não uma omissão. O admin já entrega
listagem, busca, filtros, permissões por grupo e registro de alterações para
qualquer modelo cadastrado. Escrever telas equivalentes consumiria a maior parte
do esforço do semestre para atender três casos de uso que só moderadores veem.

As telas próprias ficam concentradas no caminho de visitante e autor, que é onde
a interface é o produto.

## Camadas

```
navegador
    │
    ▼
URLs  ──▶  Views  ──▶  Models  ──▶  banco de dados
             │
             ▼
         Templates
```

Sem front-end separado. As páginas são templates do Django renderizados no
servidor. A decisão evita que a equipe precise aprender um segundo framework e
uma segunda linguagem para entregar telas simples.

## Stack

**Tabela 13 — Tecnologias**

| Camada | Escolha | Motivo |
| ------ | ------- | ------ |
| Linguagem | Python 3.14 | Base do Django |
| Framework | Django 6.1 | Python 3.14 exige a série 6.x; as 5.x não o suportam |
| Banco em desenvolvimento | SQLite | Acompanha o Django, dispensa instalação em cada máquina |
| Banco em produção | PostgreSQL | Não fica preso aos limites do SQLite em escrita concorrente |
| Interface | Templates do Django | Sem segundo framework |
| Arquivos estáticos | WhiteNoise | Serve estáticos sem depender de servidor web separado |
| Versionamento | Git e GitHub | |

A troca entre SQLite e PostgreSQL é feita pela variável de ambiente
`DATABASE_URL`. Sem ela, o projeto usa SQLite; com ela, o banco apontado. O
código é o mesmo nos dois casos, o que permite que cada integrante trabalhe sem
instalar banco algum.
