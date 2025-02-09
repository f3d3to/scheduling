# backend/core/views.py

from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum, IntegerField, Value
from django.db.models.functions import Coalesce
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


class PlanDeEstudioList(generics.ListCreateAPIView):
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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, carrera_id):
        estudiante = request.user

        try:
            carrera = PlanDeEstudio.objects.get(id=carrera_id)
        except PlanDeEstudio.DoesNotExist:
            return Response({"error": "La carrera no existe o no estás asociado a ella."}, status=404)

        # Materias del estudiante en esta carrera
        materias = MateriaEstudiante.objects.filter(
            estudiante=estudiante,
            materia__plan_de_estudio=carrera
        ).select_related('materia')

        # --- Créditos ---
        # Solo materias con ciclo definido y que no sean optativas
        total_creditos = Materia.objects.filter(
            plan_de_estudio=carrera,
            ciclo__isnull=False,
            condicion__iexact='carrera'  # Excluir materias optativas (asumiendo que 'carrera' es lo opuesto a 'optativa')
        ).aggregate(
            total=Sum('creditos')
        )['total'] or 0

        creditos_aprobados = materias.filter(
            estado='promocionada',
            materia__ciclo__isnull=False,
            materia__condicion__iexact='carrera'  # Excluir materias optativas
        ).aggregate(
            total=Sum('materia__creditos')
        )['total'] or 0

        # --- Ciclos ---
        # Solo ciclos definidos (excluir materias sin ciclo y optativas)
        ciclos_plan = Materia.objects.filter(
            plan_de_estudio=carrera,
            ciclo__isnull=False,          # Excluir ciclos nulos
            ciclo__gt='',                 # Excluir cadenas vacías
            condicion__iexact='carrera'   # Excluir materias optativas
        ).values_list('ciclo', flat=True).distinct()
        ciclos_data = {}

        for ciclo in ciclos_plan:
            total_materias = Materia.objects.filter(plan_de_estudio=carrera, ciclo=ciclo, condicion__iexact='carrera').count()
            materias_promocionadas = materias.filter(materia__ciclo=ciclo, estado='promocionada', materia__condicion__iexact='carrera').count()
            ciclos_data[ciclo] = {
                'total_materias': total_materias,
                'materias_promocionadas': materias_promocionadas
            }

        ciclos_formateados = []
        for ciclo, data in ciclos_data.items():
            porcentaje = (data['materias_promocionadas'] / data['total_materias']) * 100 if data['total_materias'] > 0 else 0

            # Solo incluir ciclos con nombre válido y porcentaje >= 0
            if ciclo and porcentaje >= 0:  # Filtra ciclos vacíos/None
                ciclos_formateados.append({
                    'nombre': ciclo,
                    'creditos_obtenidos': materias.filter(materia__ciclo=ciclo, estado='promocionada', materia__condicion__iexact='carrera').aggregate(Sum('materia__creditos'))['materia__creditos__sum'] or 0,
                    'total_creditos': Materia.objects.filter(plan_de_estudio=carrera, ciclo=ciclo, condicion__iexact='carrera').aggregate(Sum('creditos'))['creditos__sum'] or 0,
                    'porcentaje': round(porcentaje, 2)
                })

        # Ordenar los ciclos: Básico → General → Avanzado → otros
        orden_ciclos = ['Básico', 'General', 'Avanzado']
        ciclos_formateados.sort(key=lambda x: (
            orden_ciclos.index(x['nombre'])
            if x['nombre'] in orden_ciclos
            else len(orden_ciclos)  # Coloca los demás ciclos al final
        ))

        # --- Promedio ---
        # Solo materias con ciclo definido y que no sean optativas
        materias_promedio = materias.filter(
            estado__in=['promocionada', 'pendiente'],
            materia__ciclo__isnull=False,
            materia__condicion__iexact='carrera'  # Excluir materias optativas
        )
        suma_notas = materias_promedio.aggregate(
            suma=Coalesce(Sum('nota_final'), Value(0), output_field=IntegerField())
        )['suma']
        count_materias = materias_promedio.count()
        promedio_valor = round(suma_notas / count_materias, 2) if count_materias > 0 else 0

        # Respuesta (mismo formato)
        data = {
            'creditos': {
                'obtenidos': creditos_aprobados,
                'total': total_creditos,
                'porcentaje': round((creditos_aprobados / total_creditos * 100), 2) if total_creditos > 0 else 0
            },
            'ciclos': ciclos_formateados,
            'promedio': {
                'valor': promedio_valor,
                'materias_cursadas': count_materias
            },
            'plan_actual': PlanDeEstudioSerializer(carrera).data,
            'ultima_actualizacion': timezone.now()
        }

        return Response(data)

class CrearPlanConMaterias(APIView):
    def post(self, request):
        # Validar y crear el plan de estudio
        plan_serializer = PlanDeEstudioSerializer(data=request.data)
        if not plan_serializer.is_valid():
            return Response(plan_serializer.errors, status=400)

        plan = plan_serializer.save()

        # Crear las materias asociadas al plan
        materias_data = request.data.get("materias", [])
        materias_serialized = []
        for materia in materias_data:
            materia["plan_de_estudio"] = plan.id
            materia_serializer = MateriaSerializer(data=materia)
            if not materia_serializer.is_valid():
                # Revertir la creación del plan si alguna materia falla
                plan.delete()
                return Response(materia_serializer.errors, status=400)
            materias_serialized.append(materia_serializer.save())

        # Respuesta final
        response_data = {
            "id": plan.id,
            "nombre": plan.nombre,
            "año_creacion": plan.año_creacion,
            "descripcion": plan.descripcion,
            "materias": MateriaSerializer(materias_serialized, many=True).data,
        }
        return Response(response_data, status=200)