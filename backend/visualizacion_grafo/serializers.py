from rest_framework import serializers
from .models import VisualizacionGrafo, NodoGrafo, EnlaceGrafo

class VisualizacionGrafoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisualizacionGrafo
        fields = '__all__'  # O especifica los campos que necesitas
        # Si tienes campos de solo lectura, puedes usar:
        # read_only_fields = ('campo1', 'campo2')

class NodoSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField()
    nombre_materia = serializers.CharField(source='materia.nombre')

    class Meta:
        model = NodoGrafo
        fields = ['id', 'pos_x', 'pos_y', 'config_visual', 'estado', 'nombre_materia']

    def get_estado(self, obj):
        user = self.context['request'].user
        return obj.materia.estado_estudiante(user)

class EnlaceSerializer(serializers.ModelSerializer):
    fuente_nombre = serializers.CharField(source='fuente.materia.nombre')
    destino_nombre = serializers.CharField(source='destino.materia.nombre')

    class Meta:
        model = EnlaceGrafo
        fields = ['id', 'config_visual', 'fuente_nombre', 'destino_nombre']