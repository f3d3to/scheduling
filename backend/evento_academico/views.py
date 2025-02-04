# backend/evento_academico/views.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from .models import (
    EventoCalendarioAcademico, Recurrencia, TipoEvento, TipoEventoAcademico
)
from .serializers import (
    EventoCalendarioAcademicoSerializer, RecurrenciaSerializer, TipoEventoSerializer, TipoEventoAcademicoSerializer
)
from core.pagination import NoLimitPagination

# Para Recurrencia
class RecurrenciaListCreateView(generics.ListCreateAPIView):
    """
    Lista todas las recurrencias o crea una nueva
    """
    queryset = Recurrencia.objects.all()
    serializer_class = RecurrenciaSerializer

class RecurrenciaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina una recurrencia por ID
    """
    queryset = Recurrencia.objects.all()
    serializer_class = RecurrenciaSerializer

# Para TipoEventoAcademico
class TipoEventoAcademicoListCreateView(generics.ListCreateAPIView):
    """
    Lista todos los tipos de evento o crea uno nuevo
    """
    queryset = TipoEventoAcademico.objects.all()
    serializer_class = TipoEventoAcademicoSerializer

class TipoEventoAcademicoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina un tipo de evento por ID
    """
    queryset = TipoEventoAcademico.objects.all()
    serializer_class = TipoEventoAcademicoSerializer


class TipoEventoListCreateView(generics.ListCreateAPIView):
    """
    Lista todos los tipos de evento o crea uno nuevo
    """
    queryset = TipoEvento.objects.all()
    serializer_class = TipoEventoSerializer

class TipoEventoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina un tipo de evento por ID
    """
    queryset = TipoEvento.objects.all()
    serializer_class = TipoEventoSerializer

# Vistas para EventoCalendarioAcademico
class EventoCalendarioAcademicoListCreateView(generics.ListCreateAPIView):
    queryset = EventoCalendarioAcademico.objects.all()
    serializer_class = EventoCalendarioAcademicoSerializer
    pagination_class = NoLimitPagination

class EventoCalendarioAcademicoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventoCalendarioAcademico.objects.all()
    serializer_class = EventoCalendarioAcademicoSerializer
    pagination_class = NoLimitPagination


# Lista blanca de modelos permitidos
MODELOS_PERMITIDOS = {
    'eventoacademico': 'Evento Académico',
    'actividad': 'Actividad',
    'tarea': 'Tarea',
    'actividadplanificada':'Actividad Planificada',
    'metaacademica':'Objetivo Académico',
    'planificacionacademica': 'Planificación Académica',
    'recordatorio': 'Recordatorio',
    'objetivos':'Objetivos'

}

class CategoriasDisponiblesView(APIView):
    """
    Devuelve una lista de categorías disponibles para asociar con EventoCalendarioAcademico.
    """
    def get(self, request):
        categorias = [
            {'categoria': key, 'nombre': value}
            for key, value in MODELOS_PERMITIDOS.items()
        ]
        return Response(categorias)


class ElementosDeCategoriaView(APIView):
    """
    Devuelve una lista de elementos de una categoría específica.
    """
    def get(self, request, categoria):
        if categoria not in MODELOS_PERMITIDOS:
            return Response({"error": "Categoría no válida."}, status=400)

        try:
            # Obtener el modelo por su nombre
            content_type = ContentType.objects.get(model=categoria)
            model_class = content_type.model_class()

            # Filtrar instancias según el usuario autenticado (si aplica)
            queryset = model_class.objects.all()
            if hasattr(model_class, 'usuario'):  # Ajusta según tu modelo
                queryset = queryset.filter(usuario=request.user)

            # Serializar las instancias
            elementos = [
                {'id': elemento.id, 'nombre': str(elemento)}
                for elemento in queryset
            ]
            return Response(elementos)
        except ContentType.DoesNotExist:
            return Response({"error": "Categoría no encontrada."}, status=404)