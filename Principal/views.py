from django.shortcuts import render,redirect
import requests
import glob
from django.core.exceptions import ObjectDoesNotExist
import os
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from datetime import date
from qrcode import *
from Principal.forms import RegisterForm,LoginForm,NewProyecto,ChangeDataPerfil
from Principal.models import Usuario,Usuarios_proyecto,Proyecto,Token,LogoTipos,Fonts,PaletaColores,Tareas,Suscripcion,Plan
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from colorutils import Color,rgb_to_hex,hex_to_rgb, ArithmeticModel
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'Register.html'
    success_url = '/Inicio/'
    succes_message = "%(name)s Se ha creado exitosamente!"
    def form_valid(self, form):
        request = self.request
        now = datetime.today()
        login(request, form.save(), backend='django.contrib.auth.backends.ModelBackend')
        instUser = Usuario.objects.get(id=request.user.id)
        form.photo = 'media/ImagePerfil/userImageDefault.png'
        plane = Plan.objects.get(Nombre='Basico')
        Suscrp = Suscripcion(Plan=plane,Usuario=instUser,Fecha_inicio=now)
        Suscrp.save()
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
    instUser = Usuario.objects.get(id=request.user.id)
    try:
        PlanUser = Suscripcion.objects.get(Usuario=instUser)
        PlanUser = PlanUser.Plan.idPlan
        if PlanUser == 2:
            PlanUser = True
        else:
            PlanUser = False
        return render(request, 'Inicio.html',{"plan":PlanUser})
    except ObjectDoesNotExist:
        print("a")
@login_required()
def LogoutView(request):
    if request.user.photo != "userImageDefault.png":
        logout(request)
    else:
        logout(request)
    return render(request, "logout.html")
@login_required()
def Planes(request):
    userinst = Usuario.objects.get(id=request.user.id)
    planuser = Suscripcion.objects.get(Usuario=userinst)
    Basico = Plan.objects.get(idPlan=1)
    Premium = Plan.objects.get(idPlan=2)
    Planuser = planuser.Plan.idPlan
    if request.method == "POST":
        if request.POST.get('PlanBasico', False) != False:
            planuser.Plan = Basico
            planuser.save()
            return redirect('/Planes/')
        else:
            planuser.Plan = Premium
            planuser.save()
            return redirect('/Planes/')
    return render(request, "Planes.html",{"PlanUser":Planuser})
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
            linkChangepassword = "https://colorez.es/ChangePassword/?token=" + str(token)
            asunto = "Restablecer contraseña"
            mensaje = "Ingrese en el link para restablecer su contraseña." + " " + linkChangepassword
            email_desde = settings.EMAIL_HOST_USER
            lista_correos = [email]
            msg_html = render_to_string('email.html', {'Link': linkChangepassword,'user':findUser})
            send_mail(asunto,mensaje,email_desde,lista_correos,html_message=msg_html)
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

@login_required()
def GenerarPaleta(request):
    instUser = Usuario.objects.get(id=request.user.id)
    PlanUser = Suscripcion.objects.get(Usuario=instUser)
    PlanUser = PlanUser.Plan.idPlan
    if PlanUser == 2:
        PlanUser = True
    else:
        PlanUser = False
    return render(request, './Funciones/Generarpaleta.html',{"plan":PlanUser})

def MezclarColores(request):
    return render(request, './Funciones/Mezclarcolores.html')

def Obtenerpaleta(request):
    return render(request, './Funciones/Obtenerpaleta.html')

def Editarperfil(request):
    return render(request, 'Editar-perfil.html')

