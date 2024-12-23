from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sesion, TareaTimer
from .serializers import SesionSerializer, TareaTimerSerializer
from .filters import SesionFilter, TareaTimerFilter

class SesionListCreateView(ListCreateAPIView):
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SesionFilter

class SesionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer

class TareaTimerListCreateView(ListCreateAPIView):
    queryset = TareaTimer.objects.all()
    serializer_class = TareaTimerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TareaTimerFilter

class TareaTimerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = TareaTimer.objects.all()
    serializer_class = TareaTimerSerializer
