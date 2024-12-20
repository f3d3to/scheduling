from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tarea, Sesion
from .serializers import TareaSerializer, SesionSerializer
from .filters import TareaFilter, SesionFilter

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

# Lista y creación de sesiones
class SesionListCreateView(ListCreateAPIView):
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SesionFilter

# Detalle, actualización y eliminación de una sesión
class SesionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer
