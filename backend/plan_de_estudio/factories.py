import pytz
# Third-party imports
import factory
from faker import Faker
from factory.fuzzy import FuzzyText, FuzzyInteger

# Proyecto imports
from .models import PlanDeEstudio, Materia

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
