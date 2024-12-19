# pomodoro/models.py
from django.db import models
from django.contrib.auth.models import User

class Sesion(models.Model):
    """Representa un tipo de sesión de Pomodoro (e.g., Estudio, Descanso, etc.)."""
    nombre = models.CharField(max_length=255, help_text="Nombre de la sesión (Estudio, Repaso, Descanso, etc.)")
    duracion_minutos = models.PositiveIntegerField(help_text="Duración de la sesión en minutos")
    cuenta_para_completar = models.BooleanField(default=True, help_text="Indica si esta sesión cuenta para completar la tarea")
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    """Representa una tarea con un conjunto de sesiones asociadas."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tareas")
    nombre = models.CharField(max_length=255, help_text="Nombre de la tarea")
    esta_completada = models.BooleanField(default=False, help_text="Indica si la tarea está completada")
    actualizada_en = models.DateTimeField(auto_now=True)

    def verificar_completitud(self):
        """Verifica si todas las sesiones que cuentan hacia la tarea están completadas."""
        if all(
            tarea_sesion.esta_completada
            for tarea_sesion in self.tareas_sesiones.filter(sesion__cuenta_para_completar=True)
        ):
            self.esta_completada = True
            self.save()

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"

class TareaSesion(models.Model):
    """Relaciona tareas con sesiones y guarda el estado de cada sesión."""
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="tareas_sesiones")
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    esta_completada = models.BooleanField(default=False, help_text="Indica si esta sesión ha sido completada")

    def __str__(self):
        return f"{self.sesion.nombre} para {self.tarea.nombre}"