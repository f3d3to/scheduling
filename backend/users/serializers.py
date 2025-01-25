from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Usuario

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Campos personalizados
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Datos adicionales en la respuesta
        data['user'] = UsuarioSerializer(self.user).data
        return data

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'perfil')