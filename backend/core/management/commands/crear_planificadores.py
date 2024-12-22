from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from planificadores.models import (
    Estado,
    TipoPlanificador,
    Planificador,
    EstructuraPlanificador,
    Actividad,
    Tarea,
    Objetivo,
    RegistroProgreso,
)

class Command(BaseCommand):
    help = 'Crea los datos iniciales para todos los modelos relacionados con Planificadores'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Crear estados iniciales
                estados_iniciales = [
                    {"nombre": "Pendiente", "descripcion": "Elemento pendiente", "color": "#FFA500", "orden": 1},
                    {"nombre": "En Progreso", "descripcion": "Elemento en progreso", "color": "#00FF00", "orden": 2},
                    {"nombre": "Completado", "descripcion": "Elemento completado", "color": "#0000FF", "orden": 3},
                ]
                for estado_data in estados_iniciales:
                    estado, created = Estado.objects.get_or_create(
                        nombre=estado_data["nombre"],
                        defaults={
                            "descripcion": estado_data["descripcion"],
                            "color": estado_data["color"],
                            "orden": estado_data["orden"],
                        },
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Estado "{estado.nombre}" creado correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Estado "{estado.nombre}" ya existe'))

                # Crear tipos de planificador
                tipos_iniciales = [
                    {"nombre": "Calendario", "descripcion": "Planificador tipo calendario"},
                    {"nombre": "Organizador de Tareas", "descripcion": "Planificador para tareas específicas"},
                ]
                for tipo_data in tipos_iniciales:
                    tipo, created = TipoPlanificador.objects.get_or_create(
                        nombre=tipo_data["nombre"],
                        defaults={"descripcion": tipo_data["descripcion"]},
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'TipoPlanificador "{tipo.nombre}" creado correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'TipoPlanificador "{tipo.nombre}" ya existe'))

                # Crear estructuras de planificador
                estructuras_iniciales = [
                    {"nombre": "Plan Semanal", "configuracion": {
                        "vista": "semanal",
                        "campos": ["Lo más importante", "h", "Citas | reuniones"],
                        "dias": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
                        "notas": True
                    }},
                    {"nombre": "Plan Mensual", "configuracion": {
                        "vista": "mensual",
                        "dias_por_semana": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
                        "semanas": 5,
                        "tareas": True
                    }},
                    {"nombre": "Control de Estudio", "configuracion": {
                        "vista": "control de estudio",
                        "temas": 25,
                        "columnas": ["Fecha inicio", "Fecha examen"]
                    }},
                ]
                for estructura_data in estructuras_iniciales:
                    estructura, created = EstructuraPlanificador.objects.get_or_create(
                        nombre=estructura_data["nombre"],
                        defaults={
                            "configuracion": estructura_data["configuracion"],
                            "descripcion": f"Estructura para {estructura_data['nombre']}",
                        },
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'EstructuraPlanificador "{estructura.nombre}" creada correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'EstructuraPlanificador "{estructura.nombre}" ya existe'))

                # Crear planificadores iniciales
                planificadores_iniciales = [
                    {"nombre": "Mi Plan Semanal", "tipo": "Calendario", "estructura": "Plan Semanal"},
                    {"nombre": "Mi Plan Mensual", "tipo": "Calendario", "estructura": "Plan Mensual"},
                    {"nombre": "Mi Control de Estudio", "tipo": "Organizador de Tareas", "estructura": "Control de Estudio"},
                ]
                for planificador_data in planificadores_iniciales:
                    tipo = TipoPlanificador.objects.get(nombre=planificador_data["tipo"])
                    estructura = EstructuraPlanificador.objects.get(nombre=planificador_data["estructura"])
                    planificador, created = Planificador.objects.get_or_create(
                        nombre=planificador_data["nombre"],
                        defaults={
                            "tipo": tipo,
                            "estructura": estructura,
                            "descripcion": f"Planificador para {planificador_data['nombre']}",
                        },
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Planificador "{planificador.nombre}" creado correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Planificador "{planificador.nombre}" ya existe'))

                # Crear actividades iniciales
                planificador_semanal = Planificador.objects.get(nombre="Mi Plan Semanal")
                actividades_iniciales = [
                    {"nombre": "Revisión de Proyecto", "descripcion": "Revisar avances de la semana", "estado": "Pendiente"},
                    {"nombre": "Clase de Inglés", "descripcion": "Repasar gramática", "estado": "En Progreso"},
                ]
                for actividad_data in actividades_iniciales:
                    estado = Estado.objects.get(nombre=actividad_data["estado"])
                    actividad, created = Actividad.objects.get_or_create(
                        nombre=actividad_data["nombre"],
                        defaults={
                            "descripcion": actividad_data["descripcion"],
                            "planificador": planificador_semanal,
                            "estado": estado,
                        },
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Actividad "{actividad.nombre}" creada correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Actividad "{actividad.nombre}" ya existe'))

                # Crear tareas para las actividades
                actividad = Actividad.objects.get(nombre="Revisión de Proyecto")
                tareas_iniciales = [
                    {"nombre": "Preparar informe", "descripcion": "Informe semanal sobre el progreso", "fecha_limite": None},
                    {"nombre": "Reunión con el equipo", "descripcion": "Coordinar tareas futuras", "fecha_limite": None},
                ]
                for tarea_data in tareas_iniciales:
                    estado = Estado.objects.get(nombre="Pendiente")
                    tarea, created = Tarea.objects.get_or_create(
                        nombre=tarea_data["nombre"],
                        defaults={
                            "descripcion": tarea_data["descripcion"],
                            "actividad": actividad,
                            "estado": estado,
                        },
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Tarea "{tarea.nombre}" creada correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Tarea "{tarea.nombre}" ya existe'))

                # Crear objetivos
                objetivos_iniciales = [
                    {"descripcion": "Terminar proyecto trimestral", "fecha_objetivo": "2024-12-31", "completado": False},
                ]
                for objetivo_data in objetivos_iniciales:
                    planificador = Planificador.objects.get(nombre="Mi Control de Estudio")
                    objetivo, created = Objetivo.objects.get_or_create(
                        descripcion=objetivo_data["descripcion"],
                        defaults={
                            "fecha_objetivo": objetivo_data["fecha_objetivo"],
                            "completado": objetivo_data["completado"],
                            "planificador": planificador,
                        },
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Objetivo "{objetivo.descripcion}" creado correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Objetivo "{objetivo.descripcion}" ya existe'))

                # Crear registro de progreso
                registros_iniciales = [
                    {"actividad": "Revisión de Proyecto", "porcentaje": 50},
                ]
                for registro_data in registros_iniciales:
                    actividad = Actividad.objects.get(nombre=registro_data["actividad"])
                    registro, created = RegistroProgreso.objects.get_or_create(
                        actividad=actividad,
                        defaults={
                            "porcentaje": registro_data["porcentaje"],
                        },
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'RegistroProgreso para "{registro.actividad}" creado correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'RegistroProgreso para "{registro.actividad}" ya existe'))

            self.stdout.write(self.style.SUCCESS('Todos los modelos iniciales creados correctamente'))
        except Exception as e:
            raise CommandError(f'Error al crear los datos iniciales: {e}')
