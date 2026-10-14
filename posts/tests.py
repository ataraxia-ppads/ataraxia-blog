"""Testes de posts. Cada teste leva o identificador do caso de teste do plano
de testes (CTnn.mm), para que uma falha aponte direto para o caso de uso."""

from datetime import datetime
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from comments.models import Comment

from .models import Post

User = get_user_model()


def make_post(author, title, body='Corpo do texto.', published=True, **extra):
    post = Post.objects.create(author=author, title=title, body=body, **extra)
    if published:
        post.publish()
    return post


class PostTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ana = User.objects.create_user('ana', 'ana@example.com', 'Senha#forte1')
        cls.bruno = User.objects.create_user('bruno', 'bruno@example.com', 'Senha#forte2')


class ListTests(PostTestCase):
    def test_ct01_02_rascunho_fora_da_listagem(self):
        make_post(self.ana, 'Publicado')
        make_post(self.ana, 'Rascunho secreto', published=False)
        response = self.client.get(reverse('posts:list'))
        self.assertContains(response, 'Publicado')
        self.assertNotContains(response, 'Rascunho secreto')

    def test_ct01_03_segunda_pagina_sem_repetir(self):
        for i in range(12):
            make_post(self.ana, f'Texto número {i:02d}')
        first = self.client.get(reverse('posts:list'))
        second = self.client.get(reverse('posts:list'), {'page': 2})
        first_ids = {p.pk for p in first.context['posts']}
        second_ids = {p.pk for p in second.context['posts']}
        self.assertEqual(len(first_ids), 10)
        self.assertEqual(len(second_ids), 2)
        self.assertFalse(first_ids & second_ids)

    def test_ct01_04_base_vazia(self):
        response = self.client.get(reverse('posts:list'))
        self.assertContains(response, 'Ainda não há textos publicados')


class DetailTests(PostTestCase):
    def test_ct02_02_so_comentarios_aprovados_em_ordem(self):
        post = make_post(self.ana, 'Com comentários')
        Comment.objects.create(post=post, author=self.bruno, body='Primeiro aprovado')
        Comment.objects.create(post=post, author=self.bruno, body='Reprovado', approved=False)
        Comment.objects.create(post=post, author=self.ana, body='Segundo aprovado')
        response = self.client.get(post.get_absolute_url())
        self.assertNotContains(response, 'Reprovado')
        html = response.content.decode()
        self.assertLess(html.index('Primeiro aprovado'), html.index('Segundo aprovado'))

    def test_ct02_05_slug_inexistente(self):
        response = self.client.get(reverse('posts:detail', args=['nao-existe']))
        self.assertEqual(response.status_code, 404)

    def test_ct02_06_rascunho_alheio_responde_404(self):
        draft = make_post(self.ana, 'Rascunho', published=False)
        self.assertEqual(self.client.get(draft.get_absolute_url()).status_code, 404)
        self.client.force_login(self.bruno)
        self.assertEqual(self.client.get(draft.get_absolute_url()).status_code, 404)

    def test_ct02_07_autora_ve_o_proprio_rascunho(self):
        draft = make_post(self.ana, 'Meu rascunho', published=False)
        self.client.force_login(self.ana)
        response = self.client.get(draft.get_absolute_url())
        self.assertContains(response, 'Meu rascunho')


