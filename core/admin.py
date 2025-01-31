from django.contrib import admin
from .models import Usuario, Trastorno, Test, EvaluacionIA, HistorialClinico, Cita, Recomendacion, Conversacion, Notificacion

#Personalización del panel de administración para el modelo Usuario
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo', 'is_active', 'is_staff')
    list_filter = ('tipo', 'is_active', 'is_staff')
    search_fields = ('username', 'email')

#Personalización del panel de administración para Trastornos Psicológicos
class TrastornoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

#Personalización del panel de administración para Test
class TestAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'trastorno', 'nombre_test', 'puntuacion', 'fecha_realizacion')
    list_filter = ('nombre_test', 'trastorno')
    search_fields = ('usuario__username', 'nombre_test')

#Personalización del panel de administración para Evaluaciones de IA
class EvaluacionIAAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'trastorno', 'modelo_ia', 'puntuacion', 'diagnostico', 'fecha_evaluacion')
    list_filter = ('modelo_ia', 'diagnostico')
    search_fields = ('usuario__username', 'modelo_ia')

#Personalización del panel de administración para Historial Clínico
class HistorialClinicoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_actualizacion')
    filter_horizontal = ('psicologos', 'evaluaciones_ia')
    search_fields = ('usuario__username',)

#Personalización del panel de administración para Citas
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'psicologo', 'fecha_cita', 'estado')
    list_filter = ('estado', 'fecha_cita')
    search_fields = ('paciente__username', 'psicologo__username')

#Personalización del panel de administración para Recomendaciones
class RecomendacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'trastorno', 'nivel_depresion', 'titulo')
    list_filter = ('nivel_depresion', 'trastorno')
    search_fields = ('usuario__username', 'titulo')

#Personalización del panel de administración para Conversaciones con el Chatbot
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensaje_usuario', 'respuesta_chatbot', 'estado_emocional', 'fecha')
    list_filter = ('estado_emocional',)
    search_fields = ('usuario__username', 'mensaje_usuario')

#Personalización del panel de administración para Notificaciones
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('psicologo', 'mensaje', 'tipo', 'prioridad', 'fecha_creacion', 'leida')
    list_filter = ('tipo', 'prioridad', 'leida')
    search_fields = ('psicologo__username', 'mensaje')

#Registrar Modelos en Django Admin con Personalización
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Trastorno, TrastornoAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(EvaluacionIA, EvaluacionIAAdmin)
admin.site.register(HistorialClinico, HistorialClinicoAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(Recomendacion, RecomendacionAdmin)
admin.site.register(Conversacion, ConversacionAdmin)
admin.site.register(Notificacion, NotificacionAdmin)
