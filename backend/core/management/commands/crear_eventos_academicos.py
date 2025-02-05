# backend/evento_academico/management/commands/init_data.py
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from users.models import Usuario
from evento_academico.factories import (
    TipoEventoFactory,
    RecurrenciaFactory,
    EventoCalendarioAcademicoFactory,
    MetaAcademicaFactory,
    ProgresoMateriaFactory,
    RecordatorioFactory,
    EventoAcademicoFactory,
    PlanificacionAcademicaFactory,
    ActividadPlanificadaFactory,
)
from plan_de_estudio.models import MateriaEstudiante
from planificadores.models import Actividad, Tarea, Objetivo  # Importa los nuevos modelos


class Command(BaseCommand):
    help = "Inicializa datos de prueba para el usuario 'user1'"

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando creación de datos para el usuario 'user1'...")

        # Paso 1: Obtener el usuario "user1"
        try:
            user1 = Usuario.objects.get(username="user1")
        except Usuario.DoesNotExist:
            self.stdout.write(self.style.ERROR("El usuario 'user1' no existe. Por favor, crea este usuario antes de ejecutar el comando."))
            return

        # Paso 2: Verificar que el usuario tenga materias asignadas
        materias_estudiante = MateriaEstudiante.objects.filter(estudiante=user1)
        if not materias_estudiante.exists():
            self.stdout.write(self.style.ERROR("El usuario 'user1' no tiene materias asignadas. Por favor, asigna materias antes de ejecutar el comando."))
            return

        # Paso 3: Crear instancias adicionales de modelos básicos
        self.stdout.write("Creando tipos de eventos y recurrencias...")
        tipo_evento_examen = TipoEventoFactory(nombre="Examen", descripcion="Un evento de tipo examen.")
        tipo_evento_clase = TipoEventoFactory(nombre="Clase", descripcion="Un evento de tipo clase.")
        tipo_evento_tarea = TipoEventoFactory(nombre="Tarea", descripcion="Un evento de tipo tarea.")

        recurrencia_diaria = RecurrenciaFactory(frecuencia="diaria", intervalo=1)
        recurrencia_semanal = RecurrenciaFactory(frecuencia="semanal", intervalo=1)
        recurrencia_mensual = RecurrenciaFactory(frecuencia="mensual", intervalo=1)

        # Paso 4: Verificar que haya actividades, tareas y objetivos existentes
        actividades = Actividad.objects.all()
        tareas = Tarea.objects.all()
        objetivos = Objetivo.objects.all()

        if not actividades.exists() or not tareas.exists() or not objetivos.exists():
            self.stdout.write(self.style.ERROR("No hay suficientes actividades, tareas u objetivos en la base de datos. Crea al menos una instancia de cada uno antes de ejecutar el comando."))
            return

        # Paso 5: Usar factories para generar datos adicionales para "user1"
        self.stdout.write("Generando datos adicionales con factories...")
        for i in range(5):  # Genera 5 instancias de cada modelo
            # Seleccionar una materia aleatoria del usuario
            materia_estudiante = materias_estudiante.order_by('?').first()

            # Meta Académica
            meta = MetaAcademicaFactory(
                estudiante=user1,
                relacion_materia=materia_estudiante,
                tipo=["Examen", "Tarea", "Proyecto"][i % 3]  # Rotación de tipos
            )

            # Progreso Materia
            progreso = ProgresoMateriaFactory(
                materia_estudiante=materia_estudiante,
                completados=(i + 1) * 20,  # Incremento gradual
                totales=100
            )

            # Recordatorio Personalizado
            RecordatorioFactory(
                usuario=user1,
                mensaje=f"Recordatorio {i + 1} para {materia_estudiante.materia.nombre}",
                fecha_hora=datetime.now() + timedelta(days=i + 1),
                repetir=["UNA_VEZ", "DIARIO", "SEMANAL"][i % 3],
                medio_de_notificacion=["EMAIL", "PUSH", "SMS"][i % 3]
            )

            # Evento Académico
            evento_academico = EventoAcademicoFactory(
                materia=materia_estudiante.materia,
                tipo__nombre=["Clase", "Examen", "Tarea"][i % 3],
                dia=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"][i % 5],
                hora_inicio=(datetime.now() + timedelta(hours=8 + i)).time(),
                hora_fin=(datetime.now() + timedelta(hours=10 + i)).time()
            )

            # Evento Calendario Académico asociado a Actividad
            actividad = actividades.order_by('?').first()
            content_type_actividad = ContentType.objects.get_for_model(Actividad)
            EventoCalendarioAcademicoFactory(
                titulo=f"Evento {i + 1} para Actividad: {actividad.nombre}",
                descripcion=f"Descripción del evento académico {i + 1}.",
                inicio=datetime.now() + timedelta(days=i + 1),
                fin=datetime.now() + timedelta(days=i + 1, hours=2),
                todo_el_dia=False,
                color=["#FF5733", "#33FF57", "#3357FF"][i % 3],  # Colores variados
                background_color=["#FFC300", "#C3FF00", "#00FFC3"][i % 3],
                border_color=["#C70039", "#00C739", "#3900C7"][i % 3],
                text_color="#FFFFFF",
                url="https://ejemplo.com",
                tipo=[tipo_evento_examen, tipo_evento_clase, tipo_evento_tarea][i % 3],
                recurrencia=[recurrencia_diaria, recurrencia_semanal, recurrencia_mensual][i % 3],
                content_type=content_type_actividad,
                object_id=actividad.id
            )

            # Evento Calendario Académico asociado a Tarea
            tarea = tareas.order_by('?').first()
            content_type_tarea = ContentType.objects.get_for_model(Tarea)
            EventoCalendarioAcademicoFactory(
                titulo=f"Evento {i + 1} para Tarea: {tarea.nombre}",
                descripcion=f"Descripción del evento académico {i + 1}.",
                inicio=datetime.now() + timedelta(days=i + 1),
                fin=datetime.now() + timedelta(days=i + 1, hours=2),
                todo_el_dia=False,
                color=["#FF5733", "#33FF57", "#3357FF"][i % 3],  # Colores variados
                background_color=["#FFC300", "#C3FF00", "#00FFC3"][i % 3],
                border_color=["#C70039", "#00C739", "#3900C7"][i % 3],
                text_color="#FFFFFF",
                url="https://ejemplo.com",
                tipo=[tipo_evento_examen, tipo_evento_clase, tipo_evento_tarea][i % 3],
                recurrencia=[recurrencia_diaria, recurrencia_semanal, recurrencia_mensual][i % 3],
                content_type=content_type_tarea,
                object_id=tarea.id
            )

            # Evento Calendario Académico asociado a Objetivo
            objetivo = objetivos.order_by('?').first()
            content_type_objetivo = ContentType.objects.get_for_model(Objetivo)
            EventoCalendarioAcademicoFactory(
                titulo=f"Evento {i + 1} para Objetivo: {objetivo.descripcion[:20]}...",
                descripcion=f"Descripción del evento académico {i + 1}.",
                inicio=datetime.now() + timedelta(days=i + 1),
                fin=datetime.now() + timedelta(days=i + 1, hours=2),
                todo_el_dia=False,
                color=["#FF5733", "#33FF57", "#3357FF"][i % 3],  # Colores variados
                background_color=["#FFC300", "#C3FF00", "#00FFC3"][i % 3],
                border_color=["#C70039", "#00C739", "#3900C7"][i % 3],
                text_color="#FFFFFF",
                url="https://ejemplo.com",
                tipo=[tipo_evento_examen, tipo_evento_clase, tipo_evento_tarea][i % 3],
                recurrencia=[recurrencia_diaria, recurrencia_semanal, recurrencia_mensual][i % 3],
                content_type=content_type_objetivo,
                object_id=objetivo.id
            )

        self.stdout.write(self.style.SUCCESS("Datos iniciales creados exitosamente para el usuario 'user1'."))