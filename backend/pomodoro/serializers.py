# pomodoro/serializers.py
from rest_framework import serializers
from .models import Tarea, Sesion, TareaSesion

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = ['id', 'nombre', 'duracion_minutos', 'cuenta_para_completar', 'creada_en']

class TareaSesionSerializer(serializers.ModelSerializer):
    sesion = SesionSerializer()

    class Meta:
        model = TareaSesion
        fields = ['id', 'sesion', 'esta_completada']

class TareaSerializer(serializers.ModelSerializer):
    tareas_sesiones = TareaSesionSerializer(many=True, read_only=True)

    class Meta:
        model = Tarea
        fields = ['id', 'nombre', 'esta_completada', 'tareas_sesiones', 'actualizada_en']
