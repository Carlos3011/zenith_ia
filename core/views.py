from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from .models import Cita, Recomendacion, Test, EvaluacionIA
from .services.deepseek_service import MentalHealthChatbot

#Vistas públicas
def home(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def chatbotPublic(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip().lower()
        session = request.session
        
        # Iniciar evaluación PHQ-8
        if user_message == 'iniciar evaluación':
            session['phq8_active'] = True
            session['current_question'] = 0
            session['phq8_answers'] = []
            session.save()
            first_question = MentalHealthChatbot.get_phq8_question(session)
            return JsonResponse({'type': 'question', 'text': first_question})
        
        # Manejar evaluación en progreso
        if session.get('phq8_active'):
            response = MentalHealthChatbot.process_answer(session, user_message)
            session.save()
            
            if response['type'] == 'question':
                return JsonResponse(response)
            
            # Finalizar evaluación
            del session['phq8_active']
            return JsonResponse({
                'type': 'result',
                'text': f"Puntuación: {response['score']}/24 - {response['diagnosis']}",
                'recommendation': response['recommendation'],
                'style': response['style']
            })
        
        # Chat normal
        bot_response = MentalHealthChatbot.get_chat_response(user_message)
        return JsonResponse({'type': 'message', 'text': bot_response})
    
    return render(request, 'core/chatbot-public.html')

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

@login_required
def recursos(request):
    return render(request, 'core/users/resources.html')

# Vista del chatbot (solo autenticados)
@login_required
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip().lower()
        session = request.session
        
        # Iniciar evaluación PHQ-8
        if user_message == 'iniciar evaluación':
            session['phq8_active'] = True
            session['current_question'] = 0
            session['phq8_answers'] = []
            session.save()
            first_question = MentalHealthChatbot.get_phq8_question(session)
            return JsonResponse({'type': 'question', 'text': first_question})
        
        # Manejar evaluación en progreso
        if session.get('phq8_active'):
            response = MentalHealthChatbot.process_answer(session, user_message)
            session.save()
            
            if response['type'] == 'question':
                return JsonResponse(response)
            
            # Finalizar evaluación
            del session['phq8_active']
            return JsonResponse({
                'type': 'result',
                'text': f"Puntuación: {response['score']}/24 - {response['diagnosis']}",
                'recommendation': response['recommendation'],
                'style': response['style']
            })
        
        # Chat normal
        bot_response = MentalHealthChatbot.get_chat_response(user_message)
        return JsonResponse({'type': 'message', 'text': bot_response})
    
    return render(request, 'core/users/chatbot.html', context)
# Vista de mis citas (solo autenticados)
@login_required
def mis_citas(request):
    citas = Cita.objects.filter(paciente=request.user)
    return render(request, 'core/users/appointment.html', {'citas': citas})

# Vista de evaluaciones (solo autenticados)
@login_required
def evaluaciones(request):
    evaluaciones = EvaluacionIA.objects.filter(usuario=request.user)
    return render(request, 'core/users/evaluations.html', {'evaluaciones': evaluaciones})

# Vista de recomendaciones (solo autenticados)
@login_required
def recomendaciones(request):
    recomendaciones = Recomendacion.objects.filter(usuario=request.user)
    return render(request, 'core/users/recomendations.html', {'recomendaciones': recomendaciones})

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
