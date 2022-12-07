from django.contrib import admin
from django.contrib.auth.models import Group
from Principal.models import Usuario

admin.site.unregister(Group)
class UsuarioAdmin(admin.ModelAdmin):
   list_display = ['id', 'username','password','email','photo','activo','admin','staff','last_login']

admin.site.register(Usuario, UsuarioAdmin)