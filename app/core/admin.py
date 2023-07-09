"""
Django admin customisation
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for user"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # First fieldset
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)}),  # Last fieldset
    )
    readonly_fields = ('last_login',)  # Fields that cannot be edited
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # CSS class
            'fields': ('email', 'password1', 'password2', 'name', 'is_staff', 'is_superuser')
        }),
    )


admin.site.register(models.User, UserAdmin)
