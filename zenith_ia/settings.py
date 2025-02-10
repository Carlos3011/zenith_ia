from pathlib import Path
from datetime import timedelta

#Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent

#Seguridad
SECRET_KEY = 'django-insecure-zy39u&j*z39dami-q387w1cn9c4msuz0xz60y1+gzdy1i#33ot'  #Usa variables de entorno en producción
DEBUG = True  #Cambia a False en producción
ALLOWED_HOSTS = ['*']  #Cambiar en producción

DEEPSEEK_API_KEY = "sk-696b06afb4b64af68d12e57cdf9962e5"

#Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #Django REST Framework y JWT
    'rest_framework',
    'rest_framework_simplejwt',
    
    #Tu app principal
    'core',
]

#Modelo de usuario personalizado
AUTH_USER_MODEL = 'core.Usuario'

#Configuración de Django REST Framework (DRF) con JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  #Por defecto, todas las vistas requieren autenticación
    ),
}

#Configuración de JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # 🔹 Token de acceso válido por 1 día
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7), # 🔹 Token de refresh válido por 7 días
    'ROTATE_REFRESH_TOKENS': True,  # 🔹 Genera un nuevo refresh token en cada solicitud de refresh
    'BLACKLIST_AFTER_ROTATION': True,  # 🔹 Invalida los refresh tokens después de rotarlos
    'AUTH_HEADER_TYPES': ('Bearer',),
}

#Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.AuthRedirectMiddleware',  #Asegurar que existe en tu app
]

#Configuración de URLs
ROOT_URLCONF = 'zenith_ia.urls'

#Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core/templates'],  #Ajustado para cargar templates personalizados
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#Aplicación WSGI
WSGI_APPLICATION = 'zenith_ia.wsgi.application'

#Configuración de base de datos (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'zenith_db',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

#Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

#Internacionalización y zona horaria
LANGUAGE_CODE = 'es'  # 🔹 Ajustado a español
TIME_ZONE = 'America/Mexico_City'  # 🔹 Ajustado a la zona horaria de México

USE_I18N = True
USE_TZ = True

#Configuración de archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'core/static']

#Configuración de claves primarias por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
