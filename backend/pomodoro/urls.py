from django.urls import path
from .views import TareaListCreateView, TareaDetailView, SesionListCreateView, SesionDetailView

urlpatterns = [
    path('tareas/', TareaListCreateView.as_view(), name='tarea-list-create'),
    path('tareas/<int:pk>/', TareaDetailView.as_view(), name='tarea-detail'),
    path('sesiones/', SesionListCreateView.as_view(), name='sesion-list-create'),
    path('sesiones/<int:pk>/', SesionDetailView.as_view(), name='sesion-detail'),
]