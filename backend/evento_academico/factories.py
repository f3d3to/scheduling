# backend/evento_academico/factories.py
import factory
from django.utils import timezone
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from faker import Faker
from datetime import timedelta

from users.models import Usuario  # Importamos el modelo Usuario
from planificadores.models import Evento  # Importamos el modelo Evento
from plan_de_estudio.models import Materia, MateriaEstudiante  # Importamos los modelos relacionados
from .models import (
    MetaAcademica,
    ProgresoMateria,
    RecordatorioPersonalizado,
    EventoAsociadoAcademico,
    EventoAcademico,
    PlanificacionAcademica,
    ActividadPlanificada,
)

fake = Faker()

class MetaAcademicaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MetaAcademica

    estudiante = factory.Iterator(Usuario.objects.all())  # Selecciona un usuario existente
    descripcion = factory.Faker("sentence", nb_words=5)
    tipo = FuzzyChoice([choice[0] for choice in MetaAcademica.TIPO_META])
    fecha_limite = factory.LazyFunction(lambda: timezone.now() + timedelta(days=30))
    prioridad = FuzzyInteger(1, 5)
    completada = FuzzyChoice([True, False])

    @factory.lazy_attribute
    def relacion_materia(self):
        # Filtra las materias del estudiante seleccionado
        materias_estudiante = MateriaEstudiante.objects.filter(estudiante=self.estudiante)
        return factory.Iterator(materias_estudiante).next() if materias_estudiante.exists() else None


class ProgresoMateriaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgresoMateria

    @factory.lazy_attribute
    def materia_estudiante(self):
        # Filtra las materias del usuario seleccionado
        materias_estudiante = MateriaEstudiante.objects.filter(estudiante=factory.Iterator(Usuario.objects.all()))
        return factory.Iterator(materias_estudiante).next() if materias_estudiante.exists() else None

    horas_estudiadas = FuzzyInteger(0, 100)
    temas_completados = FuzzyInteger(0, 20)
    ejercicios_resueltos = FuzzyInteger(0, 50)
    autoevaluaciones = FuzzyInteger(0, 10)


class RecordatorioPersonalizadoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecordatorioPersonalizado

    usuario = factory.Iterator(Usuario.objects.all())  # Selecciona un usuario existente
    mensaje = factory.Faker("sentence", nb_words=6)
    fecha_hora = factory.LazyFunction(lambda: timezone.now() + timedelta(days=7))
    repetir = FuzzyChoice([choice[0] for choice in RecordatorioPersonalizado.FRECUENCIA_CHOICES])
    canal = FuzzyChoice([choice[0] for choice in RecordatorioPersonalizado.CANAL_CHOICES])
    relacion_evento = factory.SubFactory("planificadores.factories.EventoFactory")  # Referencia externa


class EventoAcademicoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventoAcademico

    dia = FuzzyChoice([choice[0] for choice in EventoAcademico.DIA_CHOICES])
    hora_inicio = factory.LazyFunction(lambda: (timezone.now() + timedelta(hours=1)).time())
    hora_fin = factory.LazyFunction(lambda: (timezone.now() + timedelta(hours=2)).time())
    descripcion_horario = factory.Faker("sentence", nb_words=8)

    @factory.lazy_attribute
    def materia(self):
        # Selecciona una materia existente
        return factory.Iterator(Materia.objects.all()).next() if Materia.objects.exists() else None

    tipo = FuzzyChoice([choice[0] for choice in EventoAcademico.TIPO_EVENTO])
    aula = factory.Faker("word")
    profesor = factory.Faker("name")
    es_obligatorio = FuzzyChoice([True, False])
    recursos = factory.Faker("paragraph")


class EventoAsociadoAcademicoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventoAsociadoAcademico

    evento_origen = factory.SubFactory(EventoAcademicoFactory)
    evento_destino = factory.SubFactory(EventoAcademicoFactory)
    tipo_relacion = FuzzyChoice([choice[0] for choice in EventoAsociadoAcademico.TIPO_RELACION])
    peso = FuzzyInteger(1, 5)


class PlanificacionAcademicaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlanificacionAcademica

    estudiante = factory.Iterator(Usuario.objects.all())  # Selecciona un usuario existente
    tipo = FuzzyChoice([choice[0] for choice in PlanificacionAcademica.TIPO_PLANIFICACION])
    cuatrimestre = FuzzyChoice(["1", "2"])
    año = factory.LazyFunction(lambda: timezone.now().year)
    semana = FuzzyInteger(1, 52)
    nombre = factory.Faker("sentence", nb_words=4)


class ActividadPlanificadaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActividadPlanificada

    planificacion = factory.SubFactory(PlanificacionAcademicaFactory)
    evento = factory.SubFactory("planificadores.factories.EventoFactory")  # Referencia externa
    completada = FuzzyChoice([True, False])