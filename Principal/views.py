from django.shortcuts import render,redirect
from Principal.forms import RegisterForm,LoginForm
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'Register.html'
    success_url = '/Home/'
    succes_message = "%(name)s Se ha creado exitosamente!"
    def form_valid(self, form):
        request = self.request
        login(request, form.save())
        return redirect('/Home/')
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/Home/'
    succes_message = "%(name)s Se ha creado exitosamente!"

    def form_valid(self, form):
        request = self.request
        Usuario = form.cleaned_data.get("Usuario")
        password = form.cleaned_data.get("password")
        remember_me = form.cleaned_data['remember_me']
        user = authenticate(request, username=Usuario, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                            request.session.set_expiry(0)
            return redirect('/Home/')
        return super(LoginView, self).form_invalid(form)
@login_required()
def Inicio(request):
    return render(request, 'Inicio.html')
def Index(request):
    return render(request, 'Index.html')