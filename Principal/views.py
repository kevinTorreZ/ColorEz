from django.shortcuts import render,redirect
import requests
import glob
import os
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from qrcode import *
from Principal.forms import RegisterForm,LoginForm,NewProyecto,ChangeDataPerfil
from Principal.models import Usuario,Usuarios_proyecto,File,Proyecto,Token
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from colorutils import Color,rgb_to_hex,hex_to_rgb, ArithmeticModel
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'Register.html'
    success_url = '/Inicio/'
    succes_message = "%(name)s Se ha creado exitosamente!"
    def form_valid(self, form):
        request = self.request
        form.photo = 'media/ImagePerfil/userImageDefault.png'
        login(request, form.save(), backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/Inicio/')
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/Inicio/'
    succes_message = "%(name)s Se ha creado exitosamente!"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/Inicio/')
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        request = self.request
        Usuario = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        remember_me = form.cleaned_data.get('remember_me')
        user = authenticate(request, username=Usuario, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                            request.session.set_expiry(0)
            if request.GET.get("next") == None or request.GET.get("next") == "":
                return redirect('/Inicio/')
            return redirect(request.GET.get("next"))
        return super(LoginView, self).form_invalid(form)
@login_required()
def Inicio(request):
    return render(request, 'Inicio.html')
@login_required()
def LogoutView(request):
    if request.user.photo != "userImageDefault.png":
        logout(request)
    else:
        print(request.user.photo)
        logout(request)
    return render(request, "logout.html")
def enviar_correo(request):
    if request.method == "POST":    
        email = request.POST["email"]
        userInst = Usuario.objects.filter(email=email).exists()
        if userInst:
            userInst = Usuario.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            findUser = Usuario.objects.get(email=email)
            token = token_generator.make_token(findUser)
            # objToken = Token.objects.filter(Usuario=request.user).filter(Token=token).exists()
            objToken = Token(Token=token,Usuario=userInst)
            objToken.save()
            asunto = "Restablecer contraseña"
            mensaje = "Ingrese en el link para restablecer su contraseña." + " " + "https://colorez.es/ChangePassword/?token=" + str(token)
            email_desde = settings.EMAIL_HOST_USER
            lista_correos = [email]
            send_mail(asunto,mensaje,email_desde,lista_correos)
            print("Se ha enviado el correo!!")
        else:
            return render(request, 'send_email.html',{"error":'El correo ingresado no se encuentra asociado a una cuenta.'})
    return render(request, 'send_email.html')

def validate_token(request):
    token = request.GET["token"]
    Enviado = False
    objToken = Token.objects.filter(Token=token).exists()
    if request.method == "POST":
        contraseña = request.POST["password"]
        confirmcontraseña = request.POST["confirmpassword"]
        if(contraseña == confirmcontraseña):
            Userid = Token.objects.get(Token=token)
            User = Usuario.objects.get(id=Userid.Usuario.id);
            User.set_password(contraseña) 
            User.save()
            getToken = Token.objects.filter(Token=token);
            getToken.delete()
            Enviado = True
    return render(request, "Changepassword.html",{"is_valid":objToken,"send":Enviado})



def Index(request):
    return render(request, 'Index.html')

def GenerarPaleta(request):
    return render(request, './Funciones/Generarpaleta.html')

@login_required()
def Proyectos(request):
    form = NewProyecto()
    Mostrarqr = False
    UserInst = Usuario.objects.get(id=request.user.id)
    obj = Usuarios_proyecto.objects.filter(Usuario=request.user.id)
    objOwner = Proyecto.objects.filter(Usuario=request.user.id)

    Fileobj = File.objects.all();
    if request.method == "POST":
        ProjectSelected = request.POST.get('ProjectSelected')
        now = date.today()
        Titulo = request.POST.get('Titulo')
        if Titulo == None:
            if ProjectSelected == 0:
                idprj = request.POST['idProyecto']
                searchPrjct = Proyecto.objects.get(idProyecto=idprj)
                clearListuser = Usuarios_proyecto.objects.get(Usuario=UserInst, Proyecto=searchPrjct)
                clearListuser.delete()
                searchPrjct.delete()
            else:
                userInst = Usuario.objects.get(id=request.user.id)
                token_generator = PasswordResetTokenGenerator()
                findUser = Usuario.objects.get(id=request.user.id)
                token = token_generator.make_token(findUser)
                # objToken = Token.objects.filter(Usuario=request.user).filter(Token=token).exists()
                objToken = Token(Token=token,Usuario=userInst)
                objToken.save()
                imgtest = make("https://colorez.es/invitacion_proyecto/?token=" + str(token) + "&id=" + str(ProjectSelected))
                imgtest.save("media/test2.png")
                Mostrarqr = True
        else:
            Descripcion = request.POST.get('Descripcion')
            photo = request.FILES.get('photo')
            if photo == None:
                photo = 'media/default_image_project.png'
            SaveProject = Proyecto(Titulo=Titulo,Descripcion=Descripcion,Fecha_creacion=now,Usuario=UserInst,photo=photo)
            SaveProject.save()
            AddUserPrjt = Usuarios_proyecto(Usuario=UserInst,Proyecto=SaveProject)
            AddUserPrjt.save()
    return render(request, 'Proyectos.html',{'Proyectos':obj,'form':form,'AllFiles':Fileobj,'ProyectosOwner':objOwner,"MostrarQR":Mostrarqr})
@login_required()
def Invitacion_proyecto(request):
    token = request.GET["token"]
    idProject = request.GET["id"]
    Enviado = False
    objToken = Token.objects.filter(Token=token).exists()
    projecto = Proyecto.objects.get(idProyecto=idProject)
    if request.method == "POST":
        User = Usuario.objects.get(id=request.user.id);
        vincular = Usuarios_proyecto(Usuario=User,Proyecto=projecto)
        vincular.save()
        Enviado = True
        objToken = Token.objects.get(Token=token)
        objToken.delete()
    return render(request, "invitacion_proyecto.html",{"is_valid":objToken,"send":Enviado,"Proyecto":projecto})
def Funciones(request):
    return render(request, 'Funciones.html')

def Perfil(request):
    instUser = Usuario.objects.get(id=request.user.id)
    formChange = ChangeDataPerfil(instance=instUser)
    
    if request.method == "POST":
        formChange= ChangeDataPerfil(request.POST,request.FILES,instance= instUser)
        if formChange.is_valid(): 
            if request.FILES.get('photo',"") != "":
                filepath = glob.glob('media/ImagePerfil/'+str(request.FILES['photo'])) 
                if filepath != []:
                    instUser.photo = 'media/ImagePerfil/'+str(request.FILES['photo'])
                    instUser.username = str(request.POST['username'])
                    instUser.email = str(request.POST['email'])
                    instUser.save()
                else:
                    formChange.save(commit=True)
            else:
                instUser.username = str(request.POST['username'])
                instUser.email = str(request.POST['email'])
                instUser.save()
    return render(request, "Perfil.html",{"form":formChange})
 