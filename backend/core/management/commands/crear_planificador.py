from planificadores.models import (
    Planificador, EstructuraPlanificador, Celda, Elemento,
    EstructuraElemento, Actividad, Tarea, Estado
)
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Crea instancias iniciales para los modelos de planificadores si no existen'

    def handle(self, *args, **options):
        try:
            # Crear un estado genérico
            estado_pendiente, _ = Estado.objects.get_or_create(
                nombre="Hecho",
                descripcion="Tarea o actividad Hecha",
                color="#FF0000",
                orden=1
            )

            # Crear una estructura para el planificador
            estructura_planificador = EstructuraPlanificador.objects.create(
                nombre="Semanal",
                configuracion={"tipo": "calendario", "filas": 6, "columnas": 7}  # Ejemplo de 6 filas y 7 columnas
            )

            # Crear el planificador
            planificador = Planificador.objects.create(
                nombre="Planificador Semanal",
                tipo="calendario",
                estructura=estructura_planificador
            )

            # Crear celdas para el planificador, asignando posiciones dinámicas
            celdas = []
            filas = estructura_planificador.configuracion.get("filas", 6)
            columnas = estructura_planificador.configuracion.get("columnas", 7)

            for fila in range(filas):
                for columna in range(columnas):
                    # Crear cada celda con su posición en la cuadrícula
                    celda = Celda.objects.create(
                        planificador=planificador,
                        contenido=f"Celda {fila+1}-{columna+1}",
                        fila=fila,
                        columna=columna
                    )
                    celdas.append(celda)

            # Crear una estructura para los elementos
            estructura_elemento_actividad = EstructuraElemento.objects.create(
                nombre="Actividad",
                fecha_edicion="2024-12-26T12:00:00Z",
                html_visualizacion="<div>Actividad</div>"
            )

            estructura_elemento_tarea = EstructuraElemento.objects.create(
                nombre="Tarea",
                fecha_edicion="2024-12-26T12:30:00Z",
                html_visualizacion="<div>Tarea</div>"
            )

            # Crear actividades y tareas asociadas al planificador
            actividad_1 = Actividad.objects.create(
                planificador=planificador,
                nombre="Actividad de ejemplo",
                descripcion="Una actividad inicial",
                fecha_inicio="2024-12-25",
                fecha_fin="2024-12-30",
                estado=estado_pendiente
            )

            tarea_1 = Tarea.objects.create(
                actividad=actividad_1,
                nombre="Tarea de ejemplo",
                descripcion="Primera tarea de ejemplo",
                fecha_limite="2024-12-27",
                estado=estado_pendiente,
                esta_realizada=False
            )

            # Crear elementos para las celdas
            elemento_1 = Elemento.objects.create(
                nombre="Elemento para Actividad",
                celda=celdas[0],  # Asignamos el elemento a la primera celda
                estructura=None,  # Si no tiene una estructura específica
                descripcion="Elemento inicial asociado a actividad",
                content_type=ContentType.objects.get_for_model(actividad_1),  # Cambiado
                object_id=actividad_1.id
            )

            elemento_2 = Elemento.objects.create(
                nombre="Elemento para Tarea",
                celda=celdas[0],  # Asignamos el elemento a la primera celda
                estructura=None,  # Si no tiene una estructura específica
                descripcion="Elemento inicial asociado a tarea",
                content_type=ContentType.objects.get_for_model(tarea_1),  # Cambiado
                object_id=tarea_1.id
            )

            # Opcional: Agregar más elementos si es necesario
            elemento_3 = Elemento.objects.create(
                nombre="Elemento adicional",
                celda=celdas[1],  # Asignamos este elemento al día 2
                estructura=estructura_elemento_tarea,
                descripcion="Elemento adicional para el día 2",
                content_type=ContentType.objects.get_for_model(tarea_1),
                object_id=tarea_1.id
            )

            # Final: Mostrar planificador y relaciones
            print(f"Planificador creado: {planificador.nombre}")
            print(f"Estructura: {planificador.estructura.nombre}")
            print("Celdas y elementos creados:")
            for celda in celdas:
                print(f"  - Celda {celda.fila+1}-{celda.columna+1}: {celda.contenido}")
                for elemento in celda.elementos.all():
                    print(f"    * Elemento: {elemento.nombre} - {elemento.descripcion}")

        except Exception as e:
            raise CommandError(f'Error al crear planificador: {e}')