@login_required()
def Proyectos(request):
    Mensaje_error = "Se ha alcanzado el limite de proyectos"
    form = NewProyecto()
    Mostrarqr = False
    UserInst = Usuario.objects.get(id=request.user.id)
    obj = Usuarios_proyecto.objects.filter(Usuario=request.user.id)
    objOwner = Proyecto.objects.filter(Usuario=request.user.id)
    LogotiposProyecto = LogoTipos.objects.all()
    AllTareas = Tareas.objects.all()
    AllFont = Fonts.objects.all()
    Allcolors = PaletaColores.objects.all()
    if request.method == "POST":
        ProjectSelected = request.POST.get('ProjectSelected')
        now = date.today()
        Titulo = request.POST.get('Titulo')
        if Titulo == None:
            if ProjectSelected == None:
                if request.POST.get('Change',None) == None:
                    idprj = request.POST['idProyecto']
                    searchPrjct = Proyecto.objects.get(idProyecto=idprj)
                    Selected = str(searchPrjct)
                    if request.POST.get('idProyecto',None) != None:
                        if request.POST.get('TareaEliminate',False) != False:
                            TareaEliminate = request.POST.get('TareaEliminate',False)
                            eliminateTarea = Tareas.objects.get(idTarea=TareaEliminate)
                            eliminateTarea.delete()
                        if request.POST.get('FontEliminate',False) != False:
                            Fonteliminate = request.POST.get('FontEliminate',False)
                            eliminateFont = Fonts.objects.get(idFont=Fonteliminate)
                            eliminateFont.delete()
                        if request.POST.get('logoEliminate',False) != False:
                            logoEliminate = request.POST.get('logoEliminate',False)
                            eliminarLogo = LogoTipos.objects.get(idLogo=logoEliminate)
                            os.remove(str(eliminarLogo.Logo))
                            eliminarLogo.delete()
                        if request.POST.get('colorEliminate',False) != False:
                            colorEliminate = request.POST.get('colorEliminate',False)
                            eliminarColor = PaletaColores.objects.get(idPaleta=colorEliminate)
                            eliminarColor.delete()   
                        return render(request, 'Proyectos.html',{'Proyectos':obj,'form':form,'ProyectosOwner':objOwner,"MostrarQR":Mostrarqr,'Tareas':AllTareas,'Logos':LogotiposProyecto,'Fonts':AllFont,'Paleta':Allcolors,'selected':Selected})
                    else:
                        idprj = request.POST['idProyecto']
                        searchPrjct = Proyecto.objects.get(idProyecto=idprj)
                        clearListuser = Usuarios_proyecto.objects.get(Usuario=UserInst, Proyecto=searchPrjct)
                        os.remove(str(searchPrjct.photo))
                        Loges = LogoTipos.objects.filter(Proyecto=searchPrjct)
                        for i in Loges:
                            os.remove(str(i.Logo))
                        clearListuser.delete()
                        searchPrjct.delete()
                else:
                    idprj = request.POST['idProyecto']
                    searchPrjct = Proyecto.objects.get(idProyecto=idprj)
                    color = request.POST.get('Coloradd',False)
                    fonts = request.POST.get('Fontadd',False)
                    Logo = request.FILES.get('Logoadd',False)
                    Tareadd = request.POST.get('Tareadd',False)
                    if color != "":
                        colors = PaletaColores(Color=color,Proyecto=searchPrjct)
                        colors.save()
                    if fonts != "":
                        fonts = Fonts(Fonts=fonts,Proyecto=searchPrjct)
                        fonts.save()
                    if Logo != False:
                        Logo = LogoTipos(Proyecto=searchPrjct,Logo=Logo)
                        Logo.save()
                    if Tareadd != "":
                        tarea = Tareas(Tarea=Tareadd,Proyecto=searchPrjct)
                        tarea.save()
                    Selected = str(searchPrjct)
                    return render(request, 'Proyectos.html',{'Proyectos':obj,'form':form,'ProyectosOwner':objOwner,"MostrarQR":Mostrarqr,'Tareas':AllTareas,'Logos':LogotiposProyecto,'Fonts':AllFont,'Paleta':Allcolors,'selected':Selected})
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
            UserProjects = Proyecto.objects.filter(Usuario=UserInst)
            Suscrip = Suscripcion.objects.get(Usuario=UserInst)
            if Suscrip.Plan.idPlan == 1:
                if len(UserProjects) < 1:
                    Descripcion = request.POST.get('Descripcion')
                    photo = request.FILES.get('photo')
                    if photo == None:
                        photo = 'media/ImageProyectos/default_image_project.png'
                    SaveProject = Proyecto(Titulo=Titulo,Descripcion=Descripcion,Fecha_creacion=now,Usuario=UserInst,photo=photo)
                    SaveProject.save()
                    AddUserPrjt = Usuarios_proyecto(Usuario=UserInst,Proyecto=SaveProject)
                    AddUserPrjt.save()
                    return redirect('/Proyectos/')
                else:
                    return render(request, 'Proyectos.html',{'Proyectos':obj,'form':form,'ProyectosOwner':objOwner,"MostrarQR":Mostrarqr,'Tareas':AllTareas,'Logos':LogotiposProyecto,'Fonts':AllFont,'ProyectoMax':Mensaje_error})
            else:
                if len(UserProjects) <= 5:
                    Descripcion = request.POST.get('Descripcion')
                    photo = request.FILES.get('photo')
                    if photo == None:
                        photo = 'media/ImageProyectos/default_image_project.png'
                    SaveProject = Proyecto(Titulo=Titulo,Descripcion=Descripcion,Fecha_creacion=now,Usuario=UserInst,photo=photo)
                    SaveProject.save()
                    AddUserPrjt = Usuarios_proyecto(Usuario=UserInst,Proyecto=SaveProject)
                    AddUserPrjt.save()
                    return redirect('/Proyectos/')
                else:
                    return render(request, 'Proyectos.html',{'Proyectos':obj,'form':form,'ProyectosOwner':objOwner,"MostrarQR":Mostrarqr,'Tareas':AllTareas,'Logos':LogotiposProyecto,'Fonts':AllFont,'ProyectoMax':Mensaje_error})
    return render(request, 'Proyectos.html',{'Proyectos':obj,'form':form,'ProyectosOwner':objOwner,"MostrarQR":Mostrarqr,'Tareas':AllTareas,'Logos':LogotiposProyecto,'Fonts':AllFont,'Paleta':Allcolors})
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
    return render(request, "Funciones.html")

def Perfil(request):
    instUser = Usuario.objects.get(id=request.user.id)
    formChange = ChangeDataPerfil(instance=instUser)
    ProyectosIn = Usuarios_proyecto.objects.filter(Usuario=instUser)
    ProyectosOwner = Proyecto.objects.filter(Usuario=instUser)
    PlanUser = Suscripcion.objects.get(Usuario=instUser)
    PlanUser = PlanUser.Plan.Nombre
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
                    return redirect('/Perfil/')
                else:
                    formChange.save(commit=True)
                    return redirect('/Perfil/')
            else:
                instUser.username = str(request.POST['username'])
                instUser.email = str(request.POST['email'])
                instUser.save()
                return redirect('/Perfil/')
    return render(request, "Perfil.html",{"form":formChange,"ProyectosOwner":ProyectosOwner,"ProyectosIn":ProyectosIn,"Plan":str(PlanUser)})
 