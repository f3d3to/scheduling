from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Planificador, Actividad, Tarea, EstructuraPlanificador,
    Estado, TipoPlanificador, Objetivo, RegistroProgreso
)
from .serializers import (
    PlanificadorSerializer,
    ActividadSerializer,
    TareaSerializer,
    EstructuraPlanificadorSerializer,
)
from .filters import (
    PlanificadorFilter,
    ActividadFilter,
    TareaFilter,
    EstructuraPlanificadorFilter,
)

from .serializers import (
    EstadoSerializer,
    TipoPlanificadorSerializer,
    ObjetivoSerializer,
    RegistroProgresoSerializer,
)
from .filters import (
    EstadoFilter,
    TipoPlanificadorFilter,
    ObjetivoFilter,
    RegistroProgresoFilter,
)

# Lista y creación de planificadores
class PlanificadorListCreateView(ListCreateAPIView):
    queryset = Planificador.objects.all()
    serializer_class = PlanificadorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlanificadorFilter

# Detalle, actualización y eliminación de un planificador
class PlanificadorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Planificador.objects.all()
    serializer_class = PlanificadorSerializer

# Lista y creación de estructuras de planificadores
class EstructuraPlanificadorListCreateView(ListCreateAPIView):
    queryset = EstructuraPlanificador.objects.all()
    serializer_class = EstructuraPlanificadorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstructuraPlanificadorFilter

# Detalle, actualización y eliminación de una estructura
class EstructuraPlanificadorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = EstructuraPlanificador.objects.all()
    serializer_class = EstructuraPlanificadorSerializer

# Lista y creación de actividades
class ActividadListCreateView(ListCreateAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ActividadFilter

# Detalle, actualización y eliminación de una actividad
class ActividadDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

# Lista y creación de tareas
class TareaListCreateView(ListCreateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TareaFilter

# Detalle, actualización y eliminación de una tarea
class TareaDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

# Lista y creación de estados
class EstadoListCreateView(ListCreateAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstadoFilter

# Detalle, actualización y eliminación de un estado
class EstadoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

# Lista y creación de tipos de planificador
class TipoPlanificadorListCreateView(ListCreateAPIView):
    queryset = TipoPlanificador.objects.all()
    serializer_class = TipoPlanificadorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TipoPlanificadorFilter

# Detalle, actualización y eliminación de un tipo de planificador
class TipoPlanificadorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TipoPlanificador.objects.all()
    serializer_class = TipoPlanificadorSerializer

# Lista y creación de objetivos
class ObjetivoListCreateView(ListCreateAPIView):
    queryset = Objetivo.objects.all()
    serializer_class = ObjetivoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ObjetivoFilter

# Detalle, actualización y eliminación de un objetivo
class ObjetivoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Objetivo.objects.all()
    serializer_class = ObjetivoSerializer

# Lista y creación de registros de progreso
class RegistroProgresoListCreateView(ListCreateAPIView):
    queryset = RegistroProgreso.objects.all()
    serializer_class = RegistroProgresoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegistroProgresoFilter

# Detalle, actualización y eliminación de un registro de progreso
class RegistroProgresoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = RegistroProgreso.objects.all()
    serializer_class = RegistroProgresoSerializer
