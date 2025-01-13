import importlib
import json
# Third Party
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Django
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.urls import URLPattern, URLResolver

# Proyecto
from .models import (
    Estado, Planificador, Celda, Elemento, Mensaje, Actividad, Tarea,
    RegistroProgreso, Objetivo, Etiqueta, Comentario, Recurrente, Evento,
    EventoAsociado, EstructuraPlanificador,
    EstructuraElemento,
)
from .serializers import (
    EstadoSerializer, PlanificadorSerializer, CeldaSerializer, ElementoSerializer,
    MensajeSerializer, ActividadSerializer, TareaSerializer, RegistroProgresoSerializer,
    ObjetivoSerializer, EtiquetaSerializer, ComentarioSerializer, RecurrenteSerializer,
    EventoSerializer, EventoAsociadoSerializer,
    EstructuraPlanificadorSerializer, EstructuraElementoDetalleSerializer,
    PlanificadorDetalleSerializer,
    FormularioCrearElementoSerializer, FormularioInfoSerializer,

)
from .filters import (
    EstadoFilter, PlanificadorFilter, CeldaFilter, ElementoFilter, MensajeFilter,
    ActividadFilter, TareaFilter, RegistroProgresoFilter, ObjetivoFilter, EtiquetaFilter,
    ComentarioFilter, RecurrenteFilter, EventoFilter, EventoAsociadoFilter,
    URLFilter,

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

class ModeloEstructuraListView(APIView):
    """
    Vista para listar las estructuras de modelos permitidos y sus campos.
    """

    def get(self, request, *args, **kwargs):
        # Lista de modelos permitidos en formato app_label.model_name
        MODELOS_PERMITIDOS = [
            "planificadores.tarea",
            "planificadores.actividad",
            "planificadores.objetivo",
            "planificadores.comentario",
            "planificadores.etiqueta",
            "planificadores.evento",
            "planificadores.registroprogreso",
            "planificadores.recurrente",
            # "planificadores.planificador",
            # "planificadores.estado",
        ]

        # Filtrar ContentType para incluir solo los modelos permitidos
        content_types = ContentType.objects.filter(
            app_label__in=[modelo.split(".")[0] for modelo in MODELOS_PERMITIDOS],
            model__in=[modelo.split(".")[1] for modelo in MODELOS_PERMITIDOS],
        )

        modelos = []
        for content_type in content_types:
            model_class = content_type.model_class()
            if model_class:
                campos = [
                    {
                        "name": field.name,
                        "type": field.get_internal_type(),
                        "required": not field.blank,
                        "verbose_name": field.verbose_name,
                    }
                    for field in model_class._meta.fields
                ]

                modelos.append({
                    "model_name": model_class._meta.verbose_name,
                    "app_label": model_class._meta.app_label,
                    "fields": campos,
                })

        return Response(modelos)


class SchemaListView(APIView):
    """
    Vista para listar las URLs del proyecto con soporte para filtros.
    """

    def get(self, request, *args, **kwargs):
        # Función interna para listar URLs
        def list_urls(urlpatterns, acc=None):
            if acc is None:
                acc = []
            if not urlpatterns:
                return
            pattern = urlpatterns[0]
            if isinstance(pattern, URLPattern):
                yield ''.join(acc + [str(pattern.pattern)])
            elif isinstance(pattern, URLResolver):
                yield from list_urls(pattern.url_patterns, acc + [str(pattern.pattern)])
            yield from list_urls(urlpatterns[1:], acc)

        # Importa el módulo de URLs principal
        urlconf = importlib.import_module(settings.ROOT_URLCONF)
        all_urls = list(list_urls(urlconf.urlpatterns))

        # Excluye URLs explícitamente
        excluded_urls = ["admin",]
        filtered_urls = [url for url in all_urls if not any(excluded in url for excluded in excluded_urls)]

        # Aplica el filtro para incluir URLs según patrón
        filterset = URLFilter(data=request.GET, queryset=filtered_urls)
        if filterset.is_valid():
            filtered_urls = filterset.qs()

        return Response({"urls": filtered_urls})


class FormularioCrearElementoView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FormularioCrearElementoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        elemento = serializer.save()

        # Serializar el elemento creado con el serializer de Elemento para incluir la info del objeto asociado
        elemento_data = {
            'id': elemento.id,
            'nombre': elemento.nombre,
            'celda': CeldaSerializer(elemento.celda).data,
            'estructura': EstructuraElementoDetalleSerializer(elemento.estructura).data if elemento.estructura else None,
            'descripcion': elemento.descripcion,
            'content_type': ContentType.objects.get_for_model(elemento.content_object).model if elemento.content_type else None,
            'object_id': elemento.object_id,
            'content_object': self.get_content_object_data(elemento)
        }

        return Response(elemento_data, status=status.HTTP_201_CREATED)

    def get_content_object_data(self, elemento):
        if elemento.content_object:
            serializer_class = {
                'actividad': ActividadSerializer,
                'tarea': TareaSerializer,
                'objetivo': ObjetivoSerializer,
                'comentario': ComentarioSerializer,
                'etiqueta': EtiquetaSerializer,
                'evento': EventoSerializer,
                'registro_progreso': RegistroProgresoSerializer,
                'recurrente': RecurrenteSerializer,
            }.get(elemento.content_type.model)

            if serializer_class:
                return serializer_class(elemento.content_object).data
        return None

class FormularioInfoView(APIView):
    def get(self, request, *args, **kwargs):
        # 1. Lista de modelos asociables
        modelos_asociables = [
            'actividad', 'tarea', 'objetivo', 'comentario', 'etiqueta',
            'evento', 'registroprogreso', 'recurrente'
        ]

        # 2. Estructura de modelos (similar a /estructura-modelos/)
        MODELOS_PERMITIDOS = [
            "planificadores.tarea",
            "planificadores.actividad",
            "planificadores.objetivo",
            "planificadores.comentario",
            "planificadores.etiqueta",
            "planificadores.evento",
            "planificadores.registroprogreso",
            "planificadores.recurrente",
            "planificadores.planificador",
            "planificadores.estado",
            # "users.usuario",
        ]

        # Filtrar ContentType para incluir solo los modelos permitidos
        content_types = ContentType.objects.filter(
            app_label__in=[modelo.split(".")[0] for modelo in MODELOS_PERMITIDOS],
            model__in=[modelo.split(".")[1] for modelo in MODELOS_PERMITIDOS],
        )

        estructura_modelos = []
        for content_type in content_types:
            model_class = content_type.model_class()
            if model_class:
                campos = [
                    {
                        "name": field.name,
                        "type": field.get_internal_type(),
                        "required": not field.blank,
                        "verbose_name": field.verbose_name,
                    }
                    for field in model_class._meta.fields
                ]

                estructura_modelos.append({
                    "model_name": model_class._meta.model_name,
                    "app_label": model_class._meta.app_label,
                    "fields": campos,
                })

        # 3. URLs de modelos (similar a /listado-urls/)
        urls_modelos = {
            'actividad': 'http://localhost:8000/actividades/',
            'tarea': 'http://localhost:8000/tareas/',
            'objetivo': 'http://localhost:8000/objetivos/',
            'comentario': 'http://localhost:8000/comentarios/',
            'etiqueta': 'http://localhost:8000/etiquetas/',
            'evento': 'http://localhost:8000/eventos/',
            'registroprogreso': 'http://localhost:8000/registro-progresos/',
            'recurrente': 'http://localhost:8000/recurrentes/',
            'estructura_elemento': 'http://localhost:8000/estructura-elementos/',
        }

        # 5. Estructuras de elementos disponibles
        estructuras = EstructuraElementoDetalleSerializer(EstructuraElemento.objects.all(), many=True).data

        # Serializar la respuesta
        serializer = FormularioInfoSerializer({
            'modelos_asociables': modelos_asociables,
            'estructura_modelos': estructura_modelos,
            'urls_modelos': urls_modelos,
            'estructuras': estructuras
        })

        return Response(serializer.data, status=status.HTTP_200_OK)

class CeldaContenidoUpdate(APIView):
    """
    Actualiza tanto la instancia de Celda como el JSONField en EstructuraPlanificador.
    """

    def patch(self, request, planificador_id, celda_id):
        planificador = get_object_or_404(Planificador, pk=planificador_id)
        estructura_planificador = planificador.estructura

        if not estructura_planificador:
            return Response({"error": "No se encontró la estructura del planificador"}, status=404)

        celda = get_object_or_404(Celda, pk=celda_id, planificador=planificador)
        contenido_nuevo = request.data.get('contenido')
        celda.contenido = contenido_nuevo
        celda.save()

        # Asegúrate de que estás trabajando con un diccionario
        tabla = json.loads(estructura_planificador.tabla) if isinstance(estructura_planificador.tabla, str) else estructura_planificador.tabla
        clave = f"{celda.fila},{celda.columna}"

        if clave in tabla:
            tabla[clave]['contenido'] = contenido_nuevo
            estructura_planificador.tabla = json.dumps(tabla)  # Vuelve a serializar el diccionario a string JSON para almacenarlo
            estructura_planificador.save()

        return Response({"msg": "Contenido actualizado con éxito"}, status=200)
