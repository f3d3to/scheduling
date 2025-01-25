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

        # Códigos de materias a marcar como promocionadas para user1 (plan_id=2)
        materias_promocionadas_user1 = {
            'CC01', 'CC03', 'CC04', 'CC06', 'CC08',
            'CP100', 'CP43', 'RI1', 'RI10', 'RI2',
            'RI7', 'S18', 'S29', 'S30', 'S31'
        }

        # Crear Tipos de Evaluación predefinidos
        tipos_evaluacion_predefinidos = ['Parcial', 'TP', 'Integrador', 'Coloquio', 'Examen Final']
        for nombre_tipo in tipos_evaluacion_predefinidos:
            TipoEvaluacion.objects.get_or_create(
                nombre=nombre_tipo,
                defaults={
                    'descripcion': f'Descripción de {nombre_tipo}',
                    'peso_defecto': 0.5
                }
            )

        tipos_evaluacion = list(TipoEvaluacion.objects.all())

        for usuario in usuarios:
            # Lógica especial para user1 (plan_id=2)
            if usuario.username == 'user1':
                # Filtrar solo materias del plan_id=2 y condición "carrera"
                for materia in materias:
                    if materia.plan_de_estudio_id == 2 and materia.condicion == "carrera":
                        # Marcar como promocionada si está en la lista
                        estado = 'promocionada' if materia.codigo in materias_promocionadas_user1 else 'pendiente'
                        materia_estudiante = MateriaEstudianteFactory(
                            estudiante=usuario,
                            materia=materia,
                            estado=estado  # Sobreescribir el estado
                        )

                        # Crear evaluaciones
                        tipo_evaluacion = random.choice(tipos_evaluacion)
                        num_evaluaciones = random.randint(1, 3)
                        for _ in range(num_evaluaciones):
                            EvaluacionFactory(materia_estudiante=materia_estudiante, tipo=tipo_evaluacion)

                        self.stdout.write(self.style.SUCCESS(
                            f'Creada MateriaEstudiante para {usuario.username} con materia {materia.nombre} (Estado: {estado})'
                        ))

            # Lógica normal para otros usuarios (user2, user3, etc.)
            elif re.match(r"^user\d+$", usuario.username):
                for materia in materias:
                    if materia.condicion == "carrera":
                        materia_estudiante = MateriaEstudianteFactory(estudiante=usuario, materia=materia)

                        # Crear evaluaciones
                        tipo_evaluacion = random.choice(tipos_evaluacion)
                        num_evaluaciones = random.randint(1, 3)
                        for _ in range(num_evaluaciones):
                            EvaluacionFactory(materia_estudiante=materia_estudiante, tipo=tipo_evaluacion)

                        self.stdout.write(self.style.SUCCESS(
                            f'Creada MateriaEstudiante para {usuario.username} con materia {materia.nombre}'
                        ))

        self.stdout.write(self.style.SUCCESS('Datos de prueba creados exitosamente.'))