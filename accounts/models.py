from django.conf import settings
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """O que o projeto acrescenta ao `User` do Django: a face pública da conta."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='usuário',
    )
    display_name = models.CharField('nome de exibição', max_length=80, blank=True)
    bio = models.TextField('biografia', max_length=600, blank=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    def __str__(self):
        return self.display_name or self.user.get_username()

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.user.get_username()})
