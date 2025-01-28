# backend/evento_academico/models.py
# Django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Proyecto
from users.models import Usuario
from planificadores.models import Evento

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
        return (self.temas_completados / self.materia_estudiante.materia.cantidad_temas) * 100

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
    relacion_evento = models.ForeignKey('planificadores.Evento', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Recordatorio: {self.mensaje[:20]}"

class EventoAsociadoAcademico(models.Model):
    TIPO_RELACION = [
        ('EXAMEN_MATERIA', 'Examen → Materia'),
        ('ENTREGA_TP', 'Entrega → Trabajo Práctico'),
        ('CLASE_PRACTICA', 'Clase Práctica → Teórica'),
        ('RECUPERATORIO', 'Recuperatorio → Evaluación')
    ]

    evento_origen = models.ForeignKey('EventoAcademico', on_delete=models.CASCADE, related_name='relaciones_origen')
    evento_destino = models.ForeignKey('EventoAcademico', on_delete=models.CASCADE, related_name='relaciones_destino')
    tipo_relacion = models.CharField(max_length=20, choices=TIPO_RELACION)
    peso = models.FloatField(default=1.0,
                           validators=[MinValueValidator(0.1), MaxValueValidator(5.0)])

    class Meta:
        unique_together = ('evento_origen', 'evento_destino')

    def __str__(self):
        return f"{self.get_tipo_relacion_display()}: {self.evento_origen} → {self.evento_destino}"

class EventoAcademico(HorarioBase, Evento):
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
        return self.hora_fin - self.hora_inicio

    def __str__(self):
        return f"{self.get_tipo_display()} {self.materia.nombre} - {self.dia} {self.hora_inicio}"

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
    actividades = models.ManyToManyField('planificadores.Evento', through='ActividadPlanificada')

    # Métodos clave
    def calcular_carga_horaria(self):
        return sum(evento.duracion().total_seconds() / 3600
                 for evento in self.actividades.all())

    def detectar_conflictos(self):
        eventos = self.actividades.all().order_by('dia', 'hora_inicio')
        return [(eventos[i], eventos[i+1])
              for i in range(len(eventos)-1)
              if eventos[i].dia == eventos[i+1].dia
              and eventos[i].hora_fin > eventos[i+1].hora_inicio]

    def __str__(self):
        if self.tipo == 'SEMANAL':
            return f"Planificación Semana {self.semana} - {self.año}"
        return f"Planificación {self.get_tipo_display()} {self.año}"

class ActividadPlanificada(models.Model):
    planificacion = models.ForeignKey(PlanificacionAcademica, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)

    class Meta:
        unique_together = ('planificacion', 'evento')

    def __str__(self):
        return f"{self.evento} en {self.planificacion}"
