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