from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class UserManager(BaseUserManager):
    def create_user(self, correo,usuario=None, password=None,fecha_nacimiento=None,nombre=None,rut=None, admin=False, activo=True):
        if not correo:
            raise ValueError('deben tener correos')
        if not Usuario:
            raise ValueError('Deben tener nombres de usuario')
        user = self.model(
            correo=self.normalize_email(correo),  
            usuario=usuario,
            nombre=nombre,
            rut=rut,
            fecha_nacimiento=fecha_nacimiento,
            
        )
        user.set_password(password)
        user.admin = admin
        user.activo = activo
        user.save()
        return user

    def create_superuser(self, correo,Usuario, password,fecha_nacimiento,nombre,rut):
        user = self.create_user(
            correo,Usuario,
            password=password,
            fecha_nacimiento=fecha_nacimiento,
        )
        user.admin = True
        user.save()
        return user
class Usuario(AbstractBaseUser):
    nombre = models.CharField(
        verbose_name='',
        max_length=30,
    )
    apellido = models.CharField(
        verbose_name='',
        max_length=30,
    )
    rut = models.CharField(
        verbose_name='',
        max_length=11,
        unique=True,
    )
    correo = models.EmailField(
        verbose_name='',
        max_length=70,
        unique=True,
    )
    usuario = models.CharField(
        verbose_name='',
        max_length=50,
        unique=True,
    )
    fecha_nacimiento = models.DateField(
        verbose_name='',
        max_length=50,
        unique=False,
        null=True,
    )
    activo = models.BooleanField(default=True)
    admin = models.BooleanField(default=False) 


    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['correo','rut']

    def get_full_name(self):
        return self.correo

    def get_short_name(self):
        return self.correo

    def __str__(self):
        return self.correo

    def has_perm(self, perm, obj=None):
        "El usuario tiene un permiso especifico?"
        return True

    def has_module_perms(self, app_label):
        "El usuario tiene permisos para ver la aplicacion 'app_label'?"
        return True

    @property
    def is_staff(self):
        "El usuario es miembro del staff?"
        return self.staff

    @property
    def is_admin(self):
        "El usuario es un administrador?"
        return self.admin
    objects = UserManager()

