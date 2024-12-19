
from django.conf import settings
from django.db import models

class Estado(models.Model):
    """
    Modelo que representa un estado genérico que puede ser utilizado en cualquier entidad.
    """
    nombre = models.CharField(max_length=50, unique=True, help_text="Nombre del estado (por ejemplo, Pendiente, En Progreso, Completado).")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción opcional del estado.")
    color = models.CharField(max_length=7, default="#FFFFFF", help_text="Color asociado al estado.")  # Opcional para mostrar en frontend
    orden = models.PositiveIntegerField(default=0, help_text="Orden de prioridad del estado.")  # Para ordenarlos en interfaces

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['orden']  # Los estados se ordenarán por prioridad

class BaseConEstado(models.Model):
    """
    Modelo abstracto que incluye un estado dinámico.
    """
    estado = models.ForeignKey(
        Estado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Estado actual de la entidad."
    )
    fecha_cambio_estado = models.DateTimeField(auto_now=True, help_text="Fecha del último cambio de estado.")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.estado.nombre if self.estado else 'Sin Estado'}"


class EstructuraPlanificador(models.Model):
    """
    Modelo que representa las posibles combinaciones dinámicas para configurar un planificador.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Usuario que creó esta configuración."
    )
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre de la estructura (por ejemplo, Plan Semanal, Plan Mensual, Control de Estudio)."
    )
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción opcional de la estructura.")
    configuracion = models.JSONField(
        help_text=(
            "Configuración dinámica en formato JSON. "
            "Por ejemplo, {'tipo': 'tabla', 'columnas': ['Lunes', 'Martes'], 'filas': ['8:00', '9:00']}."
        )
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación de la estructura.")
    fecha_modificacion = models.DateTimeField(auto_now=True, help_text="Última modificación de la estructura.")

    def __str__(self):
        return f"{self.nombre} ({self.usuario.username})"


class TipoPlanificador(models.Model):
    nombre = models.CharField(max_length=50, unique=True, help_text="Nombre del tipo de planificador.")
    descripcion = models.TextField(blank=True, null=True)


class Planificador(models.Model):
    """
    Modelo principal que representa un tipo de planificador, como un calendario o un organizador de tareas.
    """

    nombre = models.CharField(max_length=255, help_text="Nombre del planificador.")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción del planificador.")
    tipo = models.ForeignKey(TipoPlanificador, on_delete=models.SET_NULL, null=True, blank=True, help_text="Tipo de Planificador asociada al planificador.")
    color = models.CharField(max_length=7, default="#FFFFFF", help_text="Color asociado al planificador.")  # Color asignado
    fecha_creacion = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación del planificador.")
    fecha_modificacion = models.DateTimeField(auto_now=True, help_text="Fecha de última modificación del planificador.")
    estructura = models.ForeignKey(
        EstructuraPlanificador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Estructura dinámica asociada al planificador."
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Usuario propietario del planificador.")

    def __str__(self):
        return self.nombre


class Actividad(BaseConEstado):
    """
    Modelo que representa una actividad dentro de un planificador.
    Puede ser algo como una clase, un evento o un objetivo específico.
    """

    planificador = models.ForeignKey(Planificador, related_name="actividades", on_delete=models.CASCADE, help_text="Planificador al que pertenece la actividad.")
    nombre = models.CharField(max_length=255, help_text="Nombre de la actividad.")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción de la actividad.")
    fecha_inicio = models.DateField(blank=True, null=True, help_text="Fecha de inicio de la actividad.")
    fecha_fin = models.DateField(blank=True, null=True, help_text="Fecha de finalización de la actividad.")
    color = models.CharField(max_length=7, default="#0000FF", help_text="Color asociado a la actividad.")  # Color específico de la actividad

    def __str__(self):
        return f"{self.nombre} ({self.estado})"


class Tarea(BaseConEstado):
    actividad = models.ForeignKey(Actividad, related_name="tareas", on_delete=models.CASCADE, help_text="Actividad asociada.")
    nombre = models.CharField(max_length=255, help_text="Nombre de la tarea.")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción de la tarea.")
    fecha_limite = models.DateField(blank=True, null=True, help_text="Fecha límite para completar la tarea.")
    color = models.CharField(max_length=7, default="#FF0000", help_text="Color asociado a la tarea.")

    def __str__(self):
        return f"{self.nombre} ({self.estado.nombre if self.estado else 'Sin Estado'})"

class Objetivo(models.Model):
    planificador = models.ForeignKey(Planificador, related_name="objetivos", on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_objetivo = models.DateField()
    completado = models.BooleanField(default=False)

class RegistroProgreso(models.Model):
    """
    Modelo para registrar el progreso de actividades y tareas a lo largo del tiempo.
    """
    actividad = models.ForeignKey(Actividad, related_name="registros_progreso", on_delete=models.CASCADE, help_text="Actividad asociada al registro.")
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje de progreso.")
    fecha_registro = models.DateTimeField(auto_now_add=True, help_text="Fecha en que se registró el progreso.")

    def __str__(self):
        return f"{self.actividad.nombre} - {self.porcentaje}% ({self.fecha_registro})"
