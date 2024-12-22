from rest_framework import serializers
from .models import (Planificador, EstructuraPlanificador, Actividad, Tarea, Estado,
                     TipoPlanificador, Objetivo, RegistroProgreso)

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

class TipoPlanificadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPlanificador
        fields = '__all__'  # Incluye todos los campos del modelo

class ObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objetivo
        fields = '__all__'  # Incluye todos los campos del modelo

class RegistroProgresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroProgreso
        fields = '__all__'  # Incluye todos los campos del modelo
