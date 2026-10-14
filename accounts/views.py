from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from posts.models import Post

from .forms import ProfileForm, SignUpForm
from .models import Profile


class SignUpView(CreateView):
    """UC05: cria a conta, o perfil vem junto (sinal em `signals.py`), e a
    sessão é iniciada. Toda conta nova é de autor (RN08)."""

    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('posts:list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('posts:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, 'Conta criada. Boas-vindas ao Ataraxia!')
        return response


class ProfileDetailView(DetailView):
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        user = get_object_or_404(
            get_user_model(), username=self.kwargs['username'], is_active=True
        )
        return Profile.objects.get_or_create(user=user)[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.published.filter(author=self.object.user)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """UC07. O objeto é sempre o perfil da sessão: não há como apontar para o
    perfil de outra pessoa."""

    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'

    def get_object(self, queryset=None):
        return Profile.objects.get_or_create(user=self.request.user)[0]

    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado.')
        return super().form_valid(form)
