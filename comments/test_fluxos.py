"""Iteração 2: fluxo principal de UC10, que era só manual."""

from .models import Comment
from .tests import CommentTestCase


class MainFlowTests(CommentTestCase):
    def test_ct10_01_comentario_nasce_aprovado_e_aparece_com_autor_e_data(self):
        self.client.force_login(self.bruno)
        response = self.client.post(self.url, {'body': 'Gostei do texto.'})
        comment = Comment.objects.get()
        destino = f'{self.post.get_absolute_url()}#comentario-{comment.pk}'
        self.assertEqual(response['Location'], destino)
        response = self.client.get(self.post.get_absolute_url())
        self.assertTrue(comment.approved)
        self.assertContains(response, 'Gostei do texto.')
        self.assertContains(response, 'bruno')
        self.assertContains(response, 'datetime=')
