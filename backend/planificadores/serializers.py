from rest_framework import serializers
from .models import Planificador, EstructuraPlanificador, Actividad, Tarea, Estado

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = "__all__"

class EstructuraPlanificadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstructuraPlanificador
        fields = "__all__"

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = "__all__"

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = "__all__"

class PlanificadorSerializer(serializers.ModelSerializer):
    actividades = ActividadSerializer(many=True, read_only=True)

    class Meta:
        model = Planificador
        fields = "__all__"
