from django.urls import path

from . import views

app_name = 'comments'

urlpatterns = [
    path('texto/<slug:slug>/comentar/', views.CommentCreateView.as_view(), name='create'),
]
