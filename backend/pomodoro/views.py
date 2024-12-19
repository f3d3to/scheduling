# pomodoro/views.py
from rest_framework import viewsets
from .models import Tarea, Sesion
from .serializers import TareaSerializer, SesionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.prefetch_related('tareas_sesiones__sesion').all()
    serializer_class = TareaSerializer

    @action(detail=True, methods=['post'])
    def completar_sesion(self, request, pk=None):
        tarea = self.get_object()
        sesion_id = request.data.get('sesion_id')
        tarea_sesion = tarea.tareas_sesiones.filter(sesion_id=sesion_id).first()
        if tarea_sesion:
            tarea_sesion.esta_completada = True
            tarea_sesion.save()
            tarea.verificar_completitud()
            return Response({"estado": "sesión completada"})
        return Response({"error": "sesión no encontrada"}, status=400)

class SesionViewSet(viewsets.ModelViewSet):
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer