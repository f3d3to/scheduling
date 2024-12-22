from django.core.management.base import BaseCommand, CommandError
from pomodoro.models import Sesion, TareaTimer
from django.db import transaction

class Command(BaseCommand):
    help = 'Crea las sesiones y tareas iniciales necesarias para Pomodoro'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                sesiones_iniciales = [
                    {"nombre": "Estudio", "duracion_minutos": 60, "es_obligatoria": True},
                    {"nombre": "Descanso", "duracion_minutos": 5, "es_obligatoria": False},
                    {"nombre": "Descanso Largo", "duracion_minutos": 15, "es_obligatoria": False},
                ]
                for sesion_data in sesiones_iniciales:
                    sesion, created = Sesion.objects.get_or_create(
                        nombre=sesion_data["nombre"],
                        defaults={
                            "duracion_minutos": sesion_data["duracion_minutos"],
                            "es_obligatoria": sesion_data["es_obligatoria"],
                        },
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Sesión "{sesion.nombre}" creada correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Sesión "{sesion.nombre}" ya existe'))

                tareas_iniciales = [
                    {"nombre": "Leer", "cantidad_para_completar": 4},
                    {"nombre": "Resumir", "cantidad_para_completar": 3},
                    {"nombre": "Practicar", "cantidad_para_completar": 5},
                    {"nombre": "Hacer Exámenes", "cantidad_para_completar": 6},
                ]
                for tarea_data in tareas_iniciales:
                    tarea, created = TareaTimer.objects.get_or_create(
                        nombre=tarea_data["nombre"],
                        defaults={
                            "cantidad_para_completar": tarea_data["cantidad_para_completar"],
                            "cantidad_completadas": 0,
                            "esta_realizada": False,
                        },
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Tarea "{tarea.nombre}" creada correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Tarea "{tarea.nombre}" ya existe'))

            self.stdout.write(self.style.SUCCESS('Sesiones y tareas iniciales creadas correctamente'))
        except Exception as e:
            raise CommandError(f'Error al crear sesiones y tareas iniciales: {e}')
