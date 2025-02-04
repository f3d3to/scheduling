# backend/evento_academico/models.py
# Python
from datetime import datetime, date, timedelta
# Django
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
# Proyecto
from users.models import Usuario

class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class HorarioBase(models.Model):
    DIA_CHOICES = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo')
    ]

    dia = models.CharField(max_length=10, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    descripcion_horario = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ['dia', 'hora_inicio']

class MetaAcademica(models.Model):
    estudiante = models.ForeignKey("users.Usuario", on_delete=models.CASCADE, related_name='metas')
    descripcion = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20)
    completada = models.BooleanField(default=False)
    relacion_materia = models.ForeignKey('plan_de_estudio.MateriaEstudiante', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.descripcion}: {self.descripcion[:30]}"

class ProgresoMateria(models.Model):
    materia_estudiante = models.OneToOneField('plan_de_estudio.MateriaEstudiante', on_delete=models.CASCADE, related_name='progreso')
    completados = models.PositiveIntegerField(default=0)
    totales = models.PositiveIntegerField(default=0)

    def porcentaje_completado(self):
        if self.totales == 0:
            return 0
        return (self.completados / self.totales) * 100

    def __str__(self):
        return f"Progreso {self.materia_estudiante.materia.nombre}"

class Recordatorio(models.Model):
    FRECUENCIA_CHOICES = [
        ('UNA_VEZ', 'Una vez'),
        ('DIARIO', 'Diario'),
        ('SEMANAL', 'Semanal'),
        ('MENSUAL', 'Mensual')
    ]

    METODO_CHOICES = [
        ('EMAIL', 'Email'),
        ('PUSH', 'Notificación push'),
        ('SMS', 'Mensaje SMS')
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='recordatorios')
    mensaje = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField()
    repetir = models.CharField(max_length=10, choices=FRECUENCIA_CHOICES, default='UNA_VEZ')
    medio_de_notificacion = models.CharField(max_length=5, choices=METODO_CHOICES, default='PUSH')

    def __str__(self):
        return f"Recordatorio: {self.mensaje[:20]}"

class TipoEventoAcademico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)

class EventoAcademico(HorarioBase):
    materia = models.ForeignKey('plan_de_estudio.Materia', on_delete=models.CASCADE, related_name='eventos')
    tipo = models.ForeignKey('TipoEventoAcademico', on_delete=models.CASCADE, related_name='eventos')
    es_obligatorio = models.BooleanField(default=True)
    recursos = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Eventos académicos'
        ordering = ['materia', 'dia', 'hora_inicio']

    def duracion(self):
        # Crear objetos datetime combinando una fecha ficticia con las horas
        fecha_ficticia = date.today()  # Fecha arbitraria
        inicio = datetime.combine(fecha_ficticia, self.hora_inicio)
        fin = datetime.combine(fecha_ficticia, self.hora_fin)

        # Manejar casos donde la hora_fin es menor que la hora_inicio (evento que cruza medianoche)
        if fin < inicio:
            fin += timedelta(days=1),

        # Calcular la diferencia
        return fin - inicio

    def __str__(self):
        return f"{self.materia.nombre} - {self.tipo.nombre}"

