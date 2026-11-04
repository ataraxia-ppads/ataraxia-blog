from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'allow_comments']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 18}),
            # O campo fica na coluna lateral, fora do <form>; o atributo o liga
            # ao formulário do texto.
            'allow_comments': forms.CheckboxInput(attrs={'form': 'form-texto'}),
        }
        help_texts = {
            'body': 'Escrito em markdown: **negrito**, *itálico*, listas e links.',
            'allow_comments': 'Desmarque para encerrar a discussão. '
                              'Os comentários já feitos continuam visíveis.',
        }

    def clean_body(self):
        body = self.cleaned_data['body']
        if not body.strip():
            raise forms.ValidationError('Escreva o corpo do texto.')
        return body
