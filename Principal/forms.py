from django import forms
from Principal.models import Usuario
from django.shortcuts import render,redirect
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import string
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su Contraseña'}), label='')
    password_2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))
    class Meta:
        model = Usuario
        fields = ['username','email']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese su correo'}),
            'username': forms.TextInput(
                attrs={'placeholder': 'Ingrese su usuario'}),
            'contraseña': forms.PasswordInput(
                attrs={'placeholder': 'Ingrese su contraseña'}),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Usuario.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("El correo ya esta en uso")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        Usuario = cleaned_data.get("username")
        if len(Usuario) > 20:
            self.add_error("Usuario", "El nombre de usuario es demasiado largo!")            
        if len(password) == 0:
            self.add_error("Usuario", "Debe ingresar un nombre de usuario!")
        if len(password) < 8:
            self.add_error("password", "La contraseña debe ser mayor a 8 digitos")
        if not any(c in string.ascii_uppercase for c in str(password)):
            self.add_error("password", "La contraseña debe contener mayusculas!")
        if password is not None and password != password_2:
            self.add_error("password_2", "Las contraseñas no coinciden")
        return cleaned_data
    def save(self, commit=True):
        Usuario = super().save(commit=False)
        Usuario.set_password(self.cleaned_data["password"])
        if commit:
            Usuario.save()
        return Usuario   
class LoginForm(forms.Form):
    username = forms.CharField(label='',max_length=63, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su usuario'}))
    password = forms.CharField(label='',max_length=63, widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}))
    remember_me = forms.BooleanField(label='Recordar contraseña', required=None)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if Usuario.objects.filter(username=username).exists():
            username = Usuario.objects.get(username=username)
            if not username.check_password(password):
                self.add_error('password', 'La contraseña es incorrecta')
            if username.activo == False:
                self.add_error('username', 'El usuario esta deshabilitado')
        else:
            self.add_error('username', 'El usuario no existe')

    def get_user(self):
        cleaned_data = super(AuthenticationForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        return authenticate(username=username, password=password)

class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username','email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        Usuario = super().save(commit=False)
        Usuario.set_password(self.cleaned_data["password"])
        if commit:
            Usuario.save()
        return Usuario                                                                                                                                                                              
class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ['username','email', 'password', 'activo', 'admin', 'photo']

    def clean_password(self):
        return self.initial["password"]
