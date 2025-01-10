from django.urls import path
from .views import NotaListCreateView, NotaRetrieveUpdateDestroyView

app_name = "notas"

urlpatterns = [
    path('notas/', NotaListCreateView.as_view(), name='nota-list-create'),
    path('notas/<int:pk>/', NotaRetrieveUpdateDestroyView.as_view(), name='nota-detail'),
]
