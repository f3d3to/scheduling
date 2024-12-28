import random
import decimal
# Django
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType

# Proyecto
from planificadores.models import (
    Estado, Planificador, Celda, Elemento, Mensaje, Actividad, Tarea,
    RegistroProgreso, Objetivo, Etiqueta, Comentario, Recurrente, Evento, EventoAsociado, EstructuraPlanificador, EstructuraElemento
)
from users.models import Usuario  # Asegúrate de tener la ruta correcta al modelo Usuario

class Command(BaseCommand):
    help = 'Crea instancias iniciales para todos los modelos en planificadores/models.py y las asocia con elementos y usuarios'

    def handle(self, *args, **options):
        try:
            # Crear Estados
            estados = [
                {"nombre": "Pendiente", "descripcion": "Estado inicial", "color": "#FFA500", "orden": 1},
                {"nombre": "En Progreso", "descripcion": "Tarea en curso", "color": "#0000FF", "orden": 2},
                {"nombre": "Completado", "descripcion": "Tarea finalizada", "color": "#008000", "orden": 3},
            ]
            for estado_data in estados:
                estado, created = Estado.objects.get_or_create(
                    nombre=estado_data["nombre"],
                    defaults=estado_data
                )
                self.stdout.write(self.style.SUCCESS(f'{"Creado" if created else "Ya existe"}: Estado "{estado.nombre}"'))

            # Crear Estructuras de Planificador
            estructuras_planificador = [
                {"nombre": "Semanal", "configuracion": {"tipo": "tabla", "filas": 7, "columnas": 1}},
                {"nombre": "Mensual", "configuracion": {"tipo": "tabla", "filas": 5, "columnas": 7}},
            ]
            for estructura_data in estructuras_planificador:
                estructura, created = EstructuraPlanificador.objects.get_or_create(
                    nombre=estructura_data["nombre"],
                    defaults=estructura_data
                )
                self.stdout.write(self.style.SUCCESS(f'{"Creada" if created else "Ya existe"}: Estructura Planificador "{estructura.nombre}"'))

            # Crear Planificadores
            planificadores = [
                {"nombre": "Planificador Semanal", "tipo": "semanal", "estructura": EstructuraPlanificador.objects.get(nombre="Semanal")},
                {"nombre": "Planificador Mensual", "tipo": "mensual", "estructura": EstructuraPlanificador.objects.get(nombre="Mensual")},
            ]
            for planificador_data in planificadores:
                planificador, created = Planificador.objects.get_or_create(
                    nombre=planificador_data["nombre"],
                    defaults=planificador_data
                )
                self.stdout.write(self.style.SUCCESS(f'{"Creado" if created else "Ya existe"}: Planificador "{planificador.nombre}"'))

            # Crear Celdas con posiciones (fila, columna)
            for planificador in Planificador.objects.all():
                configuracion = planificador.estructura.configuracion
                filas = configuracion.get('filas', 6)
                columnas = configuracion.get('columnas', 7)
                for fila in range(filas):
                    for columna in range(columnas):
                        celda, created = Celda.objects.get_or_create(
                            planificador=planificador,
                            fila=fila,
                            columna=columna,
                            contenido=f"Día {fila * columnas + columna + 1}"
                        )
                        self.stdout.write(self.style.SUCCESS(f'{"Creada" if created else "Ya existe"}: Celda "{celda.contenido}" para Planificador "{planificador.nombre}"'))

            # Crear Elementos y asociarlos con diferentes modelos (Actividad, Tarea, Objetivo, etc.)
            for celda in Celda.objects.all():
                # Crear Actividad y Elemento asociado
                actividad = Actividad.objects.create(
                    planificador=Planificador.objects.first(),
                    nombre="Actividad de ejemplo",
                    descripcion="Descripción de la actividad",
                    fecha_inicio="2024-01-01",
                    fecha_fin="2024-01-07",
                    color="#FF5733"
                )
                elemento_actividad = Elemento.objects.create(
                    nombre="Elemento para Actividad",
                    celda=celda,
                    descripcion="Elemento inicial asociado a actividad",
                    content_type=ContentType.objects.get_for_model(Actividad),
                    object_id=actividad.id
                )
                self.stdout.write(self.style.SUCCESS(f'Elemento asociado a Actividad: {elemento_actividad.nombre}'))

                # Crear Tarea y Elemento asociado
                tarea = Tarea.objects.create(
                    actividad=actividad,
                    nombre="Tarea de ejemplo",
                    descripcion="Descripción de la tarea",
                    fecha_limite="2024-01-07",
                    color="#FF0000",
                    esta_realizada=False
                )
                elemento_tarea = Elemento.objects.create(
                    nombre="Elemento para Tarea",
                    celda=celda,
                    descripcion="Elemento inicial asociado a tarea",
                    content_type=ContentType.objects.get_for_model(Tarea),
                    object_id=tarea.id
                )
                self.stdout.write(self.style.SUCCESS(f'Elemento asociado a Tarea: {elemento_tarea.nombre}'))

                # Crear RegistroProgreso
                registro_progreso = RegistroProgreso.objects.create(
                    actividad=actividad,
                    porcentaje= float(decimal.Decimal(random.randrange(1, 100))/100),
                    fecha_registro=timezone.now(),
                )
                self.stdout.write(self.style.SUCCESS(f'Registro de progreso asociado a la actividad: {registro_progreso.actividad}'))

                # Crear Objetivo y Elemento asociado
                objetivo = Objetivo.objects.create(
                    descripcion="Objetivo de ejemplo",
                    fecha_objetivo="2024-01-01",
                    completado=False,
                    content_type=ContentType.objects.get_for_model(Tarea),
                    object_id=tarea.id
                )
                elemento_objetivo = Elemento.objects.create(
                    nombre="Elemento para Objetivo",
                    celda=celda,
                    descripcion="Elemento inicial asociado a objetivo",
                    content_type=ContentType.objects.get_for_model(Objetivo),
                    object_id=objetivo.id
                )
                self.stdout.write(self.style.SUCCESS(f'Elemento asociado a Objetivo: {elemento_objetivo.nombre}'))

                # Crear Recurrente y Elemento asociado
                recurrente = Recurrente.objects.create(
                    frecuencia="Diaria",
                    proxima_fecha="2024-01-02"
                )
                elemento_recurrente = Elemento.objects.create(
                    nombre="Elemento para Recurrente",
                    celda=celda,
                    descripcion="Elemento inicial asociado a recurrente",
                    content_type=ContentType.objects.get_for_model(Recurrente),
                    object_id=recurrente.id
                )
                self.stdout.write(self.style.SUCCESS(f'Elemento asociado a Recurrente: {elemento_recurrente.nombre}'))

            # Asociar usuarios existentes a Etiquetas y Eventos
            usuario = Usuario.objects.first()  # Asumiendo que quieres usar el primer usuario disponible
            etiquetas = [
                {"nombre": "Trabajo", "usuario": usuario},
                {"nombre": "Personal", "usuario": usuario}
            ]
            for etiqueta_data in etiquetas:
                etiqueta, created = Etiqueta.objects.get_or_create(
                    nombre=etiqueta_data["nombre"],
                    defaults={"usuario": etiqueta_data["usuario"]}
                )
                self.stdout.write(self.style.SUCCESS(f'{"Creada" if created else "Ya existe"}: Etiqueta "{etiqueta.nombre}"'))

            eventos = [
                {"nombre": "Reunión Inicial", "descripcion": "Reunión de ejemplo", "fecha_hora": "2024-01-01T10:00:00Z", "usuario": usuario}
            ]
            for evento_data in eventos:
                evento, created = Evento.objects.get_or_create(
                    nombre=evento_data["nombre"],
                    defaults=evento_data
                )
                self.stdout.write(self.style.SUCCESS(f'{"Creado" if created else "Ya existe"}: Evento "{evento.nombre}"'))

            mensajes = [
                {"tipo": "Recordatorio", "icono": "🔔", "color": "#FFD700"},
                {"tipo": "Alerta", "icono": "⚠️", "color": "#FF4500"},
                {"tipo": "Información", "icono": "ℹ️", "color": "#1E90FF"}
            ]
            for mensaje_data in mensajes:
                mensaje, created = Mensaje.objects.get_or_create(
                    tipo=mensaje_data["tipo"],
                    defaults={"icono": mensaje_data["icono"], "color": mensaje_data["color"]}
                )
                self.stdout.write(self.style.SUCCESS(f'{"Creado" if created else "Ya existe"}: Mensaje de tipo "{mensaje.tipo}"'))

            # Crear Comentarios
            usuario = Usuario.objects.first()  # Asumiendo que al menos un usuario existe
            comentarios = [
                {"usuario": usuario, "contenido": "Este es un comentario de prueba en el sistema."},
                {"usuario": usuario, "contenido": "Segundo comentario, con más detalles sobre el proceso."},
                {"usuario": usuario, "contenido": "Otro comentario más para completar los ejemplos."}
            ]
            for comentario_data in comentarios:
                comentario, created = Comentario.objects.get_or_create(
                    usuario=comentario_data["usuario"],
                    contenido=comentario_data["contenido"]
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Comentario creado: {comentario.contenido[:30]}...'))  # Muestra los primeros 30 caracteres del contenido
                else:
                    self.stdout.write(self.style.SUCCESS(f'Comentario ya existente: {comentario.contenido[:30]}...'))
        except Exception as e:
            raise CommandError(f'Error al crear instancias: {e}')
