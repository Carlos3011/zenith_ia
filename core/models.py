from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Modelo de Usuario (Usuarios y Psicólogos)
class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('usuario', 'Usuario'),
        ('psicologo', 'Psicólogo'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO, default='usuario')

    # Corrección del error: Agregar related_name a grupos y permisos para evitar conflictos
    groups = models.ManyToManyField(Group, related_name="usuario_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="usuario_permissions", blank=True)

    def es_psicologo(self):
        return self.tipo == 'psicologo'


# Modelo de Trastornos Psicológicos
class Trastorno(models.Model):
    nombre = models.CharField(max_length=100)  # Ejemplo: Depresión, Ansiedad, Estrés
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


# Modelo para Test (Generalizado para PHQ-8, GAD-7, etc.)
class Test(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tests")
    trastorno = models.ForeignKey(Trastorno, on_delete=models.CASCADE, related_name="tests")
    nombre_test = models.CharField(max_length=100)  # Ejemplo: PHQ-8, GAD-7
    fecha_realizacion = models.DateTimeField(auto_now_add=True)
    puntuacion = models.IntegerField()  # Puntuación general del test

    def __str__(self):
        return f"{self.nombre_test} de {self.usuario.username} - {self.fecha_realizacion}"


# Modelo para la Evaluación de IA (Diferentes Modelos de IA por Trastorno)
class EvaluacionIA(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="evaluaciones")
    trastorno = models.ForeignKey(Trastorno, on_delete=models.CASCADE, related_name="evaluaciones")
    modelo_ia = models.CharField(max_length=100)  # Ejemplo: Modelo PHQ-8, Modelo Ansiedad
    puntuacion = models.FloatField()  # Puntuación calculada por la IA (ejemplo: 0-100)
    diagnostico = models.CharField(max_length=100)  # Ejemplo: Leve, Moderado, Severo
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trastorno.nombre} - {self.diagnostico} - {self.modelo_ia}"


# Historial Clínico (Un paciente puede ser atendido por múltiples psicólogos)
class HistorialClinico(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="historial")
    psicologos = models.ManyToManyField(Usuario, related_name="pacientes", limit_choices_to={'tipo': 'psicologo'})
    notas = models.TextField()
    evaluaciones_ia = models.ManyToManyField(EvaluacionIA, related_name="historiales", blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Historial Clínico de {self.usuario.username}"


# Modelo para Citas entre Psicólogos y Pacientes
class Cita(models.Model):
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="citas_paciente")
    psicologo = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="citas_psicologo", limit_choices_to={'tipo': 'psicologo'})
    fecha_cita = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completada', 'Completada')], default='pendiente')

    def __str__(self):
        return f"Cita de {self.paciente.username} con {self.psicologo.username} el {self.fecha_cita}"


# Modelo de Recomendaciones (Personalizadas según el Trastorno y Nivel de Depresión)
class Recomendacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="recomendaciones")
    trastorno = models.ForeignKey(Trastorno, on_delete=models.CASCADE, related_name="recomendaciones")
    nivel_depresion = models.CharField(max_length=10, choices=[('leve', 'Leve'), ('moderado', 'Moderado'), ('severo', 'Severo')])
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    enlace = models.URLField()

    def __str__(self):
        return f"Recomendación para {self.trastorno.nombre} - {self.titulo}"

    class Meta:
        unique_together = ('usuario', 'trastorno', 'nivel_depresion')  # Evita duplicados


# Modelo para Conversaciones con el Chatbot (Se Almacena cada Interacción)
class Conversacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="conversaciones")
    mensaje_usuario = models.TextField()
    respuesta_chatbot = models.TextField()
    estado_emocional = models.CharField(max_length=50, choices=[('neutral', 'Neutral'), ('triste', 'Triste'), ('ansioso', 'Ansioso'), ('feliz', 'Feliz')], default='neutral')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversación con {self.usuario.username} - {self.fecha} - Estado emocional: {self.estado_emocional}"


# Modelo para Notificaciones a Psicólogos
class Notificacion(models.Model):
    psicologo = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="notificaciones", limit_choices_to={'tipo': 'psicologo'})
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)  # Indica si la notificación ha sido leída
    tipo = models.CharField(max_length=50, choices=[
        ('nuevo_paciente', 'Nuevo Paciente Asignado'),
        ('cita', 'Nueva Cita'),
        ('actualizacion', 'Actualización de Paciente'),
        ('nuevo_test', 'Nuevo Test Realizado'),
        ('nueva_recomendacion', 'Nueva Recomendación'),
    ], default='nuevo_paciente')  # Tipo de notificación
    prioridad = models.CharField(max_length=10, choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')], default='media')
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)  # Fecha de vencimiento de la notificación

    def __str__(self):
        return f"Notificación para {self.psicologo.username} - {self.mensaje}"

    class Meta:
        ordering = ['-fecha_creacion']
