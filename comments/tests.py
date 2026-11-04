"""Testes de comments, com o identificador do caso de teste do plano."""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post

from .models import MAX_LENGTH, Comment

User = get_user_model()


class CommentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user('ana', 'ana@example.com', 'Senha#forte1')
        cls.bruno = User.objects.create_user('bruno', 'bruno@example.com', 'Senha#forte2')

    def setUp(self):
        self.post = Post.objects.create(author=self.ana, title='Texto da Ana', body='Corpo.')
        self.post.publish()
        self.url = reverse('comments:create', args=[self.post.slug])

    def comment(self, body, **extra):
        return self.client.post(self.url, {'body': body, **extra})


class CreateTests(CommentTestCase):
    def test_ct10_02_sem_sessao_nada_e_gravado(self):
        response = self.comment('Anônimo')
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")
        self.assertFalse(Comment.objects.exists())

    def test_ct10_03_comentarios_encerrados(self):
        self.post.allow_comments = False
        self.post.save()
        self.client.force_login(self.bruno)
        page = self.client.get(self.post.get_absolute_url())
        self.assertContains(page, 'não aceita novos comentários')
        self.assertNotContains(page, 'name="body"')
        self.comment('Tentando mesmo assim')
        self.assertFalse(Comment.objects.exists())

    def test_ct10_04_vazio_e_so_espacos(self):
        self.client.force_login(self.bruno)
        for body in ['', '    ']:
            self.assertEqual(self.comment(body).status_code, 400)
        self.assertFalse(Comment.objects.exists())

    def test_ct10_05_limite_de_tamanho(self):
        self.client.force_login(self.bruno)
        self.comment('a' * MAX_LENGTH)
        self.assertEqual(Comment.objects.count(), 1)
        too_long = 'b' * (MAX_LENGTH + 1)
        response = self.comment(too_long)
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, too_long, status_code=400)
        self.assertEqual(Comment.objects.count(), 1)

    def test_ct10_06_texto_despublicado_durante_a_escrita(self):
        self.client.force_login(self.bruno)
        self.client.get(self.post.get_absolute_url())
        self.post.unpublish()
        response = self.client.post(self.url, {'body': 'Cheguei tarde'}, follow=True)
        self.assertContains(response, 'não está mais disponível')
        self.assertFalse(Comment.objects.exists())

    def test_ct10_07_marcacao_exibida_como_texto(self):
        self.client.force_login(self.bruno)
        self.comment('<script>alert(1)</script>')
        page = self.client.get(self.post.get_absolute_url())
        self.assertContains(page, '&lt;script&gt;alert(1)&lt;/script&gt;')
        self.assertNotContains(page, '<script>alert(1)</script>')

    def test_ct10_08_autor_forjado_e_ignorado(self):
        self.client.force_login(self.bruno)
        self.comment('Quem escreveu?', author=self.ana.pk, approved='')
        comment = Comment.objects.get()
        self.assertEqual(comment.author, self.bruno)
        self.assertTrue(comment.approved)


class ModerationTests(CommentTestCase):
    def test_ct11_02_reaprovar_volta_a_exibir(self):
        comment = Comment.objects.create(post=self.post, author=self.bruno, body='Polêmico')
        moderator = User.objects.create_superuser('moderador', 'm@example.com', 'Senha#forte3')
        self.client.force_login(moderator)
        changelist = reverse('admin:comments_comment_changelist')
        for action, visible in [('disapprove', False), ('approve', True)]:
            self.client.post(changelist, {'action': action, '_selected_action': [comment.pk]})
            page = Client().get(self.post.get_absolute_url())
            self.assertEqual('Polêmico' in page.content.decode(), visible)


class SecurityTests(CommentTestCase):
    def test_ctn03_post_sem_token_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.bruno)
        response = client.post(self.url, {'body': 'Sem token'})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Comment.objects.exists())
