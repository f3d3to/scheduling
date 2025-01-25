# Python
import random
# Django
from django.core.management.base import BaseCommand, CommandError

# Proyecto
from pomodoro.factories import SesionFactory, TareaTimerFactory
from users.factories import UsuarioFactory
from planificadores.factories import TareaFactory
from planificadores.models import Tarea

class Command(BaseCommand):
    help = 'Crea instancias iniciales para los modelos en pomodoro, users y plan_estudio usando factories'

    def handle(self, *args, **options):
        try:
            # Crear Usuarios usando factories
            for i in range(1, 3):
                username = f'user{i}'
                usuario = UsuarioFactory(username=username, password=username)
                usuario.set_password(username)
                usuario.save()
                self.stdout.write(self.style.SUCCESS(f'Usuario creado: {usuario.username} con contraseña {username}'))

            # Crear Sesiones usando factories
            for _ in range(5):
                sesion = SesionFactory()
                self.stdout.write(self.style.SUCCESS(f'Sesión creada: {sesion}'))

            # Crear TareaTimers usando factories con una Tarea seleccionada al azar
            tareas = list(Tarea.objects.all())
            for _ in range(3):
                tarea_seleccionada = random.choice(tareas)
                tarea_timer = TareaTimerFactory(tarea=tarea_seleccionada)
                self.stdout.write(self.style.SUCCESS(f'TareaTimer creada: {tarea_timer}'))

        except Exception as e:
            raise CommandError(f'Error al crear instancias: {e}')
