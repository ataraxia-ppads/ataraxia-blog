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
