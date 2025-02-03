from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from .forms import RegistroForm

# Vistas públicas
def home(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def services(request):
    return render(request, 'core/services.html')

def blog(request):
    return render(request, 'core/blog.html')

def contact(request):
    return render(request, 'core/contact.html')

def dashboard_usuario(request):
    # Lógica para mostrar el dashboard del usuario
    return render(request, 'core/users/dashboard.html')

def dashboard_psicologo(request):
    # Lógica para mostrar el dashboard del psicólogo
    return render(request, 'core/psychologists/dashboard.html')  # Asegúrate que la ruta sea correcta


# Vista de login
def login_view(request):
    # Si el usuario ya está autenticado, redirige a su dashboard
    if request.user.is_authenticated:
        return redirect('dashboard_usuario' if request.user.tipo == 'usuario' else 'dashboard_psicologo')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('dashboard_usuario' if user.tipo == 'usuario' else 'dashboard_psicologo')
        else:
            messages.error(request, 'Credenciales inválidas. Intenta nuevamente.')
    
    return render(request, 'core/auth/login.html')

# Vista de registro
def register(request):
    # Si el usuario ya está autenticado, redirige a su dashboard
    if request.user.is_authenticated:
        return redirect('dashboard_usuario' if request.user.tipo == 'usuario' else 'dashboard_psicologo')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Inicia sesión automáticamente después del registro
            messages.success(request, 'Registro exitoso. Bienvenido!')
            return redirect('dashboard_usuario')  # Redirige al dashboard del usuario
        else:
            messages.error(request, 'Corrige los errores en el formulario')
    else:
        form = RegistroForm()
    
    return render(request, 'core/auth/register.html', {'form': form})


