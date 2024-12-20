# pomodoro/models.py
from django.db import models
from django.contrib.auth.models import User

class Sesion(models.Model):
    """Representa un tipo de sesión de Pomodoro (e.g., Estudio, Descanso, etc.)."""
    nombre = models.CharField(max_length=255, help_text="Nombre de la sesión (Estudio, Repaso, Descanso, etc.)")
    duracion_minutos = models.PositiveIntegerField(help_text="Duración de la sesión en minutos para ser completada")
    es_obligatoria = models.BooleanField(default=True, help_text="Indica si esta sesión es obligatoria para completar la tarea")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class TareaTimer(models.Model):
    """Representa una tarea que requiere un número de sesiones para completarse."""
    nombre = models.CharField(max_length=255, help_text="Nombre de la tarea")
    cantidad_para_completar = models.PositiveIntegerField(help_text="Número total de sesiones necesarias para completar la tarea")
    cantidad_completadas = models.PositiveIntegerField(default=0, help_text="Número de sesiones completadas actualmente")
    esta_realizada= models.BooleanField(default=False, help_text="Indica si la tarea está completada")
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def verificar_completitud(self):
        """Verifica si la tarea está completada según las sesiones necesarias."""
        if self.cantidad_completadas >= self.cantidad_para_completar:
            self.esta_realizada = True
        else:
            self.esta_realizada = False
        self.save()

    def __str__(self):
        return f"{self.nombre}"
