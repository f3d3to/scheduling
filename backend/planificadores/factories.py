import json
from datetime import datetime
# Third-party imports
import factory
from faker import Faker
from factory.fuzzy import FuzzyInteger
from factory import LazyAttribute

# Proyecto
from .models import Estado, EstructuraPlanificador, EstructuraElemento, Planificador, Celda, Elemento, Mensaje, Actividad, Tarea, Objetivo, RegistroProgreso, Etiqueta, Comentario, Recurrente, Evento, EventoAsociado
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


class EstructuraElementoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EstructuraElemento

    nombre = factory.Faker('sentence', nb_words=4)
    configuracion = LazyAttribute(
        lambda o: json.dumps({"vista":"html"})
    )
    fecha_edicion = factory.Faker('date_this_year')
    html_visualizacion = factory.Faker('text', max_nb_chars=500)

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
    estructura = factory.SubFactory(EstructuraElementoFactory)
    descripcion = factory.Faker('paragraph', nb_sentences=2)

    @factory.post_generation
    def assign_content_object(self, create, extracted, **kwargs):
        if create and extracted:
            self.content_type = extracted['content_type']
            self.object_id = extracted['object_id']
            self.save()

class MensajeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mensaje

    tipo = factory.Faker('word')
    icono = factory.Faker('word')
    color = factory.Faker('hex_color')

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

class RegistroProgresoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RegistroProgreso

    actividad = factory.SubFactory(ActividadFactory)
    porcentaje = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True, max_value=100)
    fecha_registro = factory.LazyFunction(lambda: datetime.now().isoformat())  # Serializado para JSON

class EtiquetaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Etiqueta

    nombre = factory.Faker('word')
    usuario = factory.SubFactory(UsuarioFactory)
    color = factory.Faker('hex_color')
    descripcion = factory.Faker('paragraph', nb_sentences=2)

class ComentarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comentario

    usuario = factory.SubFactory(UsuarioFactory)
    contenido = factory.Faker('paragraph', nb_sentences=3)
    fecha_creacion = factory.Faker('date_this_year')

class RecurrenteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recurrente

    frecuencia = factory.Faker('word')
    proxima_fecha = factory.Faker('date_this_year')

class EventoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Evento

    nombre = factory.Faker('sentence', nb_words=4)
    descripcion = factory.Faker('paragraph', nb_sentences=3)
    fecha_hora = factory.LazyFunction(lambda: datetime.now().isoformat())
    usuario = factory.SubFactory(UsuarioFactory)

class EventoAsociadoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventoAsociado

    evento = factory.SubFactory(EventoFactory)

    @factory.post_generation
    def assign_content_object(self, create, extracted, **kwargs):
        if create and extracted:
            self.content_type = extracted['content_type']
            self.object_id = extracted['object_id']
            self.save()
