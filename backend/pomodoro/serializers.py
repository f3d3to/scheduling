from rest_framework import serializers
from .models import TareaTimer, Sesion
from planificadores.models import Tarea
from planificadores.serializers import TareaSerializer, TareaForTimeSerializer
from planificadores.models import Actividad

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = '__all__'

class TareaTimerSerializer(serializers.ModelSerializer):
    tarea = TareaSerializer()  # Utiliza el serializador de Tarea para detalles completos
    progress = serializers.SerializerMethodField()

    class Meta:
        model = TareaTimer
        fields = [
            'id',
            'tarea',  # Incluye los detalles de Tarea y Actividad anidados
            'cantidad_completadas',
            'cantidad_para_completar',
            'progress',
        ]

    def get_progress(self, obj):
        if obj.cantidad_para_completar == 0:
            return 0
        progress = round((obj.cantidad_completadas / obj.cantidad_para_completar) * 100)
        return min(max(progress, 0), 100)

    def update(self, instance, validated_data):
        tarea_data = validated_data.pop('tarea')
        tarea = instance.tarea

        instance.cantidad_completadas = validated_data.get('cantidad_completadas', instance.cantidad_completadas)
        instance.cantidad_para_completar = validated_data.get('cantidad_para_completar', instance.cantidad_para_completar)
        instance.save()

        Tarea.objects.filter(id=tarea.id).update(**tarea_data)

        return instance

class TareaTimerCreateSerializer(serializers.ModelSerializer):
    actividad_id = serializers.IntegerField(write_only=True) # Recibe solo el ID
    tarea = TareaForTimeSerializer()

    class Meta:
        model = TareaTimer
        fields = [
            'id',
            'cantidad_completadas',
            'cantidad_para_completar',
            'actividad_id',
            'tarea'
        ]

    def create(self, validated_data):
        tarea_data = validated_data.pop('tarea')
        actividad_id = validated_data.pop('actividad_id')

        # Obtener la instancia de Actividad
        actividad = Actividad.objects.get(pk=actividad_id)

        # Crear la tarea asociada
        tarea = Tarea.objects.create(**tarea_data)

        # Crear la instancia de TareaTimer
        tarea_timer = TareaTimer.objects.create(tarea=tarea, **validated_data)
        return tarea_timer