from django.urls import path
from .views import TareaTimerListCreateView, TareaTimerRetrieveUpdateDestroyView, SesionListCreateView, SesionRetrieveUpdateDestroyView

app_name = "pomodoro"

urlpatterns = [
    path('tareasTimer/', TareaTimerListCreateView.as_view(), name='tarea-list-create'),
    path('tareasTimer/<int:pk>/', TareaTimerRetrieveUpdateDestroyView.as_view(), name='tarea-detail'),
    path('sesiones/', SesionListCreateView.as_view(), name='sesion-list-create'),
    path('sesiones/<int:pk>/', SesionRetrieveUpdateDestroyView.as_view(), name='sesion-detail'),
]