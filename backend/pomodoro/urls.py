# pomodoro/urls.py
from django.urls import path
from .views import TareaViewSet, SesionViewSet

urlpatterns = [
    path('tareas/', TareaViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('tareas/<int:pk>/', TareaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('tareas/<int:pk>/completar_sesion/', TareaViewSet.as_view({'post': 'completar_sesion'})),
    path('sesiones/', SesionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sesiones/<int:pk>/', SesionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]