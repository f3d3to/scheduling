from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Planificador, Actividad, Tarea, EstructuraPlanificador
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
