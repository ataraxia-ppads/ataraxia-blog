from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """UC11: a moderação é feita aqui, sem tela própria."""

    list_display = ['short_body', 'author', 'post', 'created_at', 'approved']
    list_filter = ['approved', 'created_at']
    search_fields = ['body', 'author__username', 'post__title']
    readonly_fields = ['post', 'author', 'body', 'created_at']
    fields = ['post', 'author', 'body', 'created_at', 'approved']
    actions = ['approve', 'disapprove']

    @admin.display(description='comentário')
    def short_body(self, obj):
        return obj.body if len(obj.body) <= 80 else obj.body[:77] + '...'

    @admin.action(permissions=['change'], description='Aprovar os comentários selecionados')
    def approve(self, request, queryset):
        n = queryset.update(approved=True)
        self.message_user(request, f'{n} comentário(s) aprovado(s).')

    @admin.action(permissions=['change'], description='Reprovar os comentários selecionados')
    def disapprove(self, request, queryset):
        n = queryset.update(approved=False)
        self.message_user(request, f'{n} comentário(s) reprovado(s).')

    def has_add_permission(self, request):
        # Comentário nasce pelo site, com autor da sessão; o admin só modera.
        return False
