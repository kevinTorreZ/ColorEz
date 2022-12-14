"""ColorEz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.static import serve
from django.contrib.auth.views import LogoutView
from Principal import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index, name='Index'),
    path('Register/', views.RegisterView.as_view(), name='Register'),
    path('Inicio/', views.Inicio, name='Inicio'),
    path('Login/', views.LoginView.as_view(), name='Login'),
    path('logout/', views.LogoutView,name='Logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('Proyectos/', views.Proyectos, name='Proyectos'),
    path('Funciones/', views.Funciones),
    path('send_email/', views.enviar_correo, name='send_email'),
    path('ChangePassword/', views.validate_token, name='ChangePassword'),
    path('Generar-paleta/', views.GenerarPaleta),
    path('Mezclar-colores', views.MezclarColores),
    path('Obtener-paleta', views.Obtenerpaleta),
    path('Perfil/', views.Perfil),
    path('Planes/', views.Planes),
    path('Editar-perfil', views.Editarperfil),
    path('invitacion_proyecto/', views.Invitacion_proyecto, name='invitacion_proyecto'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'Principal.views.handler404'
handler500 = 'Principal.views.handler500'