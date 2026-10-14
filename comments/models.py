from django.conf import settings
from django.db import models

MAX_LENGTH = 2000


class ApprovedManager(models.Manager):
    """Comentários visíveis na leitura. O reprovado só aparece no admin (RN02)."""

    def get_queryset(self):
        return super().get_queryset().filter(approved=True)


class Comment(models.Model):
    # Excluir o texto exclui os comentários: não há comentário órfão (RN11).
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='texto',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='autor',
    )
    body = models.TextField('comentário', max_length=MAX_LENGTH)
    # Nasce aprovado; a moderação é o ato de reprovar (RN14).
    approved = models.BooleanField('aprovado', default=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    objects = models.Manager()
    visible = ApprovedManager()

    class Meta:
        verbose_name = 'comentário'
        verbose_name_plural = 'comentários'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author} em {self.post}'
