import pytz
# Third-party imports
import factory
from faker import Faker
from factory.fuzzy import FuzzyInteger

# Proyecto imports
from .models import Sesion, TareaTimer
from planificadores.factories import TareaFactory
fake = Faker()

class SesionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sesion

    nombre = factory.Faker('sentence', nb_words=1)
    duracion_minutos = FuzzyInteger(1, 60)
    es_obligatoria = factory.Faker('boolean')
    fecha_creacion = factory.Faker('date_time_this_year')

class TareaTimerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TareaTimer

    tarea = factory.SubFactory(TareaFactory)
    cantidad_para_completar = FuzzyInteger(1, 10)
    cantidad_completadas = FuzzyInteger(0, 10)

    @factory.post_generation
    def sesiones(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for sesion in extracted:
            self.sesiones.add(sesion)
