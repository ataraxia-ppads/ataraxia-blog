"""
Rotas do projeto Ataraxia.

Cada aplicação registra as suas próprias rotas em um `urls.py` dentro da
própria pasta, e as inclui aqui com `path('...', include('app.urls'))`.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Ataraxia'
admin.site.site_title = 'Ataraxia'
admin.site.index_title = 'Moderação'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('comments.urls')),
    path('', include('posts.urls')),
]

if settings.DEBUG:
    # Em desenvolvimento o próprio Django serve os arquivos enviados pelos
    # usuários. Em produção isso é responsabilidade do servidor web.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
