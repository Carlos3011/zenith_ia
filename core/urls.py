from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_views
from .api_views import register_view, login_view  
from .views import (
    home, about, services, blog, contact, 
    login_view as web_login, register, logout_view,
    dashboard_usuario, dashboard_psicologo,
    recursos, chatbot, mis_citas, evaluaciones, recomendaciones
)

urlpatterns = [
    # Páginas públicas
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
    
    # Autenticación web
    path('login/', web_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),  # Ahora usamos nuestra propia vista de logout

    # Vistas del usuario (Solo autenticados)
    path('usuario/dashboard/', dashboard_usuario, name='dashboard_usuario'),
    path('usuario/recursos/', recursos, name='recursos'),
    path('usuario/chatbot/', chatbot, name='chatbot'),
    path('usuario/mis-citas/', mis_citas, name='mis_citas'),
    path('usuario/evaluaciones/', evaluaciones, name='evaluaciones'),
    path('usuario/recomendaciones/', recomendaciones, name='recomendaciones'),

    # Vistas del psicólogo
    path('psicologo/dashboard/', dashboard_psicologo, name='dashboard_psicologo'),
    
    # API para autenticación con JWT
    path('api/register/', register_view, name='api_register'),
    path('api/login/', login_view, name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
