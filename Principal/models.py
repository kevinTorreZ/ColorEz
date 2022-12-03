from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class UserManager(BaseUserManager):
    def create_user(self, email,username=None, password=None,photo=None,is_admin=False, activo=True,):
        if not correo:
            raise ValueError('deben tener correos')
        if not username:
            raise ValueError('Deben tener nombres de usuario')
        user = self.model(
            email=self.normalize_email(email),  
            username=username,
            nombre=nombre,
            photo=photo,
            
        )
        user.set_password(password)
        user.is_admin = is_admin
        user.activo = activo
        user.save()
        return user

    def create_superuser(self, correo,username, password):
        user = self.create_user(
            correo,username,
            password=password,
        )
        user.is_admin = True
        user.save()
        return user
class Usuario(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='',
        max_length=60,
        unique=True,
    )
    username = models.CharField(
        verbose_name='',
        max_length=24,
        unique=True,
    )
    photo = models.ImageField(
        verbose_name='',
        max_length=24,
        unique=False,
        default=None,
    )
    activo = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False) 


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

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
    def is_admin(self):
        "El usuario es un administrador?"
        return self.is_admin
    objects = UserManager()

class Metodo_pago(models.Model):
    idMetodo_pago = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=45)
    def __str__(self):
       return self.Nombre
class Comprobante(models.Model):
    idComprobante = models.AutoField(primary_key=True)
    Fecha_pago = models.DateField()
    Costo = models.IntegerField()
    Metodo_pago = models.ForeignKey(Metodo_pago, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
       return self.idComprobante

class Proyecto(models.Model):
    idProyecto = models.AutoField(primary_key=True)
    Titulo = models.CharField(max_length=25)
    Descripcion = models.TextField()
    Fecha_creacion = models.DateField()
    photo = models.ImageField()
    Metodo_pago = models.ForeignKey(Metodo_pago, on_delete=models.CASCADE)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
       return self.idProyecto
class Usuarios_proyecto(models.Model):
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    def __str__(self):
       return self.Proyecto
class File(models.Model):
    idFile = models.AutoField(primary_key=True)
    url = models.FileField()
    Proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    def __str__(self):
       return self.idFile

class Plan(models.Model):
    idPlan = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=45)
    def __str__(self):
       return self.Nombre

class Suscripcion(models.Model):
    idSuscripcion = models.AutoField(primary_key=True)
    Fecha_inicio = models.DateTimeField()
    Fecha_termino = models.DateTimeField()
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Plan = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    def __str__(self):
       return self.idSuscripcion

