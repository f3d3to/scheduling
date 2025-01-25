# Django

from django.db import models
# Proyecto
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
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        ordering = ['codigo']


class MateriaEstudiante(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="materias")
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE, related_name="estudiantes")

    # Campos principales
    nota_final = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    final_obligatorio = models.BooleanField(default=True)
    catedra = models.CharField(max_length=200, blank=True, null=True)

    # REVISION DE LA MATERIA PARA ESTADISTICA. != COMENTARIOS
    comentarios = models.TextField(blank=True, null=True)
    intentos = models.PositiveIntegerField(default=0)

    # INFORMACION - HACE SEMINARIOS, TIENE GRUPO DE INVS, TIENE UN LABORATORIO, ETC-
    comentarios_docente = models.TextField(blank=True, null=True)

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
    fecha_inscripcion = models.DateField(blank=True, null=True)

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
    creditos_asignados = models.IntegerField(blank=True, null=True)

    fecha_actualizacion = models.DateTimeField(auto_now=True)

    dificultad = models.PositiveIntegerField(blank=True, null=True)

    disponible = models.BooleanField(default=False)

    class Meta:
        unique_together = ('estudiante', 'materia')
        verbose_name = "Materia Estudiante"
        verbose_name_plural = "Materias Estudiantes"
        ordering = ['materia__anio', 'materia__codigo']

    def __str__(self):
        return f"{self.estudiante.username} - {self.materia.nombre}"
    def verificar_disponibilidad(self):
        # Si la materia YA está aprobada/promocionada, NO está disponible
        if self.estado in ['promocionada']:
            return False

        # Si no tiene correlativas, está disponible (si está pendiente)
        if not self.materia.correlativas.exists():
            return True

        # Contar correlativas no promocionadas
        correlativas_no_promocionadas = MateriaEstudiante.objects.filter(
            estudiante=self.estudiante,
            materia__in=self.materia.correlativas.all()
        ).exclude(estado='promocionada').count()

        return correlativas_no_promocionadas == 0

    def save(self, *args, **kwargs):
        # Calcular disponibilidad antes de guardar
        nueva_disponibilidad = self.verificar_disponibilidad()

        # Evitar guardar si no hay cambios
        if self.pk:
            vieja_disponibilidad = MateriaEstudiante.objects.get(pk=self.pk).disponible
            if vieja_disponibilidad == nueva_disponibilidad:
                super().save(*args, **kwargs)
                return

        self.disponible = nueva_disponibilidad
        super().save(*args, **kwargs)

        # Actualizar materias dependientes SIN usar señales
        self.actualizar_materias_dependientes()

    def actualizar_materias_dependientes(self):
        """
        Actualiza el campo 'disponible' de las materias que dependen de esta.
        Usa bulk_update para evitar recursividad.
        """
        # Obtener materias que tienen esta materia como correlativa
        materias_dependientes = Materia.objects.filter(correlativas=self.materia)

        # Obtener instancias MateriaEstudiante a actualizar
        estudiantes_dependientes = MateriaEstudiante.objects.filter(
            estudiante=self.estudiante,
            materia__in=materias_dependientes
        )

        # Calcular nueva disponibilidad para cada una
        actualizaciones = []
        for me in estudiantes_dependientes:
            nueva_disponibilidad = me.verificar_disponibilidad()
            if me.disponible != nueva_disponibilidad:
                me.disponible = nueva_disponibilidad
                actualizaciones.append(me)

        # Actualizar en lote (no dispara señales)
        if actualizaciones:
            MateriaEstudiante.objects.bulk_update(actualizaciones, ['disponible'])

class TipoEvaluacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
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

    descripcion = models.CharField(max_length=200, blank=True, null=True)
    nota = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ['materia_estudiante', 'tipo']

    def __str__(self):
        return f"{self.materia_estudiante} - {self.tipo} ({self.nota})"
