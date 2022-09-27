from django.contrib import admin

from .models import User


class BaseAdminSettings(admin.ModelAdmin):
    """Панель Админа."""
    empty_value_display = '-empty-'
    list_filter = ('role', 'username')


class UsersAdmin(BaseAdminSettings):
    """Оформление панели админа."""
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'bio',
    )
    list_display_links = ('id', 'username')
    search_fields = ('role', 'username')


admin.site.register(User, UsersAdmin)
