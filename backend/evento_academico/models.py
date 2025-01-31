# backend/evento_academico/models.py
# Python
from datetime import datetime, date, timedelta
# Django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Proyecto
from users.models import Usuario

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
    TIPO_META = [
        ('RENDIMIENTO', 'Objetivo de rendimiento'),
        ('TIEMPO', 'Gestión de tiempo'),
        ('ENTREGA', 'Entrega de trabajos'),
        ('AUTOEVALUACION', 'Autoevaluación')
    ]

    estudiante = models.ForeignKey("users.Usuario", on_delete=models.CASCADE, related_name='metas')
    descripcion = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_META)
    fecha_limite = models.DateTimeField()
    prioridad = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3
    )
    completada = models.BooleanField(default=False)
    relacion_materia = models.ForeignKey('plan_de_estudio.MateriaEstudiante', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.descripcion[:30]}"

class ProgresoMateria(models.Model):
    materia_estudiante = models.OneToOneField('plan_de_estudio.MateriaEstudiante', on_delete=models.CASCADE, related_name='progreso')
    horas_estudiadas = models.PositiveIntegerField(default=0)
    temas_completados = models.PositiveIntegerField(default=0)
    ejercicios_resueltos = models.PositiveIntegerField(default=0)
    autoevaluaciones = models.PositiveIntegerField(default=0)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def porcentaje_completado(self):
        return (self.temas_completados / 10) * 100

    def __str__(self):
        return f"Progreso {self.materia_estudiante.materia.nombre}"

class RecordatorioPersonalizado(models.Model):
    FRECUENCIA_CHOICES = [
        ('UNA_VEZ', 'Una vez'),
        ('DIARIO', 'Diario'),
        ('SEMANAL', 'Semanal'),
        ('MENSUAL', 'Mensual')
    ]

    CANAL_CHOICES = [
        ('EMAIL', 'Email'),
        ('PUSH', 'Notificación push'),
        ('SMS', 'Mensaje SMS')
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='recordatorios')
    mensaje = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField()
    repetir = models.CharField(max_length=10, choices=FRECUENCIA_CHOICES, default='UNA_VEZ')
    canal = models.CharField(max_length=5, choices=CANAL_CHOICES, default='PUSH')

    def __str__(self):
        return f"Recordatorio: {self.mensaje[:20]}"


class EventoAcademico(HorarioBase):
    TIPO_EVENTO = [
        ('CLASE', 'Clase'),
        ('EXAMEN', 'Examen'),
        ('CONSULTA', 'Consulta'),
        ('ENTREGA', 'Entrega de TP'),
        ('RECUPERATORIO', 'Recuperatorio')
    ]

    materia = models.ForeignKey('plan_de_estudio.Materia', on_delete=models.CASCADE, related_name='eventos')
    tipo = models.CharField(max_length=20, choices=TIPO_EVENTO)
    aula = models.CharField(max_length=50)
    profesor = models.CharField(max_length=100)
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

class PlanificacionAcademica(models.Model):
    TIPO_PLANIFICACION = [
        ('SEMANAL', 'Semanal'),
        ('CUATRIMESTRAL', 'Cuatrimestral'),
        ('ANUAL', 'Anual')
    ]

    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='planificaciones')
    tipo = models.CharField(max_length=20, choices=TIPO_PLANIFICACION)
    cuatrimestre = models.CharField(max_length=1,
                                  choices=[('1', 'Cuatrimestre 1'), ('2', 'Cuatrimestre 2')],
                                  blank=True, null=True)
    año = models.IntegerField()
    semana = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(52)],
        blank=True, null=True
    )
    nombre = models.CharField(max_length=100)
    actividades = models.ManyToManyField(EventoAcademico, through='ActividadPlanificada')

    # # Métodos clave
    # def calcular_carga_horaria(self):
    #     return sum(evento.duracion().total_seconds() / 3600
    #              for evento in self.actividades.all())

    # def detectar_conflictos(self):
    #     eventos = self.actividades.all().order_by('dia', 'hora_inicio')
    #     return [(eventos[i], eventos[i+1])
    #           for i in range(len(eventos)-1)
    #           if eventos[i].dia == eventos[i+1].dia
    #           and eventos[i].hora_fin > eventos[i+1].hora_inicio]

    def __str__(self):
        if self.tipo == 'SEMANAL':
            return f"Planificación Semana {self.semana} - {self.año}"
        return f"Planificación {self.get_tipo_display()} {self.año}"

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


class EventoCalendarioAcademico(models.Model):
    TIPOS_EVENTO = [
        ('actividad', 'Actividad'),
        ('tarea', 'Tarea'),
        ('materia', 'Materia'),
        ('meta', 'Meta Académica'),
        ('recordatorio', 'Recordatorio'),
        # Agregar más tipos según sea necesario
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    inicio = models.DateTimeField()
    fin = models.DateTimeField(blank=True, null=True)
    todo_el_dia = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50, choices=TIPOS_EVENTO)

    # Campos para la relación genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"