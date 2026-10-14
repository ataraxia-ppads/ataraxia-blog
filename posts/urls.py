from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('texto/<slug:slug>/', views.PostDetailView.as_view(), name='detail'),
    path('meus-textos/', views.MyPostsView.as_view(), name='mine'),
    path('textos/novo/', views.PostCreateView.as_view(), name='create'),
    path('textos/<slug:slug>/editar/', views.PostUpdateView.as_view(), name='edit'),
    path('textos/<slug:slug>/excluir/', views.PostDeleteView.as_view(), name='delete'),
    path('textos/<slug:slug>/publicar/',
         views.PostStatusView.as_view(publish=True), name='publish'),
    path('textos/<slug:slug>/despublicar/',
         views.PostStatusView.as_view(publish=False), name='unpublish'),
]
