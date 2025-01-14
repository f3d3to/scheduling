from django.db import models
from users.models import Usuario
class PlanDeEstudio(models.Model):
    nombre = models.CharField(max_length=1000)
    año_creacion = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.nombre} ({self.año_creacion})"

    class Meta:
        verbose_name = "Plan de Estudio"
        verbose_name_plural = "Planes de Estudio"
        ordering = ['año_creacion', 'nombre']

class Materia(models.Model):
    plan_de_estudio = models.ForeignKey(PlanDeEstudio, related_name='materias', on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100)
    anio = models.IntegerField(blank=True, null=True)
    ciclo = models.CharField(max_length=50, blank=True, null=True)
    cuatrimestre = models.IntegerField(blank=True, null=True)
    condicion = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=1000)
    formato_didactico = models.CharField(max_length=50, blank=True, null=True)
    ch_semanal = models.IntegerField(blank=True, null=True)
    ch_cuatrimestral = models.IntegerField(blank=True, null=True)
    creditos = models.IntegerField(blank=True, null=True)
    ch_presencial = models.IntegerField(blank=True, null=True)
    ch_distancia = models.IntegerField(blank=True, null=True)
    ch_total = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    correlativas = models.ManyToManyField('self', symmetrical=False, related_name='requerida_por', blank=True)

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        ordering = ['codigo']


class MateriaEstudiante(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="materias")
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, related_name="estudiantes")

    # Campos principales
    nota_final = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)  # Ejemplo: 7.50
    final_obligatorio = models.BooleanField(default=True)
    catedra = models.CharField(max_length=200, blank=True, null=True)  # Nombre de la cátedra

    # REVISION DE LA MATERIA PARA ESTADISTICA. != COMENTARIOS
    comentarios = models.TextField(blank=True, null=True)
    intentos = models.PositiveIntegerField(default=0)  # Número de intentos

    # INFORMACION - HACE SEMINARIOS, TIENE GRUPO DE INVS, TIENE UN LABORATORIO, ETC-
    comentarios_docente = models.TextField(blank=True, null=True)  # Comentarios del docente

    # Nuevos campos
    estado = models.CharField(
        max_length=50,
        choices=[
            ('pendiente', 'Pendiente'),
            ('cursando', 'Cursando'),
            ('aprobada', 'Aprobada'),
            ('desaprobada', 'Desaprobada'),
            ('promocionada', 'Promocionada'),
        ],
        default='pendiente'
    )
    # FECHAS RELEVANTES -EVENTOS-.
    fecha_inscripcion = models.DateField(blank=True, null=True)  # Fecha de inscripción

    metodo_aprobacion = models.CharField(
        max_length=50,
        choices=[
            ('final', 'Examen Final'),
            ('promocion', 'Promoción Directa'),
            ('equivalencia', 'Equivalencia'),
        ],
        blank=True,
        null=True
    )
    creditos_asignados = models.IntegerField(blank=True, null=True)  # Créditos asignados

    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('estudiante', 'materia')
        verbose_name = "Materia Estudiante"
        verbose_name_plural = "Materias Estudiantes"
        ordering = ['materia__anio', 'materia__codigo']

    def __str__(self):
        return f"{self.estudiante.username} - {self.materia.nombre}"


class TipoEvaluacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Ejemplo: Parcial, TP, Integrador
    descripcion = models.TextField(blank=True, null=True)  # Detalles opcionales sobre el tipo
    peso_defecto = models.DecimalField(
        max_digits=4, decimal_places=2, default=1.0,
        help_text="Peso por defecto asignado a este tipo de evaluación"
    )

    def __str__(self):
        return self.nombre


class Evaluacion(models.Model):

    materia_estudiante = models.ForeignKey(
        'MateriaEstudiante', on_delete=models.CASCADE, related_name='evaluaciones'
    )
    tipo = models.ForeignKey(
        'TipoEvaluacion', on_delete=models.CASCADE, related_name='evaluaciones'
    )

    descripcion = models.CharField(max_length=200, blank=True, null=True)  # Detalles de la evaluación
    nota = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ['materia_estudiante', 'tipo']

    def __str__(self):
        return f"{self.materia_estudiante} - {self.tipo} ({self.nota})"