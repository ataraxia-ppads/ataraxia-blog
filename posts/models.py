from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class PublishedManager(models.Manager):
    """Devolve só textos publicados.

    A listagem, a busca e a página do texto consultam por aqui, e é isso que
    mantém o rascunho fora delas sem que cada view precise lembrar (RN01, RN04).
    """

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

    def search(self, term):
        # icontains vira consulta parametrizada no ORM: o termo nunca é
        # concatenado ao SQL (RN03).
        return self.get_queryset().filter(
            Q(title__icontains=term) | Q(body__icontains=term)
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Rascunho'
        PUBLISHED = 'PUBLISHED', 'Publicado'

    title = models.CharField('título', max_length=200)
    slug = models.SlugField('endereço', max_length=220, unique=True)
    body = models.TextField('corpo')
    status = models.CharField(
        'situação', max_length=10, choices=Status, default=Status.DRAFT
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='autor',
    )
    allow_comments = models.BooleanField('aceitar comentários', default=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)
    published_at = models.DateTimeField('publicado em', null=True, blank=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'texto'
        verbose_name_plural = 'textos'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def is_visible(self):
        """RN01: rascunho só existe para o próprio autor."""
        return self.status == Post.Status.PUBLISHED

    def is_visible_to(self, user):
        return self.is_visible() or user == self.author

    @property
    def was_ever_published(self):
        return self.published_at is not None

    def publish(self):
        # A data registra a primeira publicação. Despublicar e publicar de novo
        # não muda a data nem o endereço (RN10).
        self.status = Post.Status.PUBLISHED
        if self.published_at is None:
            self.published_at = timezone.now()
        self.save(update_fields=['status', 'published_at', 'updated_at'])

    def unpublish(self):
        self.status = Post.Status.DRAFT
        self.save(update_fields=['status', 'updated_at'])

    def save(self, *args, **kwargs):
        # O slug acompanha o título enquanto o texto nunca foi publicado, e
        # congela depois disso para não quebrar endereço divulgado (RN10).
        if not self.slug or not self.was_ever_published:
            self.slug = self._unique_slug()
        super().save(*args, **kwargs)

    def _unique_slug(self):
        # A3 de UC08: sufixo numérico até achar um valor livre.
        base = slugify(self.title)[:200] or 'texto'
        others = Post.objects.exclude(pk=self.pk)
        slug, n = base, 2
        while others.filter(slug=slug).exists():
            slug = f'{base}-{n}'
            n += 1
        return slug
