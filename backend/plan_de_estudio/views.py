# backend/core/views.py

from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, Case, When, IntegerField, DecimalField, Avg
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import serializers
from .models import PlanDeEstudio, Materia, MateriaEstudiante, Evaluacion
from .serializers import (
    PlanDeEstudioSerializer,
    MateriaSerializer,
    PlanDeEstudioCiclosSerializer,
    MateriaEstudianteSerializer,
    EvaluacionSerializer,
    GrafoSerializer
)
from .filters import PlanDeEstudioFilter, MateriaFilter, GrafoFilter


class PlanDeEstudioList(generics.ListAPIView):
    queryset = PlanDeEstudio.objects.all()
    serializer_class = PlanDeEstudioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlanDeEstudioFilter

class MateriaList(generics.ListAPIView):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MateriaFilter

class MateriaCorrelativasTreeView(APIView):
    def get(self, request, codigo):
        materia_base = get_object_or_404(Materia, codigo=codigo)
        visitados = set()
        niveles = []

        # Inicializa el primer nivel con la materia base
        nivel_actual = [materia_base]
        while nivel_actual:
            # Serializa el nivel actual
            nivel_serializado = MateriaSerializer(nivel_actual, many=True).data
            niveles.append(nivel_serializado)
            # Encuentra las materias dependientes (correlativas hacia adelante)
            siguiente_nivel = []
            for materia in nivel_actual:
                if materia.id not in visitados:
                    visitados.add(materia.id)
                    correlativas = materia.requerida_por.all()
                    siguiente_nivel.extend([m for m in correlativas if m.id not in visitados])
            nivel_actual = siguiente_nivel

        return Response(niveles)

class PlanDeEstudioCiclosView(generics.RetrieveAPIView):
    queryset = PlanDeEstudio.objects.prefetch_related('materias')
    serializer_class = PlanDeEstudioCiclosSerializer

class MateriasEstudiantesListCreateView(generics.ListCreateAPIView):
    serializer_class = MateriaEstudianteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Lista solo las materias asociadas al estudiante autenticado.
        """
        estudiante = self.request.user
        return MateriaEstudiante.objects.filter(estudiante=estudiante)

    def perform_create(self, serializer):
        estudiante = self.request.user
        materia_id = self.request.data.get('materia_id')

        # Verificar si ya existe una relación entre el estudiante y la materia
        if MateriaEstudiante.objects.filter(estudiante=estudiante, materia_id=materia_id).exists():
            raise serializers.ValidationError("El estudiante ya está asociado a esta materia.")

        # Si no existe, crear la relación
        serializer.save(estudiante=estudiante)


class MateriasEstudiantesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MateriaEstudianteSerializer

    def get_queryset(self):
        """
        Asegura que solo se acceda a las relaciones del estudiante autenticado.
        """
        estudiante = self.request.user
        return MateriaEstudiante.objects.filter(estudiante=estudiante)


class EvaluacionesListCreateView(generics.ListCreateAPIView):
    serializer_class = EvaluacionSerializer

    def get_queryset(self):
        """
        Lista todas las evaluaciones de las materias del estudiante autenticado.
        """
        estudiante = self.request.user
        return Evaluacion.objects.filter(materia_estudiante__estudiante=estudiante)

    def perform_create(self, serializer):
        """
        Asocia la evaluación a una relación `MateriaEstudiante` válida del estudiante autenticado.
        """
        estudiante = self.request.user
        materia_estudiante = MateriaEstudiante.objects.get(
            id=self.request.data['materia_estudiante'],
            estudiante=estudiante
        )
        serializer.save(materia_estudiante=materia_estudiante)

class EvaluacionesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EvaluacionSerializer

    def get_queryset(self):
        """
        Asegura que el estudiante solo pueda acceder a evaluaciones de sus materias.
        """
        estudiante = self.request.user
        return Evaluacion.objects.filter(materia_estudiante__estudiante=estudiante)

class DescargarPlanDeEstudioJSON(APIView):
    """
    Vista para descargar un PlanDeEstudio en formato JSON.
    """

    def exportar_a_json(self, plan):
        """
        Exporta el PlanDeEstudio y sus materias relacionadas a un string JSON
        usando DRF.
        """

        # Serializar las materias relacionadas al PlanDeEstudio
        materias = plan.materias.all()
        serializer = MateriaSerializer(materias, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return json_data.decode('utf-8')

    def get(self, request, pk):
        """
        Maneja la petición GET para descargar el JSON.
        """
        try:
            plan = PlanDeEstudio.objects.get(pk=pk)
        except PlanDeEstudio.DoesNotExist:
            return HttpResponse("Plan de estudio no encontrado.", status=404)

        json_data = self.exportar_a_json(plan)

        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="plan_de_estudio_{plan.id}.json"'
        return response


class GenerarGrafoView(generics.ListAPIView):
    serializer_class = GrafoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GrafoFilter

    def get_queryset(self):
        plan_de_estudio_id = self.request.query_params.get('plan_de_estudio__id')
        if plan_de_estudio_id:
            return Materia.objects.filter(plan_de_estudio__id=plan_de_estudio_id)
        return Materia.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({"nodos": [], "relaciones": []})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data[0])


class EstadoCarreraView(APIView):
    """Endpoint único para todos los datos del estado de la carrera"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        estudiante = request.user
        plan_activo = self._obtener_plan_activo(estudiante)

        # Optimización: Una sola query con prefetch
        materias = MateriaEstudiante.objects.filter(
            estudiante=estudiante
        ).select_related(
            'materia', 'materia__plan_de_estudio'
        ).prefetch_related('evaluaciones')

        # Cálculos en base de datos
        estadisticas = materias.aggregate(
            total_creditos=Sum('materia__creditos'),
            creditos_aprobados=Sum(
                Case(
                    When(estado='aprobada', then='materia__creditos'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            promedio=Avg(
                Case(
                    When(estado='aprobada', then='nota_final'),
                    default=None,
                    output_field=DecimalField()
                )
            )
        )

        # Agrupación por ciclo con Window functions
        ciclos = materias.values('materia__ciclo').annotate(
            total_creditos=Sum('materia__creditos'),
            obtenidos=Sum(
                Case(
                    When(estado='aprobada', then='materia__creditos'),
                    default=0
                )
            )
        )

        return Response({
            'estadisticas_generales': estadisticas,
            'desglose_ciclos': list(ciclos),
            'plan_actual': PlanDeEstudioSerializer(plan_activo).data,
            'ultima_actualizacion': timezone.now()
        })

    def _obtener_plan_activo(self, estudiante):
        # Lógica para determinar el plan activo del estudiante
        return PlanDeEstudio.objects.latest('año_creacion')