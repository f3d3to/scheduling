
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


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

class BaseEstructura(models.Model):
    nombre = models.CharField(max_length=100)
    configuracion = models.JSONField(default=dict)

    class Meta:
        abstract = True

class EstructuraPlanificador(BaseEstructura):
    # Aquí puedes agregar atributos específicos de la estructura del planificador si es necesario
    pass

class EstructuraElemento(BaseEstructura):
    fecha_edicion = models.DateTimeField(auto_now=True)
    html_visualizacion = models.TextField()

class Planificador(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)
    estructura = models.ForeignKey(EstructuraPlanificador, on_delete=models.SET_NULL, null=True)
    # Otros campos como usuario, etc.

class Celda(models.Model):
    planificador = models.ForeignKey(Planificador, related_name="celdas", on_delete=models.CASCADE)
    contenido = models.TextField(blank=True, null=True)

class Elemento(models.Model):
    nombre = models.CharField(max_length=255)
    celda = models.ForeignKey(Celda, related_name="elementos", on_delete=models.CASCADE)
    estructura = models.ForeignKey(EstructuraElemento, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class Mensaje(models.Model):
    tipo = models.CharField(max_length=50)
    icono = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=7, default="#FFFFFF")

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
    esta_realizada= models.BooleanField(default=False, help_text="Indica si la tarea está completada")
    fecha_actualizacion = models.DateTimeField(auto_now=True)

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

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, default="#FFFFFF", help_text="Color en formato hexadecimal")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción opcional de la etiqueta")

class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Recurrente(models.Model):
    frecuencia = models.CharField(max_length=50)  # Diaria, Semanal, Mensual, etc.
    proxima_fecha = models.DateField()

class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"

class EventoAsociado(models.Model):
    evento = models.ForeignKey(Evento, related_name="asociaciones", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.evento.nombre} asociado con {self.content_object}"
