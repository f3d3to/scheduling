# backend/evento_academico/management/commands/init_data.py
from django.core.management.base import BaseCommand
from users.models import Usuario
from evento_academico.factories import (
    MetaAcademicaFactory,
    ProgresoMateriaFactory,
    RecordatorioPersonalizadoFactory,
    EventoAcademicoFactory,
    PlanificacionAcademicaFactory,
    ActividadPlanificadaFactory,
)
from plan_de_estudio.models import MateriaEstudiante

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

        # Paso 3: Usar factories para generar datos adicionales para "user1"
        self.stdout.write("Generando datos adicionales con factories...")
        for _ in range(5):  # Genera 5 instancias de cada modelo
            # Meta Académica
            materia_estudiante = materias_estudiante.order_by('?').first()  # Selecciona una materia aleatoria
            meta = MetaAcademicaFactory(estudiante=user1, relacion_materia=materia_estudiante)

            # Progreso Materia
            ProgresoMateriaFactory(materia_estudiante=materia_estudiante)

            # Recordatorio Personalizado
            RecordatorioPersonalizadoFactory(usuario=user1)

            # Planificación Académica
            planificacion = PlanificacionAcademicaFactory(estudiante=user1)

            # Evento Académico
            evento = EventoAcademicoFactory(materia=materia_estudiante.materia)

            # Actividad Planificada
            ActividadPlanificadaFactory(planificacion=planificacion, evento=evento)

        self.stdout.write(self.style.SUCCESS("Datos iniciales creados exitosamente para el usuario 'user1'."))