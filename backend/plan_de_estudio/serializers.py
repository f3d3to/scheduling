from rest_framework import serializers
from .models import PlanDeEstudio, Materia, MateriaEstudiante, Evaluacion, TipoEvaluacion

class MateriaSerializer(serializers.ModelSerializer):
    correlativas = serializers.StringRelatedField(many=True)

    class Meta:
        model = Materia
        fields = '__all__'

class PlanDeEstudioCiclosSerializer(serializers.ModelSerializer):
    anios = serializers.SerializerMethodField()

    class Meta:
        model = PlanDeEstudio
        fields = ['id', 'nombre', 'año_creacion', 'descripcion','anios']

    def get_anios(self, obj):
        materias_por_anio = {}
        materias = obj.materias.all()

        for materia in materias:
            anio = materia.anio  # Asegúrate de que el modelo Materia tenga un campo 'anio'
            if anio not in materias_por_anio:
                materias_por_anio[anio] = []
            materias_por_anio[anio].append(MateriaSerializer(materia).data)

        return {anio: materias_por_anio[anio] for anio in sorted(materias_por_anio.keys())}


class MateriaEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MateriaEstudiante
        fields = "__all__"
        read_only_fields = ['estudiante']


class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = "__all__"


class TipoEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEvaluacion
        fields = "__all__"

class PlanDeEstudioSerializer(serializers.ModelSerializer):
    materias = MateriaSerializer(many=True, read_only=True)

    class Meta:
        model = PlanDeEstudio
        fields = '__all__'

from django.db.models import Prefetch

class GrafoSerializer(serializers.Serializer):
    nodos = serializers.SerializerMethodField()
    relaciones = serializers.SerializerMethodField()

    def get_nodos(self, instance):
        plan_de_estudio_id = self.context['request'].query_params.get('plan_de_estudio__id')
        estudiante_id = self.context['request'].query_params.get('estudiante_id')
        nodos = []

        if plan_de_estudio_id:
            materias = Materia.objects.filter(
                plan_de_estudio__id=plan_de_estudio_id
            ).prefetch_related('correlativas')

            if estudiante_id:
                # Obtener todas las MateriaEstudiante del estudiante en una sola consulta
                materias_estudiante = MateriaEstudiante.objects.filter(
                    estudiante_id=estudiante_id, materia__plan_de_estudio__id=plan_de_estudio_id
                ).select_related('materia')

                # Crear un diccionario para acceder rápidamente a la MateriaEstudiante por ID de materia
                materias_estudiante_dict = {me.materia.id: me for me in materias_estudiante}
            else:
                materias_estudiante_dict = {}

            for materia in materias:
                nodo = {
                    "id": materia.id,
                    "tipo": "materia",
                    "materia_endpoint": f"http://localhost:8000/materias/{materia.codigo}/",
                    "materia_estudiante_endpoint": None,
                }

                # Usar el diccionario para obtener la MateriaEstudiante, si existe
                materia_estudiante = materias_estudiante_dict.get(materia.id)
                if materia_estudiante:
                    nodo["materia_estudiante_endpoint"] = f"http://localhost:8000/materias/estudiantes/{materia_estudiante.pk}/"

                nodos.append(nodo)

        return nodos

    def get_relaciones(self, instance):
        plan_de_estudio_id = self.context['request'].query_params.get('plan_de_estudio__id')
        relaciones = []

        if plan_de_estudio_id:
            materias = Materia.objects.filter(plan_de_estudio__id=plan_de_estudio_id).prefetch_related(
                Prefetch('correlativas', queryset=Materia.objects.all())
            )

            correlativas_por_materia = {}
            for materia in materias:
                correlativas_por_materia[materia.id] = [
                    correlativa.id for correlativa in materia.correlativas.all()
                ]

            for materia in materias:
                for correlativa_id in correlativas_por_materia.get(materia.id, []):
                    relacion = {
                        "source": correlativa_id,
                        "target": materia.id,
                        "tipo": "correlativa"
                    }
                    relaciones.append(relacion)

        return relaciones