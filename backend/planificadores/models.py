
# Python
import json
# Django
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models, transaction

class Estado(models.Model):
    """
    Modelo que representa un estado genérico que puede ser utilizado en cualquier entidad.
    """
    nombre = models.CharField(max_length=50, unique=True, help_text="Nombre del estado (por ejemplo, Pendiente, En Progreso, Completado).")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción opcional del estado.")
    color = models.CharField(max_length=7, default="#FFFFFF", help_text="Color asociado al estado.")  # Opcional para mostrar en frontend
    orden = models.PositiveIntegerField(default=0, help_text="Orden de prioridad del estado.")  # Para ordenarlos en interfaces

    def __str__(self):
        return f"Estado: {self.nombre} (Orden: {self.orden})"

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
        return f"Estado actual: {self.estado.nombre if self.estado else 'Sin Estado'} - Última modificación: {self.fecha_cambio_estado.strftime('%Y-%m-%d %H:%M:%S')}"

class BaseEstructura(models.Model):
    nombre = models.CharField(max_length=100)
    configuracion = models.JSONField(default=dict)

    class Meta:
        abstract = True

class EstructuraPlanificador(BaseEstructura):
    """
    Modelo para gestionar la estructura de un planificador en forma de cuadrícula.
    Optimizado para manejar dinámicamente filas, columnas y sus celdas.
    """
    filas = models.PositiveIntegerField(default=1, help_text="Número total de filas de la cuadrícula.")
    columnas = models.PositiveIntegerField(default=1, help_text="Número total de columnas de la cuadrícula.")
    ancho_columna = models.PositiveIntegerField(default=100, help_text="Ancho de las columnas en píxeles.")
    tabla = models.JSONField(default=dict, help_text="Representación de la tabla como diccionario.")

    def __str__(self):
        return f"EstructuraPlanificador: {self.nombre} ({self.filas}x{self.columnas})"


class Planificador(models.Model):
    """
    Modelo que representa un planificador, utilizado para gestionar actividades, celdas y objetivos.
    """
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)
    estructura = models.ForeignKey(EstructuraPlanificador, on_delete=models.SET_NULL, null=True)

    # Esto está raro. ¿La relación es  X -1vs1-> Planificador?
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Tipo de la entidad asociada al planificador."
    )
    object_id = models.PositiveIntegerField(null=True, blank=True, help_text="ID de la entidad asociada al planificador.")
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        estructura_str = f"Estructura: {self.estructura.nombre}" if self.estructura else "Sin estructura"
        return f"Planificador: {self.nombre} (Tipo: {self.tipo}, {estructura_str})"

class Celda(models.Model):
    """
    Representa una celda dentro de un planificador, utilizada para organizar contenido.
    """
    planificador = models.ForeignKey(Planificador, related_name="celdas", on_delete=models.CASCADE)
    contenido = models.TextField(blank=True, null=True)
    fila = models.IntegerField(help_text="Número de la fila en la cuadrícula.")
    columna = models.IntegerField(help_text="Número de la columna en la cuadrícula.")

    def __str__(self):
        contenido_preview = self.contenido[:20] + "..." if self.contenido else "Sin contenido"
        return f"Celda del planificador '{self.planificador.nombre}': {contenido_preview}"

    def mover(self, nueva_fila, nueva_columna):
        """
        Mueve la celda a una nueva posición en la cuadrícula.
        """
        self.fila = nueva_fila
        self.columna = nueva_columna
        self.save()

class Elemento(models.Model):
    """
    Representa un elemento individual dentro de una celda, con soporte para estructuras configurables y relaciones genéricas.
    """
    nombre = models.CharField(max_length=255)
    celda = models.ForeignKey(Celda, related_name="elementos", on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        estructura_str = f"Estructura: {self.estructura.nombre}" if self.estructura else "Sin estructura"
        return f"Elemento: {self.nombre} ({estructura_str}, Celda: {self.celda.id})"


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
    evento_academico = models.ForeignKey("evento_academico.EventoAcademico", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Actividad: {self.nombre} ({self.estado.nombre if self.estado else 'Sin Estado'}, Planificador: {self.planificador.nombre})"

class Tarea(BaseConEstado):
    """
    Representa una tarea específica asociada a una actividad dentro de un planificador.
    """
    actividad = models.ForeignKey(Actividad, related_name="tareas", on_delete=models.CASCADE, help_text="Actividad asociada.")
    nombre = models.CharField(max_length=255, help_text="Nombre de la tarea.")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción de la tarea.")
    fecha_limite = models.DateField(blank=True, null=True, help_text="Fecha límite para completar la tarea.")
    color = models.CharField(max_length=7, default="#FF0000", help_text="Color asociado a la tarea.")
    esta_realizada= models.BooleanField(default=False, help_text="Indica si la tarea está completada")
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        estado_str = self.estado.nombre if self.estado else "Sin Estado"
        return f"Tarea: {self.nombre} ({estado_str}, Completada: {'Sí' if self.esta_realizada else 'No'})"

class Objetivo(models.Model):
    """
    Representa un objetivo que puede estar asociado a cualquier entidad (Planificador, Actividad, Tarea, etc.).
    """
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="Tipo de la entidad a la que está asociado el objetivo."
    )
    object_id = models.PositiveIntegerField(help_text="ID de la entidad a la que está asociado el objetivo.")
    content_object = GenericForeignKey('content_type', 'object_id')
    descripcion = models.TextField(help_text="Descripción del objetivo.")
    fecha_objetivo = models.DateField(help_text="Fecha límite para cumplir el objetivo.")
    completado = models.BooleanField(default=False, help_text="Indica si el objetivo ha sido completado.")

    def __str__(self):
        return f"Objetivo: {self.descripcion[:20]}... ({'Completado' if self.completado else 'Pendiente'})"
