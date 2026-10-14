from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'published_at', 'updated_at']
    list_filter = ['status', 'published_at']
    search_fields = ['title', 'body', 'author__username']
    readonly_fields = ['slug', 'created_at', 'updated_at', 'published_at']
