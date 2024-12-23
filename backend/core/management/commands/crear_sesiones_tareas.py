from django.core.management.base import BaseCommand, CommandError
from pomodoro.models import Sesion, TareaTimer
from planificadores.models import Tarea

class Command(BaseCommand):
    help = 'Crea instancias iniciales para los modelos de pomodoro/models.py si no existen'

    def handle(self, *args, **options):
        try:
            # Crear Sesiones
            sesiones = [
                {"nombre": "Estudio", "duracion_minutos": 25, "es_obligatoria": True},
                {"nombre": "Descanso Corto", "duracion_minutos": 5, "es_obligatoria": False},
                {"nombre": "Descanso Largo", "duracion_minutos": 15, "es_obligatoria": False},
            ]
            for sesion_data in sesiones:
                sesion, created = Sesion.objects.get_or_create(
                    nombre=sesion_data["nombre"],
                    defaults={
                        "duracion_minutos": sesion_data["duracion_minutos"],
                        "es_obligatoria": sesion_data["es_obligatoria"]
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'{"Creada" if created else "Ya existe"}: Sesión "{sesion.nombre}"'))

            # Crear Tareas Timer
            tareas = Tarea.objects.all()[:3]  # Selecciona hasta 3 tareas existentes como ejemplo
            for idx, tarea in enumerate(tareas, start=1):
                tarea_timer, created = TareaTimer.objects.get_or_create(
                    tarea=tarea,
                    defaults={
                        "cantidad_para_completar": 4,  # Ejemplo: 4 sesiones necesarias
                        "cantidad_completadas": idx  # Ejemplo: progreso diferente
                    }
                )
                if created:
                    # Asociar sesiones a la TareaTimer
                    tarea_timer.sesiones.add(*Sesion.objects.all())
                    self.stdout.write(self.style.SUCCESS(f'TareaTimer creada para la Tarea "{tarea.nombre}"'))
                else:
                    self.stdout.write(self.style.WARNING(f'TareaTimer ya existe para la Tarea "{tarea.nombre}"'))

        except Exception as e:
            raise CommandError(f'Error al crear instancias: {e}')
