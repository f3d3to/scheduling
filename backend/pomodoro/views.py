from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sesion, TareaTimer
from .serializers import SesionSerializer, TareaTimerSerializer, TareaTimerCreateSerializer
from .filters import SesionFilter, TareaTimerFilter
from rest_framework.response import Response

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


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TareaTimerCreateSerializer
        return TareaTimerSerializer


class TareaTimerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = TareaTimer.objects.all()
    serializer_class = TareaTimerSerializer