class SearchTests(PostTestCase):
    def setUp(self):
        self.titled = make_post(self.ana, 'Sobre o ornitorrinco', 'Um animal curioso.')
        self.bodied = make_post(self.ana, 'Outro assunto', 'Fala de quimeras e pouco mais.')
        make_post(self.ana, 'Texto comum')

    def search(self, term, **extra):
        return self.client.get(reverse('posts:list'), {'q': term, **extra})

    def test_ct03_02_termo_so_no_corpo(self):
        self.assertEqual(list(self.search('quimeras').context['posts']), [self.bodied])

    def test_ct03_03_sem_diferenciar_maiusculas(self):
        self.assertEqual(list(self.search('ORNITORRINCO').context['posts']), [self.titled])

    def test_ct03_04_espacos_nas_pontas(self):
        response = self.search('   ornitorrinco  ')
        self.assertEqual(list(response.context['posts']), [self.titled])
        self.assertEqual(response.context['term'], 'ornitorrinco')

    def test_ct03_06_termo_vazio_e_listagem_completa(self):
        self.assertEqual(self.search('').context['paginator'].count, 3)

    def test_ct03_07_paginacao_preserva_o_termo(self):
        for i in range(11):
            make_post(self.bruno, f'Ornitorrinco {i}')
        response = self.search('ornitorrinco', page=2)
        self.assertEqual(len(response.context['posts']), 2)
        self.assertContains(response, '?q=ornitorrinco&amp;page=1')

    def test_ct03_09_pagina_inexistente(self):
        self.assertEqual(self.search('ornitorrinco', page=99).status_code, 404)

    def test_ct03_10_termo_so_no_rascunho(self):
        make_post(self.ana, 'Segredo do pangolim', published=False)
        response = self.search('pangolim')
        self.assertEqual(response.context['paginator'].count, 0)
        self.assertContains(response, 'Nenhum texto encontrado')

    def test_ctn04_termo_com_sql_e_texto_comum(self):
        response = self.search("' OR '1'='1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['paginator'].count, 0)


class MaintainTests(PostTestCase):
    def test_ct08_02_titulo_vazio(self):
        self.client.force_login(self.ana)
        data = {'title': '  ', 'body': 'Corpo guardado'}
        response = self.client.post(reverse('posts:create'), data)
        self.assertTrue(response.context['form'].has_error('title'))
        self.assertContains(response, 'Corpo guardado')
        self.assertFalse(Post.objects.exists())

    def test_ct08_03_corpo_vazio(self):
        self.client.force_login(self.ana)
        data = {'title': 'Título guardado', 'body': ''}
        response = self.client.post(reverse('posts:create'), data)
        self.assertTrue(response.context['form'].has_error('body'))
        self.assertContains(response, 'Título guardado')

    def test_ct08_04_slug_repetido_ganha_sufixo(self):
        self.client.force_login(self.ana)
        for _ in range(2):
            self.client.post(reverse('posts:create'), {'title': 'Primeiro teste', 'body': 'x'})
        slugs = sorted(Post.objects.values_list('slug', flat=True))
        self.assertEqual(slugs, ['primeiro-teste', 'primeiro-teste-2'])
        self.assertTrue(all(p.status == Post.Status.DRAFT for p in Post.objects.all()))

    def test_ct08_06_editar_texto_alheio(self):
        post = make_post(self.ana, 'Da Ana')
        self.client.force_login(self.bruno)
        self.assertEqual(self.client.get(reverse('posts:edit', args=[post.slug])).status_code, 403)

    def test_ct08_07_excluir_texto_alheio(self):
        post = make_post(self.ana, 'Da Ana')
        self.client.force_login(self.bruno)
        response = self.client.post(reverse('posts:delete', args=[post.slug]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())

    def test_ct08_08_excluir_leva_os_comentarios(self):
        post = make_post(self.ana, 'Vai sumir')
        Comment.objects.create(post=post, author=self.bruno, body='um')
        Comment.objects.create(post=post, author=self.bruno, body='dois')
        self.client.force_login(self.ana)
        confirm = self.client.get(reverse('posts:delete', args=[post.slug]))
        self.assertContains(confirm, 'não tem volta')
        self.client.post(reverse('posts:delete', args=[post.slug]))
        self.assertFalse(Post.objects.exists())
        self.assertFalse(Comment.objects.exists())

    def test_ct08_10_slug_imutavel_depois_de_publicado(self):
        post = make_post(self.ana, 'Título original')
        self.client.force_login(self.ana)
        self.client.post(reverse('posts:edit', args=[post.slug]),
                         {'title': 'Título novo', 'body': 'x', 'allow_comments': 'on'})
        post.refresh_from_db()
        self.assertEqual(post.title, 'Título novo')
        self.assertEqual(post.slug, 'titulo-original')

    def test_ct08_11_editor_exige_autenticacao(self):
        response = self.client.get(reverse('posts:create'))
        login = reverse('accounts:login')
        self.assertRedirects(response, f"{login}?next={reverse('posts:create')}")


class PublishTests(PostTestCase):
    def test_ct09_02_despublicar(self):
        post = make_post(self.ana, 'Some daqui')
        self.client.force_login(self.ana)
        self.client.post(reverse('posts:unpublish', args=[post.slug]))
        self.client.logout()
        self.assertNotContains(self.client.get(reverse('posts:list')), 'Some daqui')
        self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 404)

    def test_ct09_03_publicar_texto_alheio(self):
        draft = make_post(self.ana, 'Rascunho da Ana', published=False)
        self.client.force_login(self.bruno)
        response = self.client.post(reverse('posts:publish', args=[draft.slug]))
        self.assertEqual(response.status_code, 403)
        draft.refresh_from_db()
        self.assertEqual(draft.status, Post.Status.DRAFT)

    def test_ct09_04_republicar_mantem_endereco(self):
        post = make_post(self.ana, 'Vai e volta')
        url = post.get_absolute_url()
        post.unpublish()
        post.title = 'Vai e volta, revisto'
        post.save()
        post.publish()
        self.assertEqual(post.get_absolute_url(), url)

    def test_publicar_so_aceita_post(self):
        draft = make_post(self.ana, 'Rascunho', published=False)
        self.client.force_login(self.ana)
        response = self.client.get(reverse('posts:publish', args=[draft.slug]))
        self.assertEqual(response.status_code, 405)

    def test_next_externo_e_ignorado(self):
        draft = make_post(self.ana, 'Rascunho', published=False)
        self.client.force_login(self.ana)
        response = self.client.post(reverse('posts:publish', args=[draft.slug]),
                                    {'next': 'https://exemplo.invalido/'})
        self.assertRedirects(response, reverse('posts:mine'))


class LocalizationTests(PostTestCase):
    def test_ctn10_data_no_fuso_de_brasilia(self):
        post = make_post(self.ana, 'Tarde da noite')
        # 23h30 em Brasília já é dia 15 em UTC.
        post.published_at = datetime(2026, 3, 14, 23, 30, tzinfo=ZoneInfo('America/Sao_Paulo'))
        post.save()
        response = self.client.get(post.get_absolute_url())
        self.assertContains(response, '14 de março de 2026')
