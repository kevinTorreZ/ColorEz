from django.shortcuts import render,redirect
import requests
from Principal.forms import RegisterForm,LoginForm
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Principal.models import Usuarios_proyecto
from colorutils import Color,rgb_to_hex,hex_to_rgb, ArithmeticModel
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'Register.html'
    success_url = '/Inicio/'
    succes_message = "%(name)s Se ha creado exitosamente!"
    def form_valid(self, form):
        request = self.request
        login(request, form.save(), backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/Inicio/')
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/Inicio/'
    succes_message = "%(name)s Se ha creado exitosamente!"

    def get(self, request, *args, **kwargs):
        login_different = reverse_lazy('login_different')
        if request.user.is_authenticated and login_different != request.path:
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
            return redirect('/Inicio/')
        return super(LoginView, self).form_invalid(form)
@login_required()
def Inicio(request):
    return render(request, 'Inicio.html')
def Index(request):
    return render(request, 'Index.html')
@login_required()
def Proyectos(request):
    obj = Usuarios_proyecto.objects.filter(Usuario='7')
    return render(request, 'Proyectos.html',{'Proyectos':obj})