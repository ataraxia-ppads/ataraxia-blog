"""
Rotas do projeto Ataraxia.

Cada aplicação registra as suas próprias rotas em um `urls.py` dentro da
própria pasta, e as inclui aqui com `path('...', include('app.urls'))`.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    # Em desenvolvimento o próprio Django serve os arquivos enviados pelos
    # usuários. Em produção isso é responsabilidade do servidor web.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
