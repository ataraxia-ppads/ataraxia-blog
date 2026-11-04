"""Iteração 2: objetivos não funcionais do plano de testes (capítulo 4)."""

import re
import time

from django.test import TestCase
from django.urls import reverse

from .models import Post
from .tests import PostTestCase, make_post


class PerformanceTests(PostTestCase):
    """CTN02 (ONF02): a listagem com 500 textos responde em até 2 segundos.

    O tempo depende da máquina, então o teste confere as duas coisas que o
    explicam: o número de consultas não cresce com a quantidade de textos, e a
    resposta cabe no limite do plano mesmo no banco de teste."""

    LIMIT_SECONDS = 2.0

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Post.objects.bulk_create([
            Post(author=cls.ana, title=f'Texto {i:03d}', slug=f'texto-{i:03d}',
                 body='Corpo do texto. ' * 40, status=Post.Status.PUBLISHED,
                 published_at=None)
            for i in range(500)
        ])
        Post.objects.update(published_at='2026-03-01T09:00:00-03:00')

    def test_ctn02_listagem_com_500_textos(self):
        url = reverse('posts:list')
        tempos = []
        for _ in range(5):
            inicio = time.perf_counter()
            response = self.client.get(url)
            tempos.append(time.perf_counter() - inicio)
            self.assertEqual(response.status_code, 200)
        self.assertLessEqual(max(tempos), self.LIMIT_SECONDS, tempos)

    def test_ctn02_consultas_nao_crescem_com_a_quantidade_de_textos(self):
        # Uma consulta para a contagem e uma para a página, com autor e perfil
        # trazidos por junção: nada de consulta por texto listado.
        with self.assertNumQueries(2):
            self.client.get(reverse('posts:list'))

    def test_ctn02_busca_com_500_textos(self):
        inicio = time.perf_counter()
        response = self.client.get(reverse('posts:list'), {'q': 'texto 499'})
        self.assertLessEqual(time.perf_counter() - inicio, self.LIMIT_SECONDS)
        self.assertEqual(response.context['paginator'].count, 1)


class AccessibilityTests(PostTestCase):
    """CTN09 (ONF07): todo campo de formulário tem rótulo associado.

    O contraste e a navegação só por teclado continuam manuais."""

    FIELD = re.compile(r'<(input|textarea|select)\b([^>]*)>', re.I)

    def assert_fields_labelled(self, html, where):
        labelled = set(re.findall(r'<label[^>]*\bfor="([^"]+)"', html))
        for tag, attrs in self.FIELD.findall(html):
            kind = re.search(r'type="([^"]+)"', attrs)
            if tag.lower() == 'input' and kind and kind.group(1) in {
                    'hidden', 'submit', 'button'}:
                continue
            ident = re.search(r'\bid="([^"]+)"', attrs)
            self.assertIsNotNone(ident, f'{where}: campo sem id: {attrs}')
            self.assertIn(ident.group(1), labelled,
                          f'{where}: campo {ident.group(1)} sem rótulo')

    def test_ctn09_formularios_de_visitante(self):
        for name in ('accounts:signup', 'accounts:login', 'posts:list'):
            html = self.client.get(reverse(name)).content.decode()
            self.assert_fields_labelled(html, name)

    def test_ctn09_formularios_de_autor(self):
        post = make_post(self.ana, 'Com comentário')
        self.client.force_login(self.ana)
        for url in (reverse('posts:create'), reverse('accounts:profile_edit'),
                    reverse('posts:edit', args=[post.slug]), post.get_absolute_url()):
            html = self.client.get(url).content.decode()
            self.assert_fields_labelled(html, url)

    def test_ctn09_idioma_da_pagina_declarado(self):
        html = self.client.get(reverse('posts:list')).content.decode()
        self.assertIn('<html lang="pt-BR">', html)


class SmokeTests(TestCase):
    """CTN07 (ONF05): a verificação de sistema do Django não aponta problemas."""

    def test_check(self):
        from django.core.management import call_command
        call_command('check')
