from django.db import models
from django.conf import settings

class Nota(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, null=True, blank=True)  # Opcional, puede ser útil para resumir la nota.
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    prioridad = models.IntegerField(default=1)  # Un campo entero para representar la prioridad, por ejemplo, 1 a 5.
    activa = models.BooleanField(default=True)  # Un booleano para manejar si la nota está activa o archivada.
    categoria = models.CharField(max_length=100, null=True, blank=True)
    privada = models.BooleanField(default=False)
    recordatorio = models.DateTimeField(null=True, blank=True)
    importancia = models.CharField(max_length=50, choices=[('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja')], default='Media')

    def __str__(self):
        estado = "Activa" if self.activa else "Archivada"
        return f"{self.titulo or 'Sin título'} - {estado} (Creada el {self.fecha_creacion.strftime('%Y-%m-%d')})"
