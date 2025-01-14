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

class FormularioCrearElementoSerializer(serializers.Serializer):
    # Datos para Elemento
    elemento_nombre = serializers.CharField(max_length=255)
    celda_id = serializers.IntegerField()
    estructura_id = serializers.IntegerField(required=False)
    descripcion = serializers.CharField(required=False, allow_blank=True)

    # Datos para el modelo asociado
    modelo_asociado = serializers.CharField()  # 'actividad', 'tarea', 'objetivo', etc.
    modelo_asociado_id = serializers.IntegerField(required=False) # Para asociar a uno existente
    # Campos para crear una nueva instancia del modelo asociado
    actividad_data = serializers.DictField(required=False)
    tarea_data = serializers.DictField(required=False)
    objetivo_data = serializers.DictField(required=False)
    comentario_data = serializers.DictField(required=False)
    etiqueta_data = serializers.DictField(required=False)
    evento_data = serializers.DictField(required=False)
    registro_progreso_data = serializers.DictField(required=False)
    recurrente_data = serializers.DictField(required=False)

    def validate(self, data):
        """
        Validar que se proporcionen los datos correctos para crear o asociar un modelo.
        """
        modelo_asociado = data.get('modelo_asociado')
        modelo_asociado_id = data.get('modelo_asociado_id')

        if modelo_asociado_id:
            if not modelo_asociado:
                raise serializers.ValidationError("Debe especificar el 'modelo_asociado' cuando se proporciona 'modelo_asociado_id'.")
        elif modelo_asociado:
            if not data.get(f"{modelo_asociado}_data"):
                raise serializers.ValidationError(f"Se requieren datos para crear un nuevo '{modelo_asociado}'.")

        return data

    @transaction.atomic
    def create(self, validated_data):
        celda_id = validated_data.pop('celda_id')
        estructura_id = validated_data.pop('estructura_id', None)
        elemento_nombre = validated_data.pop('elemento_nombre')
        descripcion = validated_data.pop('descripcion', None)
        modelo_asociado = validated_data.pop('modelo_asociado')
        modelo_asociado_id = validated_data.pop('modelo_asociado_id', None)

        # Obtener la celda
        celda = Celda.objects.get(pk=celda_id)

        # Crear o asociar el modelo relacionado
        if modelo_asociado_id:
            # Asociar a un modelo existente
            content_type = ContentType.objects.get(app_label='planificadores', model=modelo_asociado)
            try:
                content_object = content_type.get_object_for_this_type(pk=modelo_asociado_id)
            except content_type.model_class().DoesNotExist:
                raise serializers.ValidationError(f"No existe {modelo_asociado} con ID {modelo_asociado_id}")
            object_id = modelo_asociado_id
        else:
            # Crear un nuevo modelo
            data = validated_data.pop(f"{modelo_asociado}_data")
            serializer_class = {
                'actividad': ActividadSerializer,
                'tarea': TareaSerializer,
                'objetivo': ObjetivoSerializer,
                'comentario': ComentarioSerializer,
                'etiqueta': EtiquetaSerializer,
                'evento': EventoSerializer,
                'registro_progreso': RegistroProgresoSerializer,
                'recurrente': RecurrenteSerializer,
            }.get(modelo_asociado)

            if not serializer_class:
                raise serializers.ValidationError(f"Modelo desconocido: {modelo_asociado}")

            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            content_object = serializer.save()
            content_type = ContentType.objects.get_for_model(content_object)
            object_id = content_object.id

        # Crear el elemento
        elemento = Elemento.objects.create(
            nombre=elemento_nombre,
            celda=celda,
            estructura_id=estructura_id,
            descripcion=descripcion,
            content_type=content_type,
            object_id=object_id
        )

        return elemento


class FormularioInfoSerializer(serializers.Serializer):
    modelos_asociables = serializers.ListField(child=serializers.CharField())
    estructura_modelos = serializers.JSONField()
    urls_modelos = serializers.JSONField()
    estructuras = serializers.JSONField()