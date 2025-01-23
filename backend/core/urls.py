# Third-party
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Django
from django.contrib import admin
from django.urls import path, include

# Project
from users.views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

app_name = "apps"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plan_de_estudio.urls')),
    path('', include('planificadores.urls')),
    path('', include('pomodoro.urls')),
    path('', include('users.urls')),
    path('', include('visualizacion_grafo.urls')),

    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(), name='redoc'),
]
