from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('name', 'surname', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_volunteer'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'birthday',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'name', 'surname', 'birthday',),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_admin', 'is_volunteer')
    list_display = (
        'role_str',
        'phone',
        'name',
        'surname',
        'birthday',
        'email',
        'is_staff',
        'is_superuser',
        'is_active',
        'is_volunteer',
    )
    ordering = ('phone',)
    search_fields = ('phone', 'name', 'surname', 'email', 'birthday',)


admin.site.register(models.User, CustomUserAdmin)
