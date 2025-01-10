from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Nota
from .serializers import NotaSerializer

class NotaListCreateView(ListCreateAPIView):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

class NotaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