class PlanificacionAcademica(models.Model):
    TIPO_PLANIFICACION = [
        ('SEMANAL', 'Semanal'),
        ('CUATRIMESTRAL', 'Cuatrimestral'),
        ('ANUAL', 'Anual')
    ]

    estudiante = models.ForeignKey(
        "users.Usuario",
        on_delete=models.CASCADE,
        related_name='planificaciones'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_PLANIFICACION
    )
    cuatrimestre = models.CharField(
        max_length=1,
        choices=[('1', 'Cuatrimestre 1'), ('2', 'Cuatrimestre 2')],
        blank=True,
        null=True
    )
    nombre = models.CharField(max_length=100)
    semana = models.PositiveIntegerField(blank=True, null=True)  # Nueva campo
    año = models.PositiveIntegerField(default=datetime.now().year)  # Nuevo campo
    actividades = models.ManyToManyField(
        "evento_academico.EventoAcademico",
        through='ActividadPlanificada'
    )

    def calcular_carga_horaria(self):
        """
        Calcula la carga horaria total de las actividades asociadas.
        """
        return sum(
            evento.duracion().total_seconds() / 3600
            for evento in self.actividades.all()
        )

    def detectar_conflictos(self):
        """
        Detecta conflictos de horario entre las actividades asociadas.
        """
        eventos = self.actividades.all().order_by('dia', 'hora_inicio')
        conflictos = []
        for i in range(len(eventos) - 1):
            if (
                eventos[i].dia == eventos[i + 1].dia
                and eventos[i].hora_fin > eventos[i + 1].hora_inicio
            ):
                conflictos.append((eventos[i], eventos[i + 1]))
        return conflictos

    def clean(self):
        """
        Validaciones personalizadas para el modelo.
        """
        if self.tipo != 'CUATRIMESTRAL' and self.cuatrimestre is not None:
            raise ValidationError("El campo 'cuatrimestre' solo es válido para planificaciones cuatrimestrales.")

    def __str__(self):
        """
        Representación legible del objeto.
        """
        if self.tipo == 'SEMANAL':
            return f"Planificación Semana {self.semana} - {self.año}"
        elif self.tipo == 'CUATRIMESTRAL':
            return f"Planificación Cuatrimestre {self.cuatrimestre} - {self.año}"
        return f"Planificación {self.get_tipo_display()} {self.año}"

    class Meta:
        verbose_name_plural = "Planificaciones Académicas"

class ActividadPlanificada(models.Model):
    planificacion = models.ForeignKey(
        PlanificacionAcademica,
        on_delete=models.CASCADE,
        related_name='actividades_planificadas'
    )
    evento = models.ForeignKey(
        EventoAcademico,
        on_delete=models.CASCADE,
        related_name='actividades_planificadas'
    )
    completada = models.BooleanField(default=False)

    class Meta:
        unique_together = ('planificacion', 'evento')

    def __str__(self):
        return f"{self.evento} en {self.planificacion}"

class Recurrencia(models.Model):
    FRECUENCIAS = [
        ('diaria', 'Diaria'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ]
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIAS)
    intervalo = models.PositiveIntegerField(default=1)
    fin_recurrencia = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.frecuencia} cada {self.intervalo} unidad(es)"

class EventoCalendarioAcademico(models.Model):
    # Campos existentes...
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    inicio = models.DateTimeField()
    fin = models.DateTimeField(blank=True, null=True)
    todo_el_dia = models.BooleanField(default=False)
    color = models.CharField(max_length=20, blank=True, null=True)
    background_color = models.CharField(max_length=20, blank=True, null=True)
    border_color = models.CharField(max_length=20, blank=True, null=True)
    text_color = models.CharField(max_length=20, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, related_name='eventos')
    recurrencia = models.ForeignKey(Recurrencia, on_delete=models.SET_NULL, blank=True, null=True)

    # Nuevos campos para FullCalendar
    display = models.CharField(
        max_length=20,
        choices=[
            ('block', 'Bloque'),
            ('list-item', 'Elemento de lista'),
            ('background', 'Fondo'),
            ('none', 'Oculto'),
        ],
        default='block',
        help_text="Controla cómo se muestra el evento."
    )
    editable = models.BooleanField(default=True, help_text="Indica si el evento es editable.")
    start_editable = models.BooleanField(default=True, help_text="Indica si la fecha/hora de inicio es editable.")
    duration_editable = models.BooleanField(default=True, help_text="Indica si la duración es editable.")
    resource_editable = models.BooleanField(default=False, help_text="Indica si el evento puede moverse entre recursos.")
    exdate = models.CharField(max_length=255, blank=True, null=True, help_text="Fechas excluidas de la recurrencia.")
    class_names = models.CharField(max_length=255, blank=True, null=True, help_text="Clases CSS adicionales.")

    # Campos para la relación genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"

    def clean(self):
        if self.tipo.nombre == 'examen' and not self.fin:
            raise ValidationError("Los eventos de tipo 'examen' deben tener una fecha de fin.")
        if self.tipo.nombre == 'recordatorio' and self.todo_el_dia:
            raise ValidationError("Los eventos de tipo 'recordatorio' no pueden durar todo el día.")