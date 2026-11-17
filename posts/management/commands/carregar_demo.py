"""Carrega o conteúdo de demonstração descrito em docs/conteudo-demo.md.

    python manage.py carregar_demo

Pode ser rodado mais de uma vez: o que já existe é mantido. Os autores de
demonstração são os integrantes do grupo e não têm senha utilizável, então
ninguém entra com eles em produção; servem só para assinar os textos.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from comments.models import Comment
from posts.models import Post

TZ = ZoneInfo('America/Sao_Paulo')

AUTHORS = {
    'pedro': ('Pedro Emmanuel Esteves',
              'Do primeiro commit à publicação: posts, infraestrutura e a '
              'revisão do que entra no Ataraxia.'),
    'renan': ('Renan Jordão', 'Cuida de contas e da arquitetura do Ataraxia.'),
    'rafaela': ('Rafaela Rarume', 'Cuida dos diagramas, do quadro e do roteiro de testes.'),
    'felipe': ('Felipe Amorim', 'Cuida da busca do Ataraxia.'),
    'gabriel': ('Gabriel Vieira Ferreira', 'Cuida dos comentários do Ataraxia.'),
}

# Exigências do roteiro de testes: um rascunho, uma palavra incomum no título
# de um único texto (ornitorrinco), outra no corpo de outro (quimera), e datas
# de publicação diferentes entre si.
POSTS = [
    ('pedro', 'O que é o Ataraxia e por que um blog', (2026, 8, 24), [
        'O Ataraxia é uma plataforma de blog: qualquer pessoa lê, quem se cadastra '
        'escreve e moderadores cuidam do que sai do ar.',
        'Um blog é um bom objeto de estudo porque todo mundo sabe o que ele faz. Sobra '
        'atenção para a análise, o desenho, a construção e o teste.',
        'O nome vem do grego e quer dizer tranquilidade.',
    ]),
    ('renan', 'Por que Django para um blog pequeno', (2026, 9, 2), [
        'Um blog precisa de cadastro, autenticação e uma área de moderação. Nada disso '
        'precisa ser escrito do zero.',
        'O admin do Django resolve a moderação, e os validadores de senha resolvem a '
        'regra de robustez. Sobra tempo para o que é próprio do sistema: escrever, '
        'publicar, buscar e comentar.',
        'Três aplicações bastam: uma para contas, uma para textos e uma para '
        'comentários.',
    ]),
    ('rafaela', 'O ornitorrinco dos casos de uso', (2026, 9, 12), [
        'Todo levantamento tem um caso de uso que não se parece com os outros. Aqui é '
        'Gerenciar usuários: não tem tela própria, mora no admin e mesmo assim tem regra '
        'de negócio.',
        'Como o bicho que põe ovo e amamenta, ele não cabe em nenhuma gaveta. A saída é '
        'descrevê-lo pelo que o moderador pode e não pode fazer, e não pelas telas.',
        'O que não encaixa na classificação costuma ser o que mais precisa de descrição.',
    ]),
    ('rafaela', 'Protótipos em HTML antes de qualquer linha de Python', (2026, 9, 21), [
        'As telas principais podem ser desenhadas como wireframe em HTML e CSS, dentro '
        'do próprio repositório.',
        'Protótipo versionado é revisado como código: quem tem uma sugestão comenta na '
        'linha em que o botão aparece.',
        'Quando a construção começa, já se sabe onde fica cada coisa.',
    ]),
    ('pedro', 'O que a revisão por Pull Request ensina', (2026, 10, 1), [
        'Toda mudança passa por um par de olhos antes de entrar. Vale para código e vale '
        'para documentação.',
        'Manter os textos de análise em markdown, no mesmo lugar do código, permite '
        'contribuir pelo navegador, sem instalar nada.',
        'O histórico passa a contar a história do projeto: o que mudou, quando e por quê.',
    ]),
    ('felipe', 'Do caso de uso ao teste: como a busca foi construída', (2026, 10, 14), [
        'O caso de uso pede busca no título e no corpo, sem diferenciar maiúsculas, e '
        'com o termo preservado na troca de página.',
        'Cada frase dessas vira um caso de teste antes de virar código. São onze, '
        'contando o termo vazio e a página que não existe.',
        'Rascunho não entra no resultado nem na contagem.',
    ]),
    ('gabriel', 'Comentário é texto puro, e isso é uma decisão de segurança', (2026, 10, 23), [
        'Toda marcação enviada num comentário aparece na página como foi digitada. Quem '
        'manda uma tag de script vê a tag, e nada é executado.',
        'O vínculo do comentário com o autor vem da sessão e não do formulário. Mandar '
        'outro nome no envio não muda quem assinou.',
        'O autor do texto pode encerrar a discussão, e os comentários já feitos '
        'continuam visíveis.',
    ]),
    ('pedro', 'Esconder o botão não é autorização', (2026, 11, 4), [
        'Um autor só altera o que é seu. A tela não mostra o botão de editar no texto '
        'dos outros, mas isso não prova nada.',
        'Os testes de autorização enviam a requisição direto ao servidor. A resposta '
        'esperada é 403, e o texto continua onde estava.',
        'Tratar a interface como segurança é a velha quimera de todo sistema web. Quem '
        'decide é o servidor.',
    ]),
    ('renan', 'Testar antes de publicar: o que automatizar e o que olhar', (2026, 11, 15), [
        'Um plano de testes pode nascer direto dos casos de uso: cada fluxo vira pelo '
        'menos um caso, e cada regra de negócio ganha um teste que a exercita.',
        'Boa parte do que se confere à mão pode rodar sozinha. O cliente de teste do '
        'Django percorre as mesmas rotas e formulários do navegador.',
        'O que depende de ver a página, como a largura em tela pequena e o contraste, '
        'fica para um percurso curto antes de cada publicação.',
    ]),
    ('felipe', 'Rascunho: ideias para os próximos textos', None, [
        'Ainda organizando as ideias.',
    ]),
]

COMMENTS = [
    (1, 'gabriel', 'O admin pronto resolve boa parte da moderação.'),
    (1, 'rafaela', 'Uma pasta por aplicação deixa claro onde fica cada coisa.'),
    (5, 'pedro', 'Gostei da ideia de transformar cada frase do caso de uso em teste.'),
    (8, 'felipe', 'Roteiro manual curto é roteiro manual que alguém de fato segue.'),
]


class Command(BaseCommand):
    help = 'Carrega os textos de demonstração, sem apagar o que já existe.'

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        users = {}
        for username, (name, bio) in AUTHORS.items():
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_unusable_password()
                user.save()
            user.profile.display_name = name
            user.profile.bio = bio
            user.profile.save()
            users[username] = user

        posts = []
        for author, title, date, paragraphs in POSTS:
            post = Post.objects.filter(title=title).first()
            if post is None:
                post = Post.objects.create(
                    author=users[author], title=title, body='\n\n'.join(paragraphs)
                )
                if date:
                    post.published_at = datetime(*date, 9, 0, tzinfo=TZ)
                    post.save()
                    post.publish()
            posts.append(post)

        for index, author, body in COMMENTS:
            Comment.objects.get_or_create(post=posts[index], author=users[author], body=body)

        self.stdout.write(self.style.SUCCESS(
            f'{Post.published.count()} textos publicados, '
            f'{Post.objects.count() - Post.published.count()} rascunho(s).'
        ))
