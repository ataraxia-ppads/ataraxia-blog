"""Iteração 2: casos de UC05, UC06, UC07 e UC11 que eram só manuais."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from comments.models import Comment
from posts.models import Post

User = get_user_model()


class FlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user('ana', 'ana@example.com', 'Senha#forte1')

    def test_ct05_11_cadastro_tem_vinculo_para_quem_ja_tem_conta(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertContains(response, f'href="{reverse("accounts:login")}"')

    def test_ct06_01_entrar_mostra_o_nome_da_autora(self):
        response = self.client.post(reverse('accounts:login'),
                                    {'username': 'ana', 'password': 'Senha#forte1'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sair')
        self.assertContains(response, '>ana</a>')

    def test_ct06_05_depois_de_entrar_volta_ao_editor(self):
        editor = reverse('posts:create')
        response = self.client.get(editor)
        login_url = response['Location']
        self.assertEqual(login_url, f"{reverse('accounts:login')}?next={editor}")
        response = self.client.post(login_url, {
            'username': 'ana', 'password': 'Senha#forte1', 'next': editor,
        })
        self.assertRedirects(response, editor)

    def test_ct07_01_ct07_02_perfil_editado_aparece_no_perfil_publico(self):
        self.client.force_login(self.ana)
        self.client.post(reverse('accounts:profile_edit'),
                         {'display_name': 'Ana Souza', 'bio': 'Escrevo sobre café.'})
        self.client.logout()
        page = self.client.get(reverse('accounts:profile', args=['ana']))
        self.assertContains(page, 'Ana Souza')
        self.assertContains(page, 'Escrevo sobre café.')


class ModerationFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user('ana', 'ana@example.com', 'Senha#forte1')
        cls.moderator = User.objects.create_user(
            'moderador', 'mod@example.com', 'Senha#forte4', is_staff=True
        )
        cls.moderator.groups.add(Group.objects.get(name='Moderadores'))

    def test_ct11_03_filtro_lista_so_os_reprovados(self):
        post = Post.objects.create(author=self.ana, title='T', body='c')
        post.publish()
        Comment.objects.create(post=post, author=self.ana, body='Bom comentário')
        Comment.objects.create(post=post, author=self.ana, body='Comentário barrado',
                               approved=False)
        self.client.force_login(self.moderator)
        response = self.client.get(reverse('admin:comments_comment_changelist'),
                                   {'approved__exact': '0'})
        self.assertContains(response, 'Comentário barrado')
        self.assertNotContains(response, 'Bom comentário')
