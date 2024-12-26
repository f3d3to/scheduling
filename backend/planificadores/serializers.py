from rest_framework import serializers
from .models import (
    Estado, Planificador, Celda, Elemento, Mensaje, Actividad, Tarea,
    RegistroProgreso, Objetivo, Etiqueta, Comentario, Recurrente,
    Evento, EventoAsociado, EstructuraPlanificador, EstructuraElemento
)

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['id', 'nombre', 'descripcion', 'color', 'orden']

class PlanificadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planificador
        fields = ['id', 'nombre', 'tipo', 'estructura']

class CeldaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Celda
        fields = ['id', 'planificador', 'contenido']

class ElementoSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Elemento
        fields = ['id', 'nombre', 'celda', 'estructura', 'descripcion', 'content_type', 'object_id', 'content_object']

    def get_content_object(self, obj):
        # Devuelve una representación genérica del objeto relacionado
        return str(obj.content_object)

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = ['id', 'tipo', 'icono', 'color']

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'planificador', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'color', 'estado']

class TareaSerializer(serializers.ModelSerializer):
    actividad = ActividadSerializer(read_only=True)
    class Meta:
        model = Tarea
        fields = ['id', 'actividad', 'nombre', 'descripcion', 'fecha_limite', 'color', 'estado', 'esta_realizada', 'fecha_actualizacion']

class RegistroProgresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroProgreso
        fields = ['id', 'actividad', 'porcentaje', 'fecha_registro']

class ObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objetivo
        fields = ['id', 'descripcion', 'fecha_objetivo', 'completado']

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ['id', 'nombre', 'usuario']

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'usuario', 'contenido', 'fecha_creacion']

class RecurrenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurrente
        fields = ['id', 'frecuencia', 'proxima_fecha']

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['id', 'nombre', 'descripcion', 'fecha_hora', 'usuario']

class EventoAsociadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoAsociado
        fields = ['id', 'evento', 'content_type', 'object_id', 'content_object']


class EstructuraPlanificadorSerializer(serializers.ModelSerializer):
    class Meta:
        model= EstructuraPlanificador
        fields = '__all__'

class EstructuraElementoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstructuraElemento
        fields = ['id', 'nombre', 'fecha_edicion', 'html_visualizacion']

class ElementoDetalleSerializer(serializers.ModelSerializer):
    estructura = EstructuraElementoDetalleSerializer(read_only=True)
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Elemento
        fields = ['id', 'nombre', 'celda', 'estructura', 'descripcion', 'content_type', 'object_id', 'content_object']

class CeldaDetalleSerializer(serializers.ModelSerializer):
    elementos = ElementoSerializer(many=True, read_only=True)

    class Meta:
        model = Celda
        fields = ['id', 'planificador', 'contenido', 'elementos']

class EstructuraPlanificadorDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstructuraPlanificador
        fields = '__all__'

class PlanificadorDetalleSerializer(serializers.ModelSerializer):
    celdas = CeldaDetalleSerializer(many=True, read_only=True)
    estructura = EstructuraPlanificadorDetalleSerializer(read_only=True)

    class Meta:
        model = Planificador
        fields = ['id', 'nombre', 'tipo', 'estructura', 'celdas']
