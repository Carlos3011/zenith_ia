from django.urls import path
from .api_views import register_view, login_view  
from django.contrib.auth import views as auth_views
from .views import home, about, services, blog, contact, login_view as web_login, register
from . import views

urlpatterns = [
    # Páginas sin estar registrados
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
    
    # Vistas de autenticación web
    path('login/', web_login, name='login'),
    path('register/', register, name='register'),
    # Cierre de sesion
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Vistas usuarios
    path('usuario/dashboard/', views.dashboard_usuario, name='dashboard_usuario'),  # Dashboard de usuario

    # Vistas psicolgos
    path('psicologo/dashboard/', views.dashboard_psicologo, name='dashboard_psicologo'),  # Dashboard de psicólogo
    

    # Rutas API para autenticación con JWT
    path('api/register/', register_view, name='api_register'),
    path('api/login/', login_view, name='api_login'),
]
