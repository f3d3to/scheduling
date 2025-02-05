import random
from django.core.management.base import BaseCommand, CommandError
import traceback
import json

# Proyecto
from planificadores.factories import (
    EstadoFactory, EstructuraPlanificadorFactory, PlanificadorFactory, CeldaFactory,
    ElementoFactory, ActividadFactory, TareaFactory,
    ObjetivoFactory,
)

from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Crea instancias iniciales para todos los modelos en planificadores/models.py usando factories'

    def handle(self, *args, **options):
        try:
            # Crear Estados
            estados_nombres = ["Pendiente", "En Progreso", "Completado"]
            estados = []
            for nombre in estados_nombres:
                estado = EstadoFactory(nombre=nombre)
                estados.append(estado)
                #self.stdout.write(self.style.SUCCESS(f'Estado creado: {estado.nombre}'))

            # Crear Estructuras de Planificador
            estructuras_nombres = [
                ("Semanal", {"tipo": "tabla", "filas": 7, "columnas": 1}),
                ("Mensual", {"tipo": "tabla", "filas": 5, "columnas": 7})
            ]

            estructuras = []
            for nombre, configuracion in estructuras_nombres:
                estructura = EstructuraPlanificadorFactory(
                    nombre=nombre,
                    configuracion=configuracion,
                    filas=configuracion.get("filas"),
                    columnas=configuracion.get("columnas"),
                    )
                estructuras.append(estructura)
                #self.stdout.write(self.style.SUCCESS(f'Estructura Planificador creada: {estructura.nombre}'))

            # Crear Planificadores asociados a las estructuras
            planificadores_data = [
                {"nombre": "Planificador Semanal", "tipo": "semanal", "estructura": estructuras[0]},
                {"nombre": "Planificador Mensual", "tipo": "mensual", "estructura": estructuras[1]}
            ]
            planificadores = []
            for data in planificadores_data:
                planificador = PlanificadorFactory(nombre=data["nombre"], tipo=data["tipo"], estructura=data["estructura"])
                planificadores.append(planificador)
                #self.stdout.write(self.style.SUCCESS(f'Planificador creado: {planificador.nombre}'))

            # Crear Celdas asociadas a Planificadores
            for planificador in planificadores:
                filas = planificador.estructura.configuracion["filas"]
                columnas = planificador.estructura.configuracion["columnas"]
                tabla = {}
                for i in range(1, filas + 1):
                    for j in range(1, columnas + 1):
                        celda = CeldaFactory(planificador=planificador, fila=i, columna=j, contenido=f"Celda {i},{j}")
                        tabla[f"{i},{j}"] = {
                            "id": celda.id,
                            "contenido": celda.contenido,
                            "w": 1,
                            "h": 2,
                        }
                planificador.estructura.tabla = json.dumps(tabla)
                planificador.estructura.save()

            # Verificar que todas las celdas estén asociadas correctamente
            for planificador in planificadores:
                if not planificador.celdas.exists():
                    self.stdout.write(self.style.ERROR(f'El Planificador {planificador.nombre} no tiene celdas asociadas.'))

            # Crear Actividades y asociarlas a los Planificadores
            actividades = []
            for planificador in planificadores:
                for i in range(3):
                    actividad = ActividadFactory(planificador=planificador, nombre=f"Actividad {i+1} del {planificador.nombre}")
                    actividades.append(actividad)
                    #self.stdout.write(self.style.SUCCESS(f'Actividad creada: {actividad.nombre}'))

            # Crear Tareas asociadas a Actividades
            tareas = []
            for actividad in actividades:
                for i in range(2):
                    tarea = TareaFactory(actividad=actividad, nombre=f"Tarea {i+1} de {actividad.nombre}")
                    tareas.append(tarea)
                    #self.stdout.write(self.style.SUCCESS(f'Tarea creada: {tarea.nombre}'))

            # Crear Elementos asociados a Celdas y Actividades
            for planificador in planificadores:
                for celda in planificador.celdas.all():
                    actividad = random.choice(actividades)
                    elemento = ElementoFactory(
                        celda=celda,
                        nombre=f"Elemento de {celda.contenido}",
                        content_type=ContentType.objects.get_for_model(actividad),
                        object_id=actividad.id
                    )
                    #self.stdout.write(self.style.SUCCESS(f'Elemento creado: {elemento.nombre}'))

            # Crear Objetivos y asociarlos a Tareas o Actividades
            objetivos = []
            for tarea in tareas:
              objetivo = ObjetivoFactory(
                  descripcion=f"Objetivo para {tarea.nombre}",
                  content_type=ContentType.objects.get_for_model(tarea),
                  object_id=tarea.id
              )
              objetivos.append(objetivo)
              #self.stdout.write(self.style.SUCCESS(f'Objetivo creado: {objetivo.id} para {tarea.nombre}'))

            for actividad in actividades:
              objetivo = ObjetivoFactory(
                  descripcion=f"Objetivo para {actividad.nombre}",
                  content_type=ContentType.objects.get_for_model(actividad),
                  object_id=actividad.id
              )
              objetivos.append(objetivo)
              #self.stdout.write(self.style.SUCCESS(f'Objetivo creado: {objetivo.id} para {actividad.nombre}'))

            # Asociar Elementos a Celdas
            for planificador in planificadores:
                for celda in planificador.celdas.all():
                    # Asociar una actividad
                    actividad = random.choice(actividades)
                    ElementoFactory(
                        celda=celda,
                        nombre=f"Actividad en {celda.contenido}",
                        content_type=ContentType.objects.get_for_model(actividad),
                        object_id=actividad.id,
                    )

                    # Asociar una tarea
                    tarea = random.choice(tareas)
                    ElementoFactory(
                        celda=celda,
                        nombre=f"Tarea en {celda.contenido}",
                        content_type=ContentType.objects.get_for_model(tarea),
                        object_id=tarea.id,
                    )

                    # Asociar un objetivo
                    objetivo = random.choice(objetivos)
                    elemento_objetivo = ElementoFactory(
                        celda=celda,
                        nombre=f"Objetivo en {celda.contenido}",
                        content_type=ContentType.objects.get_for_model(objetivo),
                        object_id=objetivo.id,
                    )
                    #self.stdout.write(self.style.SUCCESS(f"Elemento creado: {elemento_objetivo.nombre}"))

        except Exception as e:
            traceback.print_exc()
            raise CommandError(f'Error al crear instancias: {e}, {e.__dict__}')
