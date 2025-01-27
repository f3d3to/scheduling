# backend/evento_academico/views.py
from rest_framework import generics
from .models import (
    MetaAcademica, ProgresoMateria, RecordatorioPersonalizado,
    EventoAsociado, EventoAcademico, PlanificacionAcademica, ActividadPlanificada
)
from .serializers import (
    MetaAcademicaSerializer, ProgresoMateriaSerializer,
    RecordatorioPersonalizadoSerializer, EventoAsociadoSerializer,
    EventoAcademicoSerializer, PlanificacionAcademicaSerializer,
    ActividadPlanificadaSerializer
)

class MetaAcademicaListCreateView(generics.ListCreateAPIView):
    queryset = MetaAcademica.objects.all()
    serializer_class = MetaAcademicaSerializer

    def perform_create(self, serializer):
        serializer.save(estudiante=self.request.user)

class MetaAcademicaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MetaAcademica.objects.all()
    serializer_class = MetaAcademicaSerializer

class ProgresoMateriaListCreateView(generics.ListCreateAPIView):
    queryset = ProgresoMateria.objects.all()
    serializer_class = ProgresoMateriaSerializer

class ProgresoMateriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProgresoMateria.objects.all()
    serializer_class = ProgresoMateriaSerializer

class RecordatorioPersonalizadoListCreateView(generics.ListCreateAPIView):
    queryset = RecordatorioPersonalizado.objects.all()
    serializer_class = RecordatorioPersonalizadoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class RecordatorioPersonalizadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecordatorioPersonalizado.objects.all()
    serializer_class = RecordatorioPersonalizadoSerializer

class EventoAsociadoListCreateView(generics.ListCreateAPIView):
    queryset = EventoAsociado.objects.all()
    serializer_class = EventoAsociadoSerializer

class EventoAsociadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventoAsociado.objects.all()
    serializer_class = EventoAsociadoSerializer

class EventoAcademicoListCreateView(generics.ListCreateAPIView):
    queryset = EventoAcademico.objects.all()
    serializer_class = EventoAcademicoSerializer

class EventoAcademicoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventoAcademico.objects.all()
    serializer_class = EventoAcademicoSerializer

class PlanificacionAcademicaListCreateView(generics.ListCreateAPIView):
    queryset = PlanificacionAcademica.objects.all()
    serializer_class = PlanificacionAcademicaSerializer

    def perform_create(self, serializer):
        serializer.save(estudiante=self.request.user)

class PlanificacionAcademicaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlanificacionAcademica.objects.all()
    serializer_class = PlanificacionAcademicaSerializer

class ActividadPlanificadaListCreateView(generics.ListCreateAPIView):
    queryset = ActividadPlanificada.objects.all()
    serializer_class = ActividadPlanificadaSerializer

class ActividadPlanificadaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ActividadPlanificada.objects.all()
    serializer_class = ActividadPlanificadaSerializer