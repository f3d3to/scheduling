from django.db import models
from plan_de_estudio.models import PlanDeEstudio, MateriaEstudiante

class VisualizacionGrafo(models.Model):
    plan = models.ForeignKey('plan_de_estudio.PlanDeEstudio', on_delete=models.CASCADE, related_name='grafos')
    nombre = models.CharField(max_length=100, default="Visualización Principal")
    config_global = models.JSONField(default=dict, help_text="Representación de la configuracion global del grafo.")

    class Meta:
        verbose_name = "Configuración del Grafo"
        verbose_name_plural = "Configuraciones de Grafos"

    def generar_json_visualizacion(self, usuario=None):
        return {
            'nodos': [n.to_dict(usuario) for n in self.nodos.all()],
            'enlaces': [e.to_dict() for e in self.enlaces.all()],
            'metadatos': self._calcular_metadatos(usuario)
        }

    def _calcular_metadatos(self, usuario):
        if not usuario:
            return {}

        return {
            'creditos_aprobados': self._calcular_creditos(usuario),
            'progreso': self._calcular_progreso(usuario)
        }

class NodoGrafo(models.Model):
    grafo = models.ForeignKey(VisualizacionGrafo, on_delete=models.CASCADE, related_name='nodos')
    materia = models.ForeignKey('plan_de_estudio.Materia', on_delete=models.CASCADE)

    # Propiedades de visualización
    pos_x = models.FloatField(default=0)
    pos_y = models.FloatField(default=0)
    config_visual = models.JSONField(default=dict, help_text="Configuración para visualizacion del nodo.")

    def to_dict(self, usuario=None):
        data = {
            'id': self.materia_id,
            'posicion': [self.pos_x, self.pos_y],
            'config': self.config_visual,
            'metadata': self._obtener_estado(usuario)
        }
        return data

    def _obtener_estado(self, usuario):
        if not usuario:
            return {}

        try:
            return MateriaEstudiante.objects.get(
                materia=self.materia,
                estudiante=usuario
            ).estado
        except MateriaEstudiante.DoesNotExist:
            return 'pendiente'

class EnlaceGrafo(models.Model):
    grafo = models.ForeignKey(VisualizacionGrafo, on_delete=models.CASCADE, related_name='enlaces')
    fuente = models.ForeignKey(NodoGrafo, on_delete=models.CASCADE, related_name='enlaces_salientes')
    destino = models.ForeignKey(NodoGrafo, on_delete=models.CASCADE, related_name='enlaces_entrantes')
    config_visual = models.JSONField(default=dict, help_text="Configuración para visualizacion del enlace entre nodos.")

    def to_dict(self):
        return {
            'fuente': self.fuente.materia_id,
            'destino': self.destino.materia_id,
            'config': self.config_visual
        }