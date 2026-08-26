# Como trabalhar no projeto

## Fluxo de trabalho

Ninguém escreve direto na `main`. Toda alteração entra por Pull Request, com
uma aprovação.

```
main  ←  PR  ←  1 aprovação  ←  sua branch
```

Nome da branch: `<área>/<descrição-curta>`, tudo minúsculo e com hífen.

```
posts/modelo-inicial
accounts/tela-de-cadastro
docs/roteiro-de-testes
```

O prefixo diz onde a alteração mexe sem precisar abrir o PR.

Passo a passo:

```bash
git switch main
git pull
git switch -c posts/modelo-inicial

# ... trabalhe, commite ...

git push -u origin posts/modelo-inicial
```

Depois é abrir o PR pelo GitHub, descrever o que fez e esperar a revisão. O
merge é sempre *squash*: seus commits viram um só na `main`, então não se
preocupe em ter um histórico bonito dentro da branch. A branch é apagada
automaticamente depois do merge.

Se um PR ficar parado, cobre no grupo. É melhor cobrar do que abrir uma segunda
branch em cima da primeira.

## Editar pelo navegador, sem instalar nada

Arquivos de texto — tudo em `docs/`, o `README.md`, este arquivo — podem ser
editados direto no site do GitHub, sem Python, sem Git e sem terminal.

1. Abra o arquivo no GitHub e clique no lápis, no canto superior direito.
2. Escreva.
3. Clique em **Commit changes**.
4. Escolha **Create a new branch for this commit and start a pull request**.
5. Confirme.

O GitHub cria a branch e abre o PR sozinho. É o mesmo fluxo de quem trabalha
pelo terminal, com os mesmos registros de autoria e revisão.

Para criar um arquivo novo, use o botão **Add file → Create new file** e digite
o caminho completo, com as barras: `docs/casos-de-uso/UC02.md`.

## Como revisar um Pull Request

Revisar não é só aprovar. Abra a aba **Files changed**, clique no `+` ao lado da
linha que quiser comentar e escreva ali. O comentário fica preso àquela linha, e
quem escreveu sabe exatamente do que você está falando.

No fim, **Review changes**:

- **Comment** — deixei observações, mas não estou barrando.
- **Request changes** — precisa mudar antes de entrar.
- **Approve** — pode entrar.

Discordar por escrito no PR é participação registrada no projeto. Concordar em
silêncio não é.

## Preparar o ambiente

Só para quem vai mexer em código. Uma vez, na sua máquina:

```bash
git clone https://github.com/ataraxia-ppads/ataraxia-blog.git
cd ataraxia-blog

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

Para rodar:

```bash
source .venv/bin/activate
python manage.py runserver
```

O painel de administração fica em `http://127.0.0.1:8000/admin/`.

Nenhuma configuração é obrigatória em desenvolvimento. Se precisar mudar algo,
copie `.env.example` para `.env` e edite.

## Convenção de idioma

O código é escrito em inglês; o que é lido por pessoas, em português.

**Em inglês:** pastas, arquivos, módulos, classes, funções, variáveis e campos
de modelo.

**Em português:** comentários, docstrings, documentação, mensagens de commit e
todo texto que aparece na tela para quem usa o site, incluindo as URLs.

Exemplo:

```python
class Post(models.Model):
    title = models.CharField('título', max_length=200)
    published_at = models.DateTimeField('publicado em', null=True, blank=True)

    # Um texto só aparece para o visitante depois de publicado.
    def is_visible(self):
        return self.status == Post.Status.PUBLISHED
```

## Referência entre aplicações

Um modelo de uma aplicação aponta para o de outra **por string**, sem `import`:

```python
class Post(models.Model):
    category = models.ForeignKey('taxonomy.Category', on_delete=models.PROTECT)
    tags = models.ManyToManyField('taxonomy.Tag', blank=True)
```

Isso não é preciosismo. Com `import`, quem escreve `posts` fica parado até
`taxonomy` existir. Com string, as quatro aplicações são escritas em paralelo,
em qualquer ordem.

## Cuidados com o repositório

- Não commitar `db.sqlite3`, `.env`, `.venv/` nem a pasta `media/`. O
  `.gitignore` já cobre os quatro, mas vale conferir antes do commit.
- Ao criar ou alterar um modelo, rodar `python manage.py makemigrations` e
  incluir o arquivo de migração no commit.
- Ao instalar uma biblioteca nova, atualizar o `requirements.txt` e avisar o
  grupo — todo mundo vai precisar reinstalar.
