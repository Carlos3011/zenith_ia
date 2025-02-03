from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm

#Vistas públicas
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

#Vista de dashboard del usuario (Solo autenticados)
@login_required
def dashboard_usuario(request):
    return render(request, 'core/users/dashboard.html', {'usuario': request.user})

#Vista de dashboard del psicólogo (Solo autenticados)
@login_required
def dashboard_psicologo(request):
    return render(request, 'core/psychologists/dashboard.html', {'usuario': request.user})

#Vista de login
def login_view(request):
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

#Vista de registro
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard_usuario' if request.user.tipo == 'usuario' else 'dashboard_psicologo')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido!')
            return redirect('dashboard_usuario')
        else:
            messages.error(request, 'Corrige los errores en el formulario')
    else:
        form = RegistroForm()
    
    return render(request, 'core/auth/register.html', {'form': form})

#Cierre de sesión
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('home')
