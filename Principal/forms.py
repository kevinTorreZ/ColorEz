from django import forms
from Principal.models import Usuario
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
    Usuario = forms.CharField(label='',max_length=63, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su usuario'}))
    password = forms.CharField(label='',max_length=63, widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}))
    remember_me = forms.BooleanField(label='Recordar contraseña', required=None)