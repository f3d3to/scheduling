from django.db import models

class PlanDeEstudio(models.Model):
    nombre = models.CharField(max_length=1000)
    año_creacion = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    planificadores = models.ManyToManyField(
        'planificadores.Planificador',
        blank=True,
        related_name="planes_de_estudio",
        help_text="Planificadores asociados al plan de estudios."
    )
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
