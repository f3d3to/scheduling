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
        materias_estudiante = user1.materias_estudiante.all()
        if not materias_estudiante.exists():
            self.stdout.write(self.style.ERROR("El usuario 'user1' no tiene materias asignadas. Por favor, asigna materias antes de ejecutar el comando."))
            return

        # Paso 3: Usar factories para generar datos adicionales para "user1"
        self.stdout.write("Generando datos adicionales con factories...")
        for _ in range(5):  # Genera 5 instancias de cada modelo
            MetaAcademicaFactory(estudiante=user1)
            ProgresoMateriaFactory(materia_estudiante=factory.Iterator(materias_estudiante))
            RecordatorioPersonalizadoFactory(usuario=user1)
            PlanificacionAcademicaFactory(estudiante=user1)

        # Paso 4: Crear eventos académicos y actividades planificadas
        for _ in range(5):
            evento = EventoAcademicoFactory(materia=factory.Iterator(materias_estudiante.values_list('materia', flat=True)))
            ActividadPlanificadaFactory(planificacion=factory.Iterator(user1.planificaciones.all()), evento=evento)

        self.stdout.write(self.style.SUCCESS("Datos iniciales creados exitosamente para el usuario 'user1'."))