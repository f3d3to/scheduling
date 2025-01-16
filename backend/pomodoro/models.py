# pomodoro/models.py
from django.db import models

class Sesion(models.Model):
    """Representa un tipo de sesión de Pomodoro (e.g., Estudio, Descanso, etc.)."""
    nombre = models.CharField(max_length=255, help_text="Nombre de la sesión (Estudio, Repaso, Descanso, etc.)")
    duracion_minutos = models.PositiveIntegerField(help_text="Duración de la sesión en minutos para ser completada")
    es_obligatoria = models.BooleanField(default=True, help_text="Indica si esta sesión es obligatoria para completar la tarea")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=7, default="#FFFFFF", help_text="Color asociado al estado.")
    def __str__(self):
        obligatoria_str = "Obligatoria" if self.es_obligatoria else "Opcional"
        return f"{self.nombre} ({self.duracion_minutos} min, {obligatoria_str})"

class TareaTimer(models.Model):
    tarea = models.OneToOneField('planificadores.Tarea', on_delete=models.CASCADE, related_name='tarea_timer')
    cantidad_para_completar = models.PositiveIntegerField(help_text="Número total de sesiones necesarias para completar la tarea")
    cantidad_completadas = models.PositiveIntegerField(default=0, help_text="Número de sesiones completadas actualmente")
    sesiones = models.ManyToManyField(Sesion, blank=True, help_text="Sesiones asociadas a esta tarea.")

    def verificar_completitud(self):
        """Verifica si la tarea está completada según las sesiones necesarias."""
        self.tarea.esta_realizada = self.cantidad_completadas >= self.cantidad_para_completar
        self.tarea.save()

    def __str__(self):
        progreso = f"{self.cantidad_completadas}/{self.cantidad_para_completar}"
        estado = "Completada" if self.cantidad_completadas >= self.cantidad_para_completar else "En progreso"
        return f"Tarea: {self.tarea.nombre} ({progreso} - {estado})"

