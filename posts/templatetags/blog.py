import markdown as md
import nh3
from django import template
from django.utils.safestring import mark_safe
from django.utils.text import Truncator

register = template.Library()

ALLOWED_TAGS = {
    'p', 'br', 'hr', 'strong', 'em', 'code', 'pre', 'blockquote',
    'ul', 'ol', 'li', 'h2', 'h3', 'h4', 'a',
}


@register.filter
def markdown(text):
    """Corpo do texto em markdown. O HTML gerado passa por uma lista fechada de
    marcações, e qualquer outra coisa, inclusive <script>, é descartada."""
    html = md.markdown(text, extensions=['sane_lists'], output_format='html')
    return mark_safe(nh3.clean(html, tags=ALLOWED_TAGS, attributes={'a': {'href', 'title'}}))


@register.filter
def excerpt(text, words=40):
    """Resumo da listagem: o texto já renderizado, sem marcação, cortado."""
    plain = nh3.clean(md.markdown(text), tags=set())
    return Truncator(plain).words(words, truncate=' …')


WORDS_PER_MINUTE = 200


@register.filter
def reading_time(text):
    """Minutos de leitura, a 200 palavras por minuto e nunca menos que um."""
    return max(1, round(len(text.split()) / WORDS_PER_MINUTE))


@register.filter
def initials(profile):
    """Iniciais do avatar: as duas primeiras palavras do nome, ou as duas
    primeiras letras quando o nome tem uma palavra só."""
    words = str(profile).split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return str(profile)[:2].upper()
