from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'tipo' in self.fields:
            del self.fields['tipo']
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.tipo = 'usuario'  # Se asegura de que el usuario registrado sea siempre de tipo 'usuario'
        if commit:
            usuario.save()
        return usuario
