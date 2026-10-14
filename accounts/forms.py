from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

User = get_user_model()


class SignUpForm(UserCreationForm):
    """UC05. A robustez da senha é a dos validadores do Django (RN07), e o
    `save()` herdado grava a senha como hash PBKDF2 (RN06)."""

    email = forms.EmailField(label='E-mail')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe uma conta com este e-mail.')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio']
        widgets = {'bio': forms.Textarea(attrs={'rows': 5})}
        help_texts = {
            'display_name': 'Como seu nome aparece nos textos. '
                            'Em branco, usa o nome de usuário.',
        }
