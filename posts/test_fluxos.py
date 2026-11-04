"""Iteração 2: casos do plano de testes que a Iteração 1 deixava para execução
manual e que dá para provar sem navegador (fluxo principal e alternativos).

Cada teste leva o identificador do caso de teste (CTnn.mm). O que só se confere
olhando a tela, como o visual do botão Cancelar, continua manual."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.urls import reverse
from django.utils import timezone

from comments.models import Comment

from .models import Post
from .tests import PostTestCase, make_post


class ReadAndListTests(PostTestCase):
    def test_ct01_01_publicados_do_mais_recente_para_o_mais_antigo(self):
        base = datetime(2026, 3, 1, 9, 0, tzinfo=ZoneInfo('America/Sao_Paulo'))
        for i in range(9):
            post = make_post(self.ana, f'Texto {i}')
            post.published_at = base + timedelta(days=i)
            post.save()
        make_post(self.ana, 'Rascunho', published=False)
        response = self.client.get(reverse('posts:list'))
        titles = [p.title for p in response.context['posts']]
        self.assertEqual(titles, [f'Texto {i}' for i in range(8, -1, -1)])

    def test_ct02_01_leitura_mostra_titulo_autor_data_e_corpo(self):
        post = make_post(self.ana, 'Para ler', 'Um corpo **claro**.')
        response = self.client.get(post.get_absolute_url())
        self.assertContains(response, 'Para ler')
        self.assertContains(response, 'ana')
        self.assertContains(response, '<strong>claro</strong>')
        self.assertContains(response, 'datetime=')

    def test_ct02_03_visitante_ve_convite_no_lugar_do_formulario(self):
        post = make_post(self.ana, 'Aberto a todos')
        response = self.client.get(post.get_absolute_url())
        self.assertNotContains(response, 'name="body"')
        self.assertContains(response, reverse('accounts:login'))
        self.assertContains(response, reverse('accounts:signup'))

    def test_ct02_04_aviso_de_texto_sem_comentarios(self):
        post = make_post(self.ana, 'Silencioso')
        response = self.client.get(post.get_absolute_url())
        self.assertContains(response, 'Ainda não há comentários')


class SearchFlowTests(PostTestCase):
    def setUp(self):
        self.target = make_post(self.ana, 'Sobre o ornitorrinco')
        make_post(self.ana, 'Texto comum')

    def test_ct03_01_busca_no_titulo_conta_e_mantem_o_termo(self):
        response = self.client.get(reverse('posts:list'), {'q': 'ornitorrinco'})
        self.assertEqual(list(response.context['posts']), [self.target])
        self.assertContains(response, '<strong>1</strong> texto encontrado')
        self.assertContains(response, 'value="ornitorrinco"')

    def test_ct03_05_opcao_de_limpar_leva_a_listagem_completa(self):
        response = self.client.get(reverse('posts:list'), {'q': 'ornitorrinco'})
        self.assertContains(response, f'href="{reverse("posts:list")}"')
        self.assertContains(response, 'Limpar busca')
        completa = self.client.get(reverse('posts:list'))
        self.assertEqual(completa.context['paginator'].count, 2)

    def test_ct03_08_termo_inexistente_oferece_voltar(self):
        response = self.client.get(reverse('posts:list'), {'q': 'inexistente'})
        self.assertContains(response, 'Nenhum texto encontrado')
        self.assertContains(response, 'Ver todos os textos')

    def test_ct03_11_endereco_direto_equivale_a_busca_pela_tela(self):
        pela_tela = self.client.get(reverse('posts:list'), {'q': 'ornitorrinco'})
        direto = self.client.get('/?q=ornitorrinco')
        self.assertEqual(list(direto.context['posts']), list(pela_tela.context['posts']))


class MaintainFlowTests(PostTestCase):
    def test_ct08_01_texto_nasce_rascunho_aberto_a_comentarios(self):
        self.client.force_login(self.ana)
        # O navegador envia a caixa marcada, que é o valor inicial do formulário.
        form = self.client.get(reverse('posts:create')).context['form']
        self.assertTrue(form['allow_comments'].value())
        self.client.post(reverse('posts:create'), {
            'title': 'Primeiro teste', 'body': 'Corpo.', 'allow_comments': 'on',
        })
        post = Post.objects.get()
        self.assertEqual(post.slug, 'primeiro-teste')
        self.assertEqual(post.status, Post.Status.DRAFT)
        self.assertTrue(post.allow_comments)
        self.assertContains(self.client.get(reverse('posts:mine')), 'Primeiro teste')
        self.client.logout()
        self.assertNotContains(self.client.get(reverse('posts:list')), 'Primeiro teste')

    def test_ct08_05_editar_o_corpo_atualiza_a_data_de_modificacao(self):
        post = make_post(self.ana, 'Para editar', 'Corpo antigo.')
        antes = post.updated_at
        self.client.force_login(self.ana)
        self.client.post(reverse('posts:edit', args=[post.slug]), {
            'title': 'Para editar', 'body': 'Corpo novo.', 'allow_comments': 'on',
        })
        post.refresh_from_db()
        self.assertEqual(post.body, 'Corpo novo.')
        self.assertGreater(post.updated_at, antes)

    def test_ct08_09_abrir_a_confirmacao_nao_exclui_e_cancelar_volta_ao_texto(self):
        post = make_post(self.ana, 'Fica')
        self.client.force_login(self.ana)
        response = self.client.get(reverse('posts:delete', args=[post.slug]))
        self.assertContains(response, reverse('posts:edit', args=[post.slug]))
        self.assertContains(response, 'Cancelar')
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())

    def test_ct09_01_publicar_registra_a_data_e_lista_o_texto(self):
        draft = make_post(self.ana, 'Vai ao ar', published=False)
        self.client.force_login(self.ana)
        self.client.post(reverse('posts:publish', args=[draft.slug]))
        draft.refresh_from_db()
        self.assertEqual(draft.status, Post.Status.PUBLISHED)
        self.assertLess(timezone.now() - draft.published_at, timedelta(minutes=1))
        self.client.logout()
        self.assertContains(self.client.get(reverse('posts:list')), 'Vai ao ar')

    def test_ct10_09_encerrar_comentarios_mantem_os_existentes(self):
        post = make_post(self.ana, 'Discussão')
        Comment.objects.create(post=post, author=self.bruno, body='Já comentado')
        self.client.force_login(self.ana)
        # Caixa de comentários desmarcada: o navegador não envia o campo.
        self.client.post(reverse('posts:edit', args=[post.slug]),
                         {'title': 'Discussão', 'body': 'Corpo.'})
        page = self.client.get(post.get_absolute_url())
        self.assertContains(page, 'Já comentado')
        self.assertContains(page, 'não aceita novos comentários')
        self.assertNotContains(page, 'name="body"')
