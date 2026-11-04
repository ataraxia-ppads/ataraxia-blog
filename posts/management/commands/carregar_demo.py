"""Carrega o conteúdo de demonstração descrito em docs/conteudo-demo.md.

    python manage.py carregar_demo

Pode ser rodado mais de uma vez: o que já existe é mantido. Os autores de
demonstração não têm senha utilizável, então ninguém entra com eles em
produção; servem só para assinar os textos.
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
    'helena': ('Helena Prado', 'Desenvolvedora backend. Escreve sobre Python e carreira.'),
    'marcos': ('Marcos Tavares', 'Professor de matemática que aprendeu a programar aos 40.'),
    'julia': ('Júlia Nogueira', 'Analista de dados e leitora compulsiva.'),
}

# Exigências do roteiro de testes: um rascunho, uma palavra incomum no título
# de um único texto (ornitorrinco), outra no corpo de outro (quimera), e datas
# de publicação diferentes entre si.
POSTS = [
    ('helena', 'Por que aprendi Python antes de qualquer outra linguagem', (2026, 3, 14), [
        'Quando decidi mudar de área, a primeira pergunta foi por onde começar. Havia '
        'listas com dez linguagens, e cada uma prometia ser a definitiva.',
        'Escolhi Python por um motivo pouco romântico: era a que tinha mais material em '
        'português. Aprender programação já é difícil o bastante sem somar a barreira do '
        'idioma a cada dúvida.',
        'Dois anos depois a escolha se provou certa por outro motivo. A comunidade é '
        'grande, então toda dúvida que tive alguém já teve antes, e escreveu a resposta.',
    ]),
    ('marcos', 'O que o ornitorrinco ensina sobre classificar as coisas', (2026, 4, 2), [
        'Quando o primeiro ornitorrinco empalhado chegou à Europa, os naturalistas acharam '
        'que era fraude: bico de pato costurado num corpo de castor.',
        'O bicho não cabia em nenhuma gaveta. Põe ovos como réptil, amamenta como '
        'mamífero, tem veneno como poucos animais têm.',
        'Toda classificação é uma aposta sobre o que importa. Quando aparece um caso que '
        'não cabe, o problema raramente é o caso.',
    ]),
    ('julia', 'Três livros que mudaram meu jeito de ler dados', (2026, 4, 20), [
        'Não são livros técnicos. Nenhum ensina uma ferramenta, e talvez por isso tenham '
        'durado mais do que qualquer curso que fiz.',
        'O primeiro me ensinou a desconfiar de média. O segundo, a desenhar antes de '
        'calcular. O terceiro, a perguntar quem coletou o dado e por quê.',
        'Se tivesse que escolher um só, ficaria com o terceiro. Todo número tem autor.',
    ]),
    ('helena', 'Testes automatizados não são burocracia', (2026, 5, 9), [
        'Durante muito tempo achei que escrever teste era trabalho dobrado: o código e '
        'depois a prova de que o código funciona.',
        'Mudei de ideia no dia em que uma alteração pequena quebrou o cadastro, e só '
        'descobri porque um teste antigo, que eu nem lembrava de ter escrito, falhou.',
        'Teste bom não prova que o sistema funciona. Ele avisa, cedo, quando deixou de '
        'funcionar.',
    ]),
    ('marcos', 'Aprender a programar depois dos quarenta', (2026, 5, 27), [
        'A pergunta que mais ouço é se não é tarde. Não é, mas também não é igual a '
        'aprender aos vinte.',
        'Tenho menos tempo e menos paciência para tutorial longo. Em compensação, sei '
        'reconhecer quando não entendi algo, e isso economiza semanas.',
        'O conselho que dou é o mesmo que daria a qualquer idade: escreva um programa '
        'pequeno que resolva um problema seu.',
    ]),
    ('julia', 'Gráfico de pizza quase nunca é a melhor escolha', (2026, 6, 15), [
        'O olho humano compara comprimentos muito melhor do que ângulos. Por isso duas '
        'fatias parecidas numa pizza viram um palpite.',
        'Uma barra horizontal ordenada resolve a maioria dos casos, e ainda deixa espaço '
        'para escrever o nome de cada categoria por extenso.',
        'A pizza tem um uso honesto: mostrar que uma parte é quase o todo. Fora disso, '
        'prefira barras.',
    ]),
    ('helena', 'Como escrevo mensagens de commit', (2026, 7, 3), [
        'A mensagem de commit é a única documentação que acompanha cada mudança para '
        'sempre. Vale os trinta segundos que custa.',
        'Escrevo a primeira linha dizendo o que muda, no presente, e deixo o corpo para o '
        'porquê. O como já está no próprio diff.',
        'Quando não consigo resumir a mudança numa linha, quase sempre é sinal de que '
        'ela deveria ser dois commits.',
    ]),
    ('marcos', 'Matemática para quem programa', (2026, 8, 12), [
        'Não é preciso cálculo para fazer um site. Mas algumas ideias aparecem o tempo '
        'todo, e vale conhecê-las pelo nome.',
        'Conjuntos explicam boa parte do que um banco de dados faz. Lógica explica os '
        'ifs. Contagem explica por que um algoritmo fica lento.',
        'Para o resto, há a velha quimera do programador que sabe tudo antes de começar. '
        'Ninguém sabe. Aprende-se no caminho.',
    ]),
    ('julia', 'Dados abertos e o que fazer com eles', (2026, 9, 1), [
        'O portal de dados abertos da sua cidade provavelmente tem mais coisa do que '
        'você imagina: horários de ônibus, licitações, atendimentos de saúde.',
        'O difícil não é achar o dado, é fazer a pergunta certa. Comece por algo que '
        'incomoda você no dia a dia.',
        'Publique o resultado, mesmo que pequeno. Dado aberto que ninguém lê continua '
        'fechado na prática.',
    ]),
    ('helena', 'Rascunho: notas sobre revisão de código', None, [
        'Ainda organizando as ideias. Revisão de código é conversa, não fiscalização.',
    ]),
]

COMMENTS = [
    (0, 'marcos', 'Material em português foi decisivo para mim também.'),
    (0, 'julia', 'E a comunidade continua sendo o melhor argumento.'),
    (1, 'julia', 'Nunca mais vou olhar para uma taxonomia do mesmo jeito.'),
    (3, 'marcos', 'O teste que você esqueceu que escreveu é o melhor tipo de teste.'),
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
