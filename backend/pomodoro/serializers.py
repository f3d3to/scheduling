from rest_framework import serializers
from .models import Tarea, Sesion

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = "__all__"

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = "__all__"
