from django import forms

from .models import MAX_LENGTH, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Só o corpo vem do formulário. Texto e autor vêm da URL e da sessão,
        # e um campo forjado no POST é ignorado (RN16).
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'maxlength': MAX_LENGTH}),
        }
        labels = {'body': 'Seu comentário'}

    def clean_body(self):
        body = self.cleaned_data['body'].strip()
        if not body:
            raise forms.ValidationError('O comentário está vazio.')
        if len(body) > MAX_LENGTH:
            raise forms.ValidationError(
                f'O comentário tem {len(body)} caracteres; o limite é {MAX_LENGTH}.'
            )
        return body
