# backend/evento_academico/serializers.py
from rest_framework import serializers
from .models import (
    MetaAcademica, ProgresoMateria, Recordatorio,
    EventoAcademico, PlanificacionAcademica, ActividadPlanificada,
    EventoCalendarioAcademico, Recurrencia,
    TipoEventoAcademico,
    TipoEvento
)
from django.contrib.contenttypes.models import ContentType

class MetaAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaAcademica
        fields = '__all__'
        read_only_fields = ('estudiante',)

class ProgresoMateriaSerializer(serializers.ModelSerializer):
    porcentaje_completado = serializers.SerializerMethodField()

    class Meta:
        model = ProgresoMateria
        fields = '__all__'
        read_only_fields = ('materia_estudiante', 'ultima_actualizacion')

    def get_porcentaje_completado(self, obj):
        return obj.porcentaje_completado()

class RecordatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recordatorio
        fields = '__all__'
        read_only_fields = ('usuario',)

class EventoAcademicoSerializer(serializers.ModelSerializer):
    duracion = serializers.SerializerMethodField()

    class Meta:
        model = EventoAcademico
        fields = '__all__'

    def get_duracion(self, obj):
        return obj.duracion()

class PlanificacionAcademicaSerializer(serializers.ModelSerializer):
    # carga_horaria = serializers.SerializerMethodField()
    # conflictos = serializers.SerializerMethodField()

    class Meta:
        model = PlanificacionAcademica
        fields = '__all__'
        read_only_fields = ('estudiante',)

    # def get_carga_horaria(self, obj):
    #     return obj.calcular_carga_horaria()

    # def get_conflictos(self, obj):
    #     return obj.detectar_conflictos()

class ActividadPlanificadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadPlanificada
        fields = '__all__'

class RecurrenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurrencia
        fields = '__all__'


class TipoEventoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEventoAcademico
        fields = ['id', 'nombre', 'descripcion']

class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEvento
        fields = ['id', 'nombre', 'descripcion']

from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import EventoCalendarioAcademico, TipoEvento, Recurrencia

class EventoCalendarioAcademicoSerializer(serializers.ModelSerializer):
    # Serialización de la relación genérica
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model'
    )
    # Serialización de las relaciones ForeignKey
    tipo = serializers.PrimaryKeyRelatedField(
        queryset=TipoEvento.objects.all()
    )
    recurrencia = serializers.PrimaryKeyRelatedField(
        queryset=Recurrencia.objects.all(),
        allow_null=True,
        required=False
    )
    # Campo personalizado para mapear el contenido del objeto relacionado
    extendedProps = serializers.SerializerMethodField()
    # Campo rrule generado dinámicamente
    rrule = serializers.SerializerMethodField()

    class Meta:
        model = EventoCalendarioAcademico
        fields = [
            'id',
            'titulo',
            'descripcion',
            'inicio',
            'fin',
            'todo_el_dia',
            'color',
            'background_color',
            'border_color',
            'text_color',
            'url',
            'tipo',
            'recurrencia',
            'content_type',
            'object_id',
            'display',
            'editable',
            'start_editable',
            'duration_editable',
            'resource_editable',
            'rrule',
            'exdate',
            'class_names',
            'extendedProps',
        ]

    def get_rrule(self, obj):
        """
        Genera el valor de rrule basado en el campo recurrencia.
        """
        if not obj.recurrencia:
            return None

        # Mapear frecuencia a RFC 5545
        frecuencia_map = {
            'diaria': 'DAILY',
            'semanal': 'WEEKLY',
            'mensual': 'MONTHLY',
            'anual': 'YEARLY',
        }
        frecuencia_rfc = frecuencia_map.get(obj.recurrencia.frecuencia)

        # Construir la regla de recurrencia
        rrule_parts = [f"FREQ={frecuencia_rfc}", f"INTERVAL={obj.recurrencia.intervalo}"]

        # Agregar fecha de finalización si existe
        if obj.recurrencia.fin_recurrencia:
            rrule_parts.append(f"UNTIL={obj.recurrencia.fin_recurrencia.strftime('%Y%m%dT%H%M%SZ')}")
        print(";".join(rrule_parts))
        return ";".join(rrule_parts)

    def get_extendedProps(self, obj):
        """
        Serializa el contenido del objeto relacionado (content_object)
        solo en las solicitudes GET.
        """
        if obj.content_object:
            # Serializa el objeto relacionado como un diccionario
            return {
                'content_object': str(obj.content_object),
                'content_type': obj.content_type.model,
                'object_id': obj.object_id,
            }
        return None