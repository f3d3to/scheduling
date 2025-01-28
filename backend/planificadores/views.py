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
from django.db import transaction
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
    DynamicSerializer

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        tabla = json.loads(estructura_planificador.tabla) if isinstance(estructura_planificador.tabla, str) else estructura_planificador.tabla
        clave = f"{celda.fila},{celda.columna}"

        if clave in tabla:
            tabla[clave]['contenido'] = contenido_nuevo
            estructura_planificador.tabla = json.dumps(tabla)
            estructura_planificador.save()

        return Response({"msg": "Contenido actualizado con éxito"}, status=200)

    def delete(self, request, planificador_id, celda_id):
        # Obtener la celda y asegurarse de que pertenece al planificador
        celda = get_object_or_404(Celda, id=celda_id, planificador_id=planificador_id)

        # Obtener la estructura asociada
        planificador = get_object_or_404(Planificador, id=planificador_id)
        estructura = planificador.estructura
        if not estructura:
            return Response(
                {"error": "La estructura del planificador no existe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Iniciar una transacción para asegurarse de que todo se actualiza correctamente
        with transaction.atomic():
            # Eliminar todos los elementos relacionados con la celda
            elementos_relacionados = celda.elementos.all()  # Usar el related_name "elementos"
            elementos_relacionados.delete()

            # Eliminar la celda
            celda.delete()

            # Actualizar la tabla en la estructura
            tabla = json.loads(estructura.tabla) if isinstance(estructura.tabla, str) else estructura.tabla
            coordenadas = f"{celda.fila},{celda.columna}"
            if coordenadas in tabla:
                del tabla[coordenadas]  # Eliminar la entrada de la celda eliminada
                estructura.tabla = tabla  # Asignar de nuevo el JSON actualizado
                estructura.save()  # Guardar los cambios en la estructura

        return Response(
            {"message": "Celda, sus elementos relacionados y la tabla de la estructura fueron actualizados correctamente."},
            status=status.HTTP_200_OK,
        )

class EstructuraPlanificadorUpdateAPIView(APIView):
    def post(self, request, pk):
        estructura = get_object_or_404(EstructuraPlanificador, pk=pk)
        planificador = estructura.planificador_set.first()
        tabla_celdas = request.data.get('tabla', {})

        if not planificador:
            return Response({'error': 'No se encontró un planificador asociado.'}, status=status.HTTP_400_BAD_REQUEST)

        nueva_tabla = {}

        # Procesar celdas primero
        if tabla_celdas:
            print("Procesando celdas:", tabla_celdas)

            with transaction.atomic():
                for coordenadas, datos_celda in tabla_celdas.items():
                    fila, columna = map(int, coordenadas.split(','))
                    celda_id = datos_celda.get('id')

                    if celda_id is None:
                        # Crear nueva celda
                        nueva_celda = Celda.objects.create(
                            planificador=planificador,
                            contenido=datos_celda.get('contenido', ''),
                            fila=fila,
                            columna=columna,
                        )
                        nueva_tabla[f"{fila},{columna}"] = {
                            'id': nueva_celda.id,
                            'contenido': nueva_celda.contenido,
                            'fila': nueva_celda.fila,
                            'columna': nueva_celda.columna,
                            'w': datos_celda.get('w', 1),
                            'h': datos_celda.get('h', 1),
                        }
                        print(f"Celda creada: {nueva_celda.id}")
                    else:
                        celda, created = Celda.objects.update_or_create(
                            id=celda_id,
                            defaults={
                                'planificador': planificador,
                                'contenido': datos_celda.get('contenido', ''),
                                'fila': fila,
                                'columna': columna,
                            }
                        )
                        nueva_tabla[f"{fila},{columna}"] = {
                            'id': celda.id,
                            'contenido': celda.contenido,
                            'fila': celda.fila,
                            'columna': celda.columna,
                            'w': datos_celda.get('w', 1),
                            'h': datos_celda.get('h', 1),
                        }
                        print(f"Celda actualizada: {celda_id}")

        estructura_serializer = EstructuraPlanificadorSerializer(
            estructura,
            data={
                **request.data,
                'tabla': nueva_tabla,
            },
            partial=True,
        )
        if estructura_serializer.is_valid():
            estructura_serializer.save()
        else:
            return Response(estructura_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Estructura del planificador y celdas actualizadas correctamente'}, status=status.HTTP_200_OK)


class ModeloAPIView(APIView):
    """
    Gestión de modelos dinámicos: listar modelos y sus instancias (GET) y crear una instancia nueva (POST).
    """
    def get(self, request, *args, **kwargs):
        """
        Devuelve todos los modelos permitidos y sus instancias.
        """
        print("Obteniendo información de los modelos permitidos...")
        modelos_a_incluir = [
            'materia',
            'tipoevaluacion',
            'evaluacion',
            'actividad',
            'comentario',
            'estado',
            'etiqueta',
            'evento',
            'eventoasociado',
            'mensaje',
            'objetivo',
            'recurrente',
            'registroprogreso',
            'tarea',
            'sesion',
            'tareatimer'
        ]
        allowed_models = ContentType.objects.filter(model__in=modelos_a_incluir)
        modelos = []
        for content_type in allowed_models:
            model = content_type.model_class()
            if not model:
                continue
            campos = [field.name for field in model._meta.fields]
            instancias = [{'id': obj.id, 'nombre': str(obj)} for obj in model.objects.all()]
            modelos.append({
                'nombre': content_type.name.title(),
                'model': content_type.model,
                'id': content_type.id,
                'campos': campos,
                'instancias': instancias,
            })
        return Response(modelos, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Crea una instancia de un modelo dinámicamente.
        """
        modelo = request.data.get('modelo')
        datos = request.data.get('datos')

        if not modelo or not datos:
            return Response({'error': 'Modelo y datos son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content_type = ContentType.objects.get(model=modelo)
            model = content_type.model_class()

            instancia = model.objects.create(**datos)
            return Response({'id': instancia.id, 'nombre': str(instancia)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AsociarElementoAPIView(APIView):
    """
    Asocia un elemento existente a una celda.
    """
    def post(self, request, planificador_id, celda_id):
        instancia_id = request.data.get('instancia_id')
        model = request.data.get('model')
        if not instancia_id:
            return Response({'error': 'Se requiere el ID de la instancia'}, status=status.HTTP_400_BAD_REQUEST)

        celda = get_object_or_404(Celda, id=celda_id, planificador_id=planificador_id)

        try:
            content_type = ContentType.objects.get(model=model)
            # Asegurarse de que el objeto exista para este tipo y ID
            model_class = content_type.model_class()
            objeto = model_class.objects.get(id=instancia_id)
            elemento = Elemento.objects.create(
                celda=celda,
                content_type=content_type,
                object_id=instancia_id,
                nombre=f'Elemento Celda {celda.id}({celda.fila},{celda.columna})',
            )
            return Response({'message': 'Elemento asociado correctamente', 'id': elemento.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ElementoDetailView(APIView):
    def get(self, request, content_type_id, object_id):
        try:
            model = ContentType.objects.get_for_id(content_type_id).model_class()
            instance = model.objects.get(id=object_id)

            # Crea una instancia del serializador dinámico
            DynamicSerializer.Meta.model = model
            serializer = DynamicSerializer(instance)

            return Response(serializer.data)
        except model.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
        except ContentType.DoesNotExist:
            return Response({"error": "ContentType not found"}, status=status.HTTP_404_NOT_FOUND)

