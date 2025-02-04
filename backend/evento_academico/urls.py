from django.urls import path
from .views import *

app_name = "evento_academico"

urlpatterns = [
    # Recurrencias
    path('recurrencias/', RecurrenciaListCreateView.as_view(), name='recurrencia-list-create'),
    path('recurrencias/<int:pk>/', RecurrenciaDetailView.as_view(), name='recurrencia-detail'),

    # Tipos de Evento
    path('tipos-evento/', TipoEventoListCreateView.as_view(), name='tipo-evento-list-create'),
    path('tipos-evento/<int:pk>/', TipoEventoDetailView.as_view(), name='tipo-evento-detail'),
    # EventoCalendarioAcademico
    path('eventos-calendario/', EventoCalendarioAcademicoListCreateView.as_view(), name='evento-calendario-list-create'),
    path('eventos-calendario/<int:pk>/', EventoCalendarioAcademicoDetailView.as_view(), name='evento-calendario-detail'),

    path('categorias-disponibles/', CategoriasDisponiblesView.as_view(), name='categorias-disponibles'),
    path('elementos/<str:categoria>/', ElementosDeCategoriaView.as_view(), name='elementos-de-categoria'),

]