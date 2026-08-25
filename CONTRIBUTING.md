# Como trabalhar no projeto

## Preparar o ambiente

Uma vez só, na sua máquina:

```bash
git clone <url-do-repositório>
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

O painel de administração fica em `http://127.0.0.1:8000/admin/`. Ainda não há
nenhuma outra página: o projeto tem só a configuração, e as aplicações serão
criadas depois.

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

## Cuidados com o repositório

- Não commitar `db.sqlite3`, `.env`, `.venv/` nem a pasta `media/`. O
  `.gitignore` já cobre os quatro, mas vale conferir antes do commit.
- Ao criar ou alterar um modelo, rodar `python manage.py makemigrations` e
  incluir o arquivo de migração no commit.
- Ao instalar uma biblioteca nova, atualizar o `requirements.txt` e avisar o
  grupo — todo mundo vai precisar reinstalar.

## Fluxo de trabalho

Ainda não definido. Como o grupo vai organizar tarefas, branches, revisão e
merge é assunto da primeira reunião com todos os integrantes.

Enquanto isso, combine antes de mexer em algo que outra pessoa esteja tocando.
