from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import (
    Estado, Planificador, Celda, Elemento, Mensaje, Actividad, Tarea,
    RegistroProgreso, Objetivo, Etiqueta, Comentario, Recurrente, Evento,
    EventoAsociado, EstructuraPlanificador
)
from .serializers import (
    EstadoSerializer, PlanificadorSerializer, CeldaSerializer, ElementoSerializer,
    MensajeSerializer, ActividadSerializer, TareaSerializer, RegistroProgresoSerializer,
    ObjetivoSerializer, EtiquetaSerializer, ComentarioSerializer, RecurrenteSerializer,
    EventoSerializer, EventoAsociadoSerializer, EstructuraPlanificadorSerializer,
    PlanificadorDetalleSerializer
)
from .filters import (
    EstadoFilter, PlanificadorFilter, CeldaFilter, ElementoFilter, MensajeFilter,
    ActividadFilter, TareaFilter, RegistroProgresoFilter, ObjetivoFilter, EtiquetaFilter,
    ComentarioFilter, RecurrenteFilter, EventoFilter, EventoAsociadoFilter,

)

# Estado
class EstadoListCreateView(ListCreateAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstadoFilter

class EstadoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

# Planificador
class PlanificadorListCreateView(ListCreateAPIView):
    queryset = Planificador.objects.all()
    serializer_class = PlanificadorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlanificadorFilter

class PlanificadorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Planificador.objects.all()
    serializer_class = PlanificadorSerializer

# Celda
class CeldaListCreateView(ListCreateAPIView):
    queryset = Celda.objects.all()
    serializer_class = CeldaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CeldaFilter

class CeldaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Celda.objects.all()
    serializer_class = CeldaSerializer

# Elemento
class ElementoListCreateView(ListCreateAPIView):
    queryset = Elemento.objects.all()
    serializer_class = ElementoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ElementoFilter

class ElementoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Elemento.objects.all()
    serializer_class = ElementoSerializer

# Mensaje
class MensajeListCreateView(ListCreateAPIView):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer

class MensajeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer

# Actividad
class ActividadListCreateView(ListCreateAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ActividadFilter

class ActividadRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

# Tarea
class TareaListCreateView(ListCreateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TareaFilter

class TareaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

# RegistroProgreso
class RegistroProgresoListCreateView(ListCreateAPIView):
    queryset = RegistroProgreso.objects.all()
    serializer_class = RegistroProgresoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegistroProgresoFilter

class RegistroProgresoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = RegistroProgreso.objects.all()
    serializer_class = RegistroProgresoSerializer

# Objetivo
class ObjetivoListCreateView(ListCreateAPIView):
    queryset = Objetivo.objects.all()
    serializer_class = ObjetivoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ObjetivoFilter

class ObjetivoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Objetivo.objects.all()
    serializer_class = ObjetivoSerializer

# Etiqueta
class EtiquetaListCreateView(ListCreateAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EtiquetaFilter

class EtiquetaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer

# Comentario
class ComentarioListCreateView(ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComentarioFilter

class ComentarioRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

# Recurrente
class RecurrenteListCreateView(ListCreateAPIView):
    queryset = Recurrente.objects.all()
    serializer_class = RecurrenteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecurrenteFilter

class RecurrenteRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Recurrente.objects.all()
    serializer_class = RecurrenteSerializer

# Evento
class EventoListCreateView(ListCreateAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventoFilter

class EventoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

# EventoAsociado
class EventoAsociadoListCreateView(ListCreateAPIView):
    queryset = EventoAsociado.objects.all()
    serializer_class = EventoAsociadoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventoAsociadoFilter

class EventoAsociadoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = EventoAsociado.objects.all()
    serializer_class = EventoAsociadoSerializer

# EstructuraPlanificador
class EstructuraPlanificadorListCreateView(ListCreateAPIView):
    queryset = EstructuraPlanificador.objects.all()
    serializer_class = EstructuraPlanificadorSerializer
    filter_backends = [DjangoFilterBackend]

class EstructuraPlanificadorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = EstructuraPlanificador.objects.all()
    serializer_class = EstructuraPlanificadorSerializer

class PlanificadorDetailView(APIView):
    """
    API View para obtener un planificador con todos sus detalles incluyendo celdas y elementos.
    """

    def get(self, request, pk, format=None):
        """
        Obtiene y devuelve el detalle de un planificador específico por su ID.
        """
        planificador = get_object_or_404(Planificador, pk=pk)
        serializer = PlanificadorDetalleSerializer(planificador)
        return Response(serializer.data)
