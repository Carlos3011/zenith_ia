from django.db import models
from django.contrib.auth.models import AbstractUser

# 📌 Modelo de Usuario (con Psicólogos y Usuarios)
class Usuario(AbstractUser):  
    TIPO_USUARIO = [
        ('usuario', 'Usuario'),
        ('psicologo', 'Psicólogo'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO, default='usuario')

    def es_psicologo(self):
        return self.tipo == 'psicologo'

# 📌 Modelo para el Test PHQ-8
class TestPHQ8(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tests")
    fecha_realizacion = models.DateTimeField(auto_now_add=True)
    p1 = models.IntegerField()
    p2 = models.IntegerField()
    p3 = models.IntegerField()
    p4 = models.IntegerField()
    p5 = models.IntegerField()
    p6 = models.IntegerField()
    p7 = models.IntegerField()
    p8 = models.IntegerField()
    puntaje_total = models.IntegerField()

    def evaluar_riesgo(self):
        if self.puntaje_total >= 20:
            return "Severo"
        elif self.puntaje_total >= 10:
            return "Moderado"
        else:
            return "Leve"

# 📌 Modelo de Historial Clínico
class HistorialClinico(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="historial")
    psicologos = models.ManyToManyField(Usuario, related_name="pacientes", limit_choices_to={'tipo': 'psicologo'})
    notas = models.TextField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)

# 📌 Modelo de Citas entre Psicólogos y Pacientes
class Cita(models.Model):
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="citas_paciente")
    psicologo = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="citas_psicologo", limit_choices_to={'tipo': 'psicologo'})
    fecha_cita = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completada', 'Completada')], default='pendiente')
