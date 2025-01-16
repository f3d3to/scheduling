import json
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

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
    planificador = serializers.PrimaryKeyRelatedField(queryset=Planificador.objects.all())
    class Meta:
        model = Celda
        fields = '__all__'

class ElementoSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = Elemento
        fields = ['id', 'nombre', 'celda', 'estructura', 'descripcion', 'content_type', 'object_id', 'content_object', 'color']

    def get_content_object(self, obj):
        return str(obj.content_object)

    def get_color(self, obj):
        if hasattr(obj.content_object, 'color'):
            return getattr(obj.content_object, 'color', None)
        return "#c7c7c7"

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
    estado =  EstadoSerializer(read_only=True)
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
        fields = ['id', 'nombre', 'usuario', 'color']

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

class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        return value

class EstructuraPlanificadorSerializer(serializers.ModelSerializer):
    tabla = serializers.JSONField()
    nombre = serializers.SerializerMethodField()

    class Meta:
        model= EstructuraPlanificador
        fields = '__all__'

    def get_nombre(self, obj):
        planificador = Planificador.objects.get(estructura=obj)
        return planificador.nombre

    def to_representation(self, instance):
        """ Modificar la representación de la instancia para el frontend. """
        ret = super().to_representation(instance)
        tabla = ret.get('tabla')
        if isinstance(tabla, str):
            try:
                # Intentar cargar la cadena JSON y asignar el objeto JSON resultante a 'tabla'
                ret['tabla'] = json.loads(tabla)
            except json.JSONDecodeError:
                # Si hay un error en la decodificación, dejar 'tabla' como está o manejarlo de otra manera
                ret['tabla'] = tabla
        return ret

    def update(self, instance, validated_data):
        tabla_completa = validated_data.get('tabla', {})
        if tabla_completa:
            with transaction.atomic():
                if isinstance(tabla_completa, str):
                    tabla_completa = json.loads(tabla_completa)

                # Iterar sobre cada celda proporcionada en la tabla completa.
                for coordenadas, datos_celda in tabla_completa.items():
                    fila_destino, columna_destino = map(int, coordenadas.split(','))
                    id_celda = datos_celda['id']

                    # Obtener la instancia de la celda actual por su ID.
                    celda = Celda.objects.filter(id=id_celda).first()
                    if celda:
                        # Verificar si las coordenadas han cambiado.
                        if celda.fila != fila_destino or celda.columna != columna_destino:
                            # Mover la celda a las nuevas coordenadas.
                            print(f"Celda movida de ({celda.fila}, {celda.columna}) a ({fila_destino}, {columna_destino})")
                            celda.mover(fila_destino, columna_destino)
                            print(f" a ({fila_destino}, {columna_destino})")
                        else:
                            # Agregar una declaración de registro para movimientos que no se realizan.
                            print(f"No se movió la celda de ({celda.fila}, {celda.columna}) ya que no cambió de posición.")
                instance.save()
        return super().update(instance, validated_data)

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
    estructura = EstructuraPlanificadorSerializer(read_only=True)

    class Meta:
        model = Planificador
        fields = ['id', 'nombre', 'tipo', 'estructura', 'celdas']

class DynamicSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        for field_name, field in self.fields.items():
            if isinstance(field, serializers.PrimaryKeyRelatedField) or isinstance(field, serializers.ManyRelatedField):
                field_value = getattr(instance, field_name)
                if field_value is None:
                    ret[field_name] = None
                elif isinstance(field, serializers.PrimaryKeyRelatedField):
                    # Para relaciones ForeignKey o OneToOne
                    ret[field_name] = str(field_value)
                else:
                    # Para relaciones ManyToMany o Reverse ForeignKey
                    ret[field_name] = [str(item) for item in field_value.all()]

        return ret

    class Meta:
        model = None  # Se asignará dinámicamente
        fields = '__all__'