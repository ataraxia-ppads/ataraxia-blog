from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from comments.forms import CommentForm
from comments.models import Comment

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    """UC01 e UC03: a listagem é a busca com o termo vazio."""

    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # RN05: o termo vem do endereço, e a paginação o preserva.
        self.term = self.request.GET.get('q', '').strip()
        posts = Post.published.search(self.term) if self.term else Post.published.all()
        return posts.select_related('author__profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['term'] = self.term
        return context


class PostDetailView(DetailView):
    """UC02: rascunho alheio responde 404, nunca 403 (RN01)."""

    template_name = 'posts/post_detail.html'

    def get_object(self, queryset=None):
        post = get_object_or_404(
            Post.objects.select_related('author__profile'), slug=self.kwargs['slug']
        )
        if not post.is_visible_to(self.request.user):
            raise Http404
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (
            Comment.visible.filter(post=self.object).select_related('author__profile')
        )
        context.setdefault('comment_form', CommentForm())
        return context


class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """RN09: a autoria é conferida no servidor. Quem não é o autor recebe 403."""

    def get_object(self, queryset=None):
        if not hasattr(self, '_post'):
            self._post = get_object_or_404(Post, slug=self.kwargs['slug'])
        return self._post

    def test_func(self):
        return self.get_object().author == self.request.user


class MyPostsView(LoginRequiredMixin, ListView):
    template_name = 'posts/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-updated_at')


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:mine')

    def form_valid(self, form):
        # RN12: todo texto nasce rascunho; o modelo já tem DRAFT por padrão.
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Rascunho salvo. Publique quando estiver pronto.')
        return response


class PostUpdateView(AuthorRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Alterações salvas.')
        return response

    def get_success_url(self):
        return reverse('posts:edit', kwargs={'slug': self.object.slug})


class PostDeleteView(AuthorRequiredMixin, DeleteView):
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:mine')

    def form_valid(self, form):
        # Os comentários vão junto, pelo CASCADE do modelo (RN11).
        messages.success(self.request, f'"{self.get_object()}" foi excluído.')
        return super().form_valid(form)


class PostStatusView(AuthorRequiredMixin, View):
    """UC09: publicar e despublicar são atos explícitos, sempre por POST."""

    publish = True
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        if self.publish:
            post.publish()
            messages.success(request, 'Texto publicado.')
        else:
            post.unpublish()
            messages.success(request, 'Texto despublicado. Ele voltou a ser rascunho.')
        # Só volta para endereço do próprio site; qualquer outro vira Meus textos.
        next_url = request.POST.get('next', '')
        if not url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
        ):
            next_url = reverse('posts:mine')
        return redirect(next_url)
