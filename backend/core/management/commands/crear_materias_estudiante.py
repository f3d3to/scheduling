# Python
import re
import random
# Django
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
# Proyecto
from plan_de_estudio.models import Materia, TipoEvaluacion
from plan_de_estudio.factories import MateriaEstudianteFactory, EvaluacionFactory

Usuario = get_user_model()
class Command(BaseCommand):
    help = 'Crea datos de prueba para MateriaEstudiante y Evaluacion para cada usuario.'

    def handle(self, *args, **options):
        usuarios = Usuario.objects.all()
        materias = list(Materia.objects.all())

        if not materias:
            self.stdout.write(self.style.WARNING('No hay materias creadas. Crea algunas materias primero.'))
            return

        # Crear Tipos de Evaluación predefinidos si no existen
        tipos_evaluacion_predefinidos = ['Parcial', 'TP', 'Integrador', 'Coloquio', 'Examen Final']
        for nombre_tipo in tipos_evaluacion_predefinidos:
            TipoEvaluacion.objects.get_or_create(
                nombre=nombre_tipo,
                defaults={
                    'descripcion': f'Descripción de {nombre_tipo}',
                    'peso_defecto': 0.5  # Puedes ajustar el peso por defecto
                }
            )

        tipos_evaluacion = list(TipoEvaluacion.objects.all())  # Obtener todos los tipos de evaluacion

        for usuario in usuarios:
            # Asignar todas las materias a cada usuario
            for materia in materias:
                if materia.condicion == "carrera" and re.match(r"^user\d+$", usuario.username):
                    materia_estudiante = MateriaEstudianteFactory(estudiante=usuario, materia=materia)

                    # Obtener un TipoEvaluacion aleatorio
                    tipo_evaluacion = random.choice(tipos_evaluacion)

                    # Crear entre 1 y 3 Evaluaciones para cada MateriaEstudiante
                    num_evaluaciones = random.randint(1, 3)
                    for _ in range(num_evaluaciones):
                        EvaluacionFactory(materia_estudiante=materia_estudiante, tipo=tipo_evaluacion)

                    self.stdout.write(self.style.SUCCESS(
                        f'Creada MateriaEstudiante para {usuario.username} con materia {materia.nombre} y sus evaluaciones.'
                    ))

        self.stdout.write(self.style.SUCCESS('Datos de prueba creados exitosamente.'))