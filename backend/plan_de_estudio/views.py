# backend/core/views.py

from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import PlanDeEstudio, Materia
from .serializers import PlanDeEstudioSerializer, MateriaSerializer, PlanDeEstudioCiclosSerializer
from .filters import PlanDeEstudioFilter, MateriaFilter


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


from django.http import JsonResponse
from rest_framework.views import APIView
from .models import PlanDeEstudio, Materia

class PlanDeEstudioGraphView(APIView):
    def get(self, request, pk):
        # Obtener el plan de estudio por su ID
        try:
            plan = PlanDeEstudio.objects.prefetch_related('materias', 'materias__correlativas').get(pk=pk)
        except PlanDeEstudio.DoesNotExist:
            return JsonResponse({"error": "Plan de estudio no encontrado."}, status=404)

        # Organizar materias por año
        materias_por_anio = {}
        for materia in plan.materias.all():
            anio = materia.anio if materia.anio else "Sin Año"
            if anio not in materias_por_anio:
                materias_por_anio[anio] = []
            materias_por_anio[anio].append({
                "id": materia.codigo,
                "name": materia.nombre,
                "group": materia.ciclo or "Sin Ciclo"
            })

        # Crear enlaces basados en las correlativas
        links = []
        for materia in plan.materias.all():
            for correlativa in materia.correlativas.all():
                links.append({
                    "source": correlativa.codigo,
                    "target": materia.codigo,
                    "type": "correlativa"
                })

        # Crear estructura final
        data = {
            "plan": {
                "id": plan.id,
                "name": plan.nombre,
                "year": plan.año_creacion
            },
            "years": materias_por_anio,
            "links": links
        }

        return JsonResponse(data)
