from django.db import models

class HorarioMateria(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=10, choices=[
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado')
    ])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aula = models.CharField(max_length=50, blank=True, null=True)
    profesor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('materia', 'dia', 'hora_inicio', 'hora_fin')

    def __str__(self):
        return f"{self.materia.nombre} - {self.dia} {self.hora_inicio}-{self.hora_fin}"

class EventoAcademico(models.Model):
    TIPO_EVENTO = [
        ('INSCRIPCION', 'Inscripción'),
        ('DESINSCRIPCION', 'Desinscripción'),
        ('PRIORIDAD', 'Prioridad'),
        ('CERTIFICADO', 'Presentación de Certificado'),
        ('INICIO_CURSADA', 'Inicio de Cursada'),
        ('FINAL_CURSADA', 'Finalización de Cursada'),
        ('EXAMEN', 'Examen'),
        ('RECESO', 'Receso Académico'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_EVENTO)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    es_obligatorio = models.BooleanField(default=False)
    requiere_confirmacion = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)  # Para eventos virtuales
    documento_requerido = models.FileField(upload_to='documentos_eventos/', blank=True, null=True)
    recordatorio = models.BooleanField(default=False)  # Enviar notificación
    recordatorio_fecha = models.DateTimeField(blank=True, null=True)  # Cuándo enviar
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

class AsistenciaEvento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(EventoAcademico, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)
    fecha_confirmacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('usuario', 'evento')

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.nombre}"

class PlanificacionCuatrimestral(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='planificaciones')
    cuatrimestre = models.CharField(max_length=1, choices=[('1', 'Cuatrimestre 1'), ('2', 'Cuatrimestre 2')])
    año = models.IntegerField()
    materias = models.ManyToManyField(Materia, through='MateriaPlanificada')

    def __str__(self):
        return f"Planificación {self.cuatrimestre} - {self.año} ({self.estudiante.username})"

class MateriaPlanificada(models.Model):
    planificacion = models.ForeignKey(PlanificacionCuatrimestral, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    horarios = models.ManyToManyField(HorarioMateria)

    def __str__(self):
        return f"{self.materia.nombre} en {self.planificacion}"
