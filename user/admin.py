from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.html import format_html


# Register your models here.

class UserAdmin(UserAdmin):
    search_fields = ('phone', 'username', 'email')
    list_filter = ('is_client', 'is_seller')
    list_display = ('phone', 'email', 'username', 'is_seller', 'is_client', 'show_image', 'date_joined')
    date_hierarchy = ('date_joined')

    @admin.display(empty_value='-', description="show image")
    def show_image(self, obj):
        if (obj.image):
            return format_html(
                '<img src="{}" width=50 height=50/>', obj.image.url,
            )
        return '-'

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('phone', 'email', 'username'), 'password1', 'password2')
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('phone', 'password', 'username', 'email', 'is_client', 'is_seller')
        }),

        ('more options', {
            'classes': ('collapse',),
            'fields': ('first_name', 'last_name', 'image'),
        }),
    )

    save_on_top = True
    list_editable = ('is_client', 'is_seller')


admin.site.register(User, UserAdmin)
