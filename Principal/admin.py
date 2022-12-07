from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

usuario = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'username','password','admin', 'activo','photo']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('email', 'password','username')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin','activo','photo')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','password','admin', 'activo','photo')}
        ),
    )
    search_fields = ['username']
    ordering = ['username']
    filter_horizontal = ()
admin.site.register(usuario, UserAdmin)