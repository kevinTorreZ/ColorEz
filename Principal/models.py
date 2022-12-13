from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class UserManager(BaseUserManager):
    def create_user(self, email,username=None, password=None,photo=None,staff=False,admin=False, activo=True,):
        user = self.model(
            email=self.normalize_email(email),  
            username=username,
            photo=photo,
            
        )
        user.set_password(password)
        user.admin = admin
        user.staff = staff
        user.activo = activo
        user.save()
        return user

    def create_superuser(self, email,username, password):
        user = self.create_user(
            email,username,
            password=password,
        )
        user.staff = True
        user.admin = True
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
        upload_to = 'media/ImagePerfil/',
        default='userImageDefault.png',
        verbose_name='',
        max_length=40,
        unique=False,
    )
    activo = models.BooleanField(default=True)
    admin = models.BooleanField(default=False) 
    staff = models.BooleanField(default=False) 

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "El usuario tiene un permiso especifico?"
        return True

    def has_module_perms(self, app_label):
        "El usuario tiene permisos para ver la aplicacion 'app_label'?"
        return True
    @property
    def is_admin(self):
        "El usuario es un administrador?"
        return self.admin
    @property
    def is_staff(self):
        "El usuario es un administrador?"
        return self.staff
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
    Descripcion = models.TextField(max_length=75)
    Fecha_creacion = models.DateField(verbose_name='',)
    photo = models.ImageField(upload_to = 'media/ImageProyectos',unique=False, height_field = None, width_field = None, max_length = 100, help_text = None)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name='',)
    def __str__(self):
       return self.Titulo
class LogoTipos(models.Model):
    idLogo = models.AutoField(primary_key=True)
    Logo = models.ImageField(upload_to = 'media/Logotipos',unique=False, height_field = None, width_field = None, max_length = 100, help_text = None)
    Proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    def __str__(self):
       return self.Logo
class Tareas(models.Model):
    idTarea = models.AutoField(primary_key=True)
    Tarea = models.CharField(max_length=100)
    Proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    def __str__(self):
       return self.Tarea
class Fonts(models.Model):
    idTarea = models.AutoField(primary_key=True)
    Fonts = models.CharField(max_length=100)
    Proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    def __str__(self):
       return self.Fonts
class PaletaColores(models.Model):
    idTarea = models.AutoField(primary_key=True)
    Color = models.CharField(max_length=35)
    Proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    def __str__(self):
       return self.Color
class Usuarios_proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    def __str__(self):
       return str(self.id)
class Plan(models.Model):
    idPlan = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=45)
    def __str__(self):
       return self.Nombre

class Suscripcion(models.Model):
    idSuscripcion = models.AutoField(primary_key=True)
    Fecha_inicio = models.DateTimeField()
    Fecha_termino = models.DateTimeField(null=True)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    Plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    def __str__(self):
       return self.idSuscripcion

class Token(models.Model):
    idToken = models.AutoField(primary_key=True)
    Token = models.CharField(max_length=50)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
       return self.Token    


