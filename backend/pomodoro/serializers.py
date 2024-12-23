from rest_framework import serializers
from .models import TareaTimer, Sesion

from rest_framework import serializers
from .models import Sesion, TareaTimer

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = ['id', 'nombre', 'duracion_minutos', 'es_obligatoria', 'fecha_creacion']

class TareaTimerSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    class Meta:
        model = TareaTimer
        fields = [
            'id',
            'tarea',
            'cantidad_completadas',
            'cantidad_para_completar',
            'progress',  # Agrega el campo progress
        ]

    def get_progress(self, obj):
        if obj.cantidad_para_completar == 0:
            return 0
        progress = round((obj.cantidad_completadas / obj.cantidad_para_completar) * 100)
        return min(max(progress, 0), 100)