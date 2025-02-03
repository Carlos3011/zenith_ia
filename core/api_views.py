from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .forms import RegistroForm
from .models import Usuario

#Función para generar tokens JWT para un usuario
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#Registro de usuario con JWT
@api_view(['POST'])
def register_view(request):
    form = RegistroForm(request.POST)  #Asegurar que `request.POST` contiene los datos del formulario
    if form.is_valid():
        user = form.save()
        tokens = get_tokens_for_user(user)  #Generamos tokens para el usuario recién creado
        return Response(tokens, status=status.HTTP_201_CREATED)
    
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

#Login de usuario con JWT
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    #Intentar autenticar con el username
    user = authenticate(username=username, password=password)
    
    #Si no encuentra el usuario con el username, intentar con el email
    if user is None:
        try:
            user = Usuario.objects.get(email=username)
            user = authenticate(username=user.username, password=password)
        except Usuario.DoesNotExist:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    #Si el usuario es válido, devolver tokens
    if user is not None:
        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)
    
    return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
