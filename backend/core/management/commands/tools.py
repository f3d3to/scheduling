import pandas as pd
from django.db import transaction
from plan_de_estudio.models import PlanDeEstudio, Materia

def importar_plan_de_estudios(ruta_archivo, nombre_plan="Ciencia de Datos", año_creacion=2021, descripcion=""):
    # Leer el archivo Excel
    df = pd.read_excel(ruta_archivo)

    # Verificar que la columna 'codigo' y 'materia' existan
    required_columns = ['codigo', 'materia', 'creditos', 'correlativas']
    if not all(col in df.columns for col in required_columns):
        print(f"Error: El archivo Excel debe contener las columnas: {', '.join(required_columns)}")
        return

    with transaction.atomic():
        # Crear el Plan de Estudio
        plan = PlanDeEstudio.objects.create(
            nombre=nombre_plan,
            año_creacion=año_creacion,
            descripcion=descripcion
        )
        # Primera pasada: Crear todas las materias
        materias_creadas = {}
        for _, row in df.iterrows():
            codigo = row['codigo'] if pd.notna(row['codigo']) else row['materia'][:9]
            # Crear la materia sin correlativas
            materia, created = Materia.objects.get_or_create(
                codigo=codigo,  # Buscar solo por código
                defaults={
                    'plan_de_estudio': plan,
                    'nombre': row['materia'] if pd.notna(row['materia']) else '',
                    'anio': row['anio'] if pd.notna(row['anio']) else '',
                    'ciclo': row['ciclo'] if pd.notna(row['ciclo']) else '',
                    'cuatrimestre': row['cuatrimestre'] if pd.notna(row['cuatrimestre']) else 0,
                    'condicion': row['condicion'] if pd.notna(row['condicion']) else '',
                    'formato_didactico': row['formato_didactico'] if pd.notna(row['formato_didactico']) else '',
                    'ch_semanal': row['ch_semanal'] if pd.notna(row['ch_semanal']) else 0,
                    'ch_cuatrimestral': row['ch_cuatrimestral'] if pd.notna(row['ch_cuatrimestral']) else 0,
                    'creditos': row['creditos'] if pd.notna(row['creditos']) else 0,
                    'ch_presencial': row['ch_presencial'] if pd.notna(row['ch_presencial']) else 0,
                    'ch_distancia': row['ch_distancia'] if pd.notna(row['ch_distancia']) else 0,
                    'ch_total': row['ch_total'] if pd.notna(row['ch_total']) else 0,
                    'descripcion': row['descripcion'] if pd.notna(row['descripcion']) else ''
                }
            )
            materias_creadas[codigo] = materia

        # Segunda pasada: Asignar correlativas
        codigos_faltantes = set()
        for _, row in df.iterrows():
            codigo = row['codigo'] if pd.notna(row['codigo']) else row['materia'][:9]
            materia = materias_creadas.get(codigo)

            if pd.notna(row.get('correlativas', '')):
                correlativas_codigos = row['correlativas'].split('|')
                for correlativa_codigo in correlativas_codigos:
                    correlativa_codigo = correlativa_codigo.strip()
                    correlativa_materia = materias_creadas.get(correlativa_codigo)
                    if correlativa_materia:
                        materia.correlativas.add(correlativa_materia)
                    else:
                        codigos_faltantes.add(correlativa_codigo)

        # Log de advertencias para correlativas no encontradas
        if codigos_faltantes:
            print("Advertencias: No se encontraron las siguientes materias correlativas:")
            for codigo in codigos_faltantes:
                print(f" - {codigo}")

print("Importación completada con advertencias si hay correlativas faltantes.")
