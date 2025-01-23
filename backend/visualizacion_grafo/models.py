from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from plan_de_estudio.models import PlanDeEstudio, Materia, MateriaEstudiante
from plan_de_estudio.serializers import MateriaSerializer, MateriaEstudianteSerializer

class VisualizacionGrafo(models.Model):
    plan_de_estudio = models.OneToOneField(PlanDeEstudio, on_delete=models.CASCADE, related_name='visualizacion_grafo', null=True, blank=True)
    nombre = models.CharField(max_length=100, default="Visualización Principal")
    config_global = models.JSONField(default=dict, help_text="Representación de la configuracion global del grafo.")

    class Meta:
        verbose_name = "Configuración del Grafo"
        verbose_name_plural = "Configuraciones de Grafos"

    def generar_json_visualizacion(self, usuario=None):
        return {
            'nodos': [n.to_dict(usuario) for n in self.nodos.all()],
            'enlaces': [e.to_dict() for e in self.enlaces.all()],
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
            'correlativas': [m.codigo for m in self.materia.correlativas.all()],
            'anio': self.materia.anio,
            'metadata': MateriaSerializer(self.materia).data,
            'materia_estudiante': self._obtener_estado(usuario) if usuario else None
        }
        return data

    def _obtener_estado(self, usuario):
        if not usuario:
            return {}
        try:
            return MateriaEstudianteSerializer(self.materia.estudiantes.get(estudiante_id=usuario.id)).data
        except MateriaEstudiante.DoesNotExist:
            return None

class EnlaceGrafo(models.Model):
    grafo = models.ForeignKey(VisualizacionGrafo, on_delete=models.CASCADE, related_name='enlaces')
    fuente = models.ForeignKey(NodoGrafo, on_delete=models.CASCADE, related_name='enlaces_salientes')
    destino = models.ForeignKey(NodoGrafo, on_delete=models.CASCADE, related_name='enlaces_entrantes')
    config_visual = models.JSONField(default=dict, help_text="Configuración para visualizacion del enlace entre nodos.")

    def to_dict(self):
        return {
            'source': MateriaSerializer(self.fuente.materia).data["codigo"],
            'target': MateriaSerializer(self.destino.materia).data["codigo"],
            'config': self.config_visual
        }

# Señal para crear la VisualizacionGrafo al crear el PlanDeEstudio (sin nodos/enlaces todavía)
@receiver(post_save, sender=PlanDeEstudio)
def crear_estructura_grafo(sender, instance, created, **kwargs):
    if created:
        VisualizacionGrafo.objects.create(
            plan_de_estudio=instance,
            nombre=f"Grafo de {instance.nombre}",
            config_global={"tipo_layout": "jerarquico"}
        )

# Señal para crear NodoGrafo cuando se crea/actualiza una Materia
@receiver(post_save, sender=Materia)
def actualizar_nodos_grafo(sender, instance, created, **kwargs):
    visualizacion = instance.plan_de_estudio.visualizacion_grafo
    # Crear o actualizar nodo asociado a la materia
    NodoGrafo.objects.update_or_create(
        grafo=visualizacion,
        materia=instance,
        defaults={
            'config_visual': {
                'color': "#4CAF50" if instance.ciclo == "Básico" else "#2196F3"
            }
        }
    )

# Señal para crear EnlaceGrafo cuando se modifican correlativas
@receiver(m2m_changed, sender=Materia.correlativas.through)
def actualizar_enlaces_grafo(sender, instance, action, pk_set, **kwargs):
    if action not in ("post_add", "post_remove"):
        return

    visualizacion = instance.plan_de_estudio.visualizacion_grafo

    # 1. Tomar las correlativas actuales de la materia
    correlativas_actuales = set(instance.correlativas.all())

    # 2. Tomar todos los enlaces donde destino=instance
    enlaces_existentes = EnlaceGrafo.objects.filter(
        grafo=visualizacion,
        destino__materia=instance
    )

    # 3. Borrar solo los que no estén en correlativas_actuales
    for enlace in enlaces_existentes:
        corr_materia = enlace.fuente.materia
        if corr_materia not in correlativas_actuales:
            enlace.delete()

    # 4. Crear los enlaces que falten
    for correlativa in correlativas_actuales:
        ya_existe = enlaces_existentes.filter(
            fuente__materia=correlativa
        ).exists()
        if not ya_existe:
            fuente = visualizacion.nodos.get(materia=correlativa)
            destino = visualizacion.nodos.get(materia=instance)
            EnlaceGrafo.objects.create(
                grafo=visualizacion,
                fuente=fuente,
                destino=destino,
                config_visual={"tipo": "dependencia"}
            )
