from django.core.management.base import BaseCommand, CommandError
from .tools import importar_plan_de_estudios
from plan_de_estudio.models import PlanDeEstudio
import os

class Command(BaseCommand):
    help = 'Importa planes de estudio desde archivos Excel hardcodeados si no están creados'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_cdd = os.path.join(base_dir, 'CdD_PLAN.xlsx')
        ruta_ri = os.path.join(base_dir, 'RI_PLAN.xlsx')
        ruta_info = os.path.join(base_dir, 'INFORMATICA_PLAN.xlsx')

        planes = [
            {"ruta": ruta_info, "nombre_plan": "Ingeniería Informática", "año_creacion": 2023, "descripcion": "Plan de estudio para Ingeniería Informática"},
            {"ruta": ruta_ri, "nombre_plan": "Relaciones Internacionales", "año_creacion": 2020, "descripcion": "Plan de estudio para Relaciones Internacionales"},
            {"ruta": ruta_cdd, "nombre_plan": "Licenciatura en Ciencia de Datos", "año_creacion": 2021, "descripcion": "Plan de estudio para Licenciatura en Ciencia de Datos"},
        ]

        try:
            for plan in planes:
                # Verificar si el plan ya existe
                if PlanDeEstudio.objects.filter(nombre=plan["nombre_plan"]).exists():
                    self.stdout.write(self.style.WARNING(f'El plan "{plan["nombre_plan"]}" ya existe.'))
                else:
                    # Importar el plan si no existe
                    importar_plan_de_estudios(
                        plan["ruta"],
                        nombre_plan=plan["nombre_plan"],
                        año_creacion=plan["año_creacion"],
                        descripcion=plan["descripcion"]
                    )
                    self.stdout.write(self.style.SUCCESS(f'Se importó "{plan["nombre_plan"]}" correctamente'))
        except Exception as e:
            raise CommandError(f'Error al importar planes de estudio: {e}')
