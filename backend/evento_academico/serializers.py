# backend/evento_academico/serializers.py
from rest_framework import serializers
from .models import (
    MetaAcademica, ProgresoMateria, RecordatorioPersonalizado,
    EventoAsociado, EventoAcademico, PlanificacionAcademica, ActividadPlanificada
)

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

class RecordatorioPersonalizadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordatorioPersonalizado
        fields = '__all__'
        read_only_fields = ('usuario',)

class EventoAsociadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoAsociado
        fields = '__all__'

class EventoAcademicoSerializer(serializers.ModelSerializer):
    duracion = serializers.SerializerMethodField()

    class Meta:
        model = EventoAcademico
        fields = '__all__'

    def get_duracion(self, obj):
        return obj.duracion()

class PlanificacionAcademicaSerializer(serializers.ModelSerializer):
    carga_horaria = serializers.SerializerMethodField()
    conflictos = serializers.SerializerMethodField()

    class Meta:
        model = PlanificacionAcademica
        fields = '__all__'
        read_only_fields = ('estudiante',)

    def get_carga_horaria(self, obj):
        return obj.calcular_carga_horaria()

    def get_conflictos(self, obj):
        return obj.detectar_conflictos()

class ActividadPlanificadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadPlanificada
        fields = '__all__'