import json
from datetime import datetime
# Third-party imports
import factory
from faker import Faker
from factory.fuzzy import FuzzyInteger
from factory import LazyAttribute

# Proyecto
from .models import Estado, EstructuraPlanificador, Planificador, Celda, Elemento, Actividad, Tarea, Objetivo
from users.factories import UsuarioFactory
fake = Faker()

class EstadoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Estado

    nombre = factory.Faker('word')
    descripcion = factory.Faker('paragraph', nb_sentences=2)
    color = factory.Faker('hex_color')
    orden = FuzzyInteger(1, 10)

class EstructuraPlanificadorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EstructuraPlanificador

    nombre = factory.Faker('sentence', nb_words=4)
    configuracion = factory.LazyAttribute(lambda _: json.dumps({"tipo": "tabla", "filas": 5, "columnas": 5}))
    filas = FuzzyInteger(1, 10)
    columnas = FuzzyInteger(1, 10)
    ancho_columna = FuzzyInteger(50, 200)
    tabla = LazyAttribute(
        lambda o: json.dumps({
            f"{i},{j}": {"id": "", "contenido": f"Celda {i}-{j}"}
            for i in range(1, o.filas + 1)
            for j in range(1, o.columnas + 1)
        })
    )

class PlanificadorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Planificador

    nombre = factory.Faker('sentence', nb_words=4)
    tipo = factory.Faker('word')
    estructura = factory.SubFactory(EstructuraPlanificadorFactory)

    @factory.post_generation
    def print_creation(self, create, extracted, **kwargs):
        if create:  # Solo imprime si la instancia fue creada
            print(f"Planificador creado: {self.nombre}, tipo: {self.tipo}, estructura: {self.estructura.nombre}")


class CeldaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Celda

    planificador = factory.SubFactory(PlanificadorFactory)
    contenido = factory.Faker('paragraph', nb_sentences=2)
    fila = FuzzyInteger(1, 5)
    columna = FuzzyInteger(1, 5)

class ElementoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Elemento

    nombre = factory.Faker('sentence', nb_words=3)
    celda = factory.SubFactory(CeldaFactory)
    descripcion = factory.Faker('paragraph', nb_sentences=2)

    @factory.post_generation
    def assign_content_object(self, create, extracted, **kwargs):
        if create and extracted:
            self.content_type = extracted['content_type']
            self.object_id = extracted['object_id']
            self.save()

class ActividadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Actividad

    planificador = factory.SubFactory(PlanificadorFactory)
    nombre = factory.Faker('sentence', nb_words=4)
    descripcion = factory.Faker('paragraph', nb_sentences=3)
    fecha_inicio = factory.Faker('date_this_year')
    fecha_fin = factory.Faker('date_this_year')
    color = factory.Faker('hex_color')

class TareaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tarea

    actividad = factory.SubFactory(ActividadFactory)
    nombre = factory.Faker('sentence', nb_words=4)
    descripcion = factory.Faker('paragraph', nb_sentences=3)
    fecha_limite = factory.Faker('date_this_year')
    color = factory.Faker('hex_color')
    esta_realizada = factory.Faker('boolean')

class ObjetivoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Objetivo

    descripcion = factory.Faker('paragraph', nb_sentences=3)
    fecha_objetivo = factory.Faker('date_this_year')
    completado = factory.Faker('boolean')

    @factory.post_generation
    def assign_content_object(self, create, extracted, **kwargs):
        if create and extracted:
            self.content_type = extracted['content_type']
            self.object_id = extracted['object_id']
            self.save()
