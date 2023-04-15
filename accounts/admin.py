from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts import models, forms


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ('name', 'sex', 'birth_date', 'phone_number', 'is_admin')
    list_display_links = list_display
    list_filter = ('sex', 'birth_date', 'is_admin')
    filter_horizontal = ()
    add_form = forms.UserCreationForm
    form = forms.UserChangeForm
    ordering = ('name',)
    search_fields = ('name', 'phone_number')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password', 'is_admin')}),
        ('Personal info', {'fields': ('name', 'sex', 'birth_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'sex', 'birth_date', 'phone_number', 'password1', 'password2', 'is_admin'),
        }),
    )


# Remove Group model from admin interface
admin.site.unregister(Group)
