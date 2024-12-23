# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Extiende el modelo de usuario de Django para agregar campos adicionales.
    """
    perfil = models.TextField(blank=True, null=True, help_text="Descripción del perfil del usuario.")

    def __str__(self):
        return self.username
