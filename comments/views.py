from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views import View

from posts.models import Post

from .forms import CommentForm
from .models import Comment


class CommentCreateView(LoginRequiredMixin, View):
    """UC10. Sem sessão, o LoginRequiredMixin manda para a autenticação (RN13)."""

    http_method_names = ['post']

    def post(self, request, slug):
        # A confirmação acontece na gravação, e não só ao exibir o formulário:
        # o texto pode ter sido despublicado enquanto alguém escrevia (E2).
        post = Post.published.filter(slug=slug).first()
        if post is None:
            messages.error(request, 'Este texto não está mais disponível.')
            return redirect('posts:list')

        if not post.allow_comments:
            # A2 de UC10 e RN17.
            messages.error(request, 'Este texto não aceita novos comentários.')
            return redirect(post)

        form = CommentForm(request.POST)
        if not form.is_valid():
            # E1: reexibe a página do texto com o que foi digitado.
            return TemplateResponse(request, 'posts/post_detail.html', {
                'post': post,
                'object': post,
                'comments': Comment.visible.filter(post=post).select_related('author__profile'),
                'comment_form': form,
            }, status=400)

        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, 'Comentário publicado.')
        return redirect(f'{post.get_absolute_url()}#comentario-{comment.pk}')
