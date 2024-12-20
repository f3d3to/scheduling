"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include

app_name = "apps"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plan_de_estudio.urls')),
    path('', include('planificadores.urls')),
    path('', include('pomodoro.urls')),

]
