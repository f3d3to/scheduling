import pytz
import datetime
# Third-party imports
import factory
from faker import Faker
from factory.fuzzy import FuzzyText, FuzzyInteger, FuzzyChoice, FuzzyDate
from django.contrib.auth import get_user_model

# Proyecto imports
from .models import PlanDeEstudio, Materia, MateriaEstudiante

Usuario = get_user_model()
fake = Faker()

class PlanDeEstudioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlanDeEstudio

    nombre = factory.Faker('sentence', nb_words=4)
    año_creacion = factory.Faker('year')
    descripcion = factory.Faker('paragraph', nb_sentences=3)

class MateriaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Materia

    plan_de_estudio = factory.SubFactory(PlanDeEstudioFactory)
    codigo = factory.Faker('bothify', text='MAT-###')
    anio = FuzzyInteger(1, 5)
    ciclo = factory.Faker('word')
    cuatrimestre = FuzzyInteger(1, 2)
    condicion = factory.Faker('word')
    nombre = factory.Faker('sentence', nb_words=3)
    formato_didactico = factory.Faker('word')
    ch_semanal = FuzzyInteger(1, 20)
    ch_cuatrimestral = FuzzyInteger(10, 200)
    creditos = FuzzyInteger(1, 10)
    ch_presencial = FuzzyInteger(0, 100)
    ch_distancia = FuzzyInteger(0, 100)
    ch_total = factory.LazyAttribute(lambda o: o.ch_presencial + o.ch_distancia)
    descripcion = factory.Faker('paragraph', nb_sentences=2)

    @factory.post_generation
    def correlativas(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for correlativa in extracted:
            self.correlativas.add(correlativa)

# factories.py
import datetime
import factory
from faker import Faker
from factory.fuzzy import FuzzyInteger, FuzzyChoice, FuzzyDate, FuzzyDecimal
from django.utils import timezone

# Proyecto imports
from plan_de_estudio.models import PlanDeEstudio, Materia, MateriaEstudiante, TipoEvaluacion, Evaluacion
from users.models import Usuario  # Asumiendo que tienes un modelo Usuario personalizado


# class MateriaFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Materia

#     plan_de_estudio = factory.SubFactory(PlanDeEstudioFactory)
#     codigo = factory.Sequence(lambda n: f"MAT-{n:03}")
#     anio = FuzzyInteger(1, 5)
#     ciclo = FuzzyChoice(choices=['Básico', 'Superior', 'Electivo'])
#     cuatrimestre = FuzzyInteger(1, 2)
#     condicion = FuzzyChoice(choices=['Regular', 'Libre'])
#     nombre = factory.Faker('sentence', nb_words=3)
#     formato_didactico = FuzzyChoice(choices=['Teórico', 'Práctico', 'Teórico-Práctico'])
#     ch_semanal = FuzzyInteger(1, 8)
#     ch_cuatrimestral = FuzzyInteger(30, 120)
#     creditos = FuzzyInteger(4, 8)
#     ch_presencial = FuzzyInteger(0, 100)
#     ch_distancia = FuzzyInteger(0, 50)
#     ch_total = factory.LazyAttribute(lambda o: o.ch_presencial + o.ch_distancia)
#     descripcion = factory.Faker('paragraph', nb_sentences=2)

#     @factory.post_generation
#     def correlativas(self, create, extracted, **kwargs):
#         if not create:
#             return

#         if extracted:
#           for correlativa in extracted:
#               self.correlativas.add(correlativa)
#         else:
#           # Seleccionar aleatoriamente hasta 2 correlativas, evitando agregar la misma materia
#           materias_disponibles = list(Materia.objects.exclude(pk=self.pk).order_by('?')[:2])
#           self.correlativas.add(*materias_disponibles)

class MateriaEstudianteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MateriaEstudiante

    estudiante = FuzzyChoice(choices=Usuario.objects.all())
    materia = factory.SubFactory(MateriaFactory)
    nota_final = FuzzyDecimal(low=4, high=10, precision=2)
    final_obligatorio = factory.Faker('boolean')
    catedra = factory.Faker('company')
    comentarios = factory.Faker('paragraph')
    intentos = FuzzyInteger(0, 3)
    comentarios_docente = factory.Faker('paragraph')
    estado = FuzzyChoice(choices=['pendiente', 'cursando', 'aprobada', 'desaprobada', 'promocionada'])
    fecha_inscripcion = FuzzyDate(start_date=datetime.date(2020, 1, 1), end_date=datetime.date.today())
    metodo_aprobacion = FuzzyChoice(choices=['final', 'promocion', 'equivalencia'])
    creditos_asignados = FuzzyInteger(2, 8)
    fecha_actualizacion = factory.LazyFunction(timezone.now)
    dificultad = FuzzyInteger(1, 5)

    @factory.post_generation
    def ensure_unique(self, create, extracted, **kwargs):
        if not create:
            return

        # Asegurarse de que no exista otra MateriaEstudiante con la misma materia y estudiante
        if MateriaEstudiante.objects.filter(estudiante=self.estudiante, materia=self.materia).exists():
            self.delete()

class TipoEvaluacionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TipoEvaluacion

    nombre = FuzzyChoice(choices=['Parcial', 'TP', 'Integrador', 'Coloquio', 'Examen Final'])
    descripcion = factory.Faker('paragraph', nb_sentences=1)
    peso_defecto = FuzzyDecimal(low=0.1, high=1.0, precision=2)

class EvaluacionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Evaluacion

    materia_estudiante = factory.SubFactory(MateriaEstudianteFactory)
    tipo = factory.SubFactory(TipoEvaluacionFactory)
    descripcion = factory.Faker('sentence', nb_words=4)
    nota = FuzzyDecimal(low=1, high=10, precision=2)
    fecha = FuzzyDate(start_date=datetime.date(2020, 1, 1), end_date=datetime.date.today())
