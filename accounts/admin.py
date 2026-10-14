from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(DjangoUserAdmin):
    """UC13 com RN18: o moderador gerencia contas de autores, mas não vê nem
    concede o papel de superusuário, e não altera a conta de quem o tem."""

    inlines = [ProfileInline]
    moderator_fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Situação', {'fields': ('is_active', 'is_staff', 'groups')}),
        ('Datas', {'fields': ('last_login', 'date_joined')}),
    )

    def get_fieldsets(self, request, obj=None):
        if obj is None or request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        return self.moderator_fieldsets

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return ('last_login', 'date_joined')

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
