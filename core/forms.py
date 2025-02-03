from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    #Configuración del formulario de registro
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']  # No incluimos 'tipo' aquí

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Eliminar el campo 'tipo' para que no sea visible ni editable en el formulario
        if 'tipo' in self.fields:
            del self.fields['tipo']
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        #Forzamos que el tipo de usuario sea siempre 'usuario' al registrarse
        usuario.tipo = 'usuario'  # Si quieres que por defecto siempre sea 'usuario'
        
        if commit:
            usuario.save()  # Guardamos el usuario con el tipo ya establecido
        return usuario
