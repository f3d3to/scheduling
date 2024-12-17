from django.core.management.base import BaseCommand, CommandError
from .tools import importar_plan_de_estudios
import os

class Command(BaseCommand):
    help = 'Importa planes de estudio desde archivos Excel hardcodeados'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_cdd = os.path.join(base_dir, 'CdD_PLAN.xlsx')
        ruta_ri = os.path.join(base_dir, 'RI_PLAN.xlsx')
        ruta_info = os.path.join(base_dir, 'INFORMATICA_PLAN.xlsx')


        # Proceso de importación para cada archivo
        try:
            importar_plan_de_estudios(ruta_info, nombre_plan="Relaciones Internacionales", año_creacion=2020, descripcion="Plan de estudio para Ingeniería Informática")
            self.stdout.write(self.style.SUCCESS(f'Se importó INFO correctamente'))

            importar_plan_de_estudios(ruta_ri, nombre_plan="Relaciones Internacionales", año_creacion=2020, descripcion="Plan de estudio para  Relaciones Internacionales")
            self.stdout.write(self.style.SUCCESS(f'Se importó RI correctamente'))

            importar_plan_de_estudios(ruta_cdd, nombre_plan="Licenciatura en Ciencia de Datos", año_creacion=2021, descripcion="Plan de estudio para Licenciatura en Ciencia de Datos")
            self.stdout.write(self.style.SUCCESS(f'Se importó CdD correctamente'))
        except Exception as e:
            raise CommandError(f'Error al importar planes de estudio: {e}')
