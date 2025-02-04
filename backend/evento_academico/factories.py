import factory
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from evento_academico.models import (
    TipoEvento,
    MetaAcademica,
    ProgresoMateria,
    Recordatorio,
    TipoEventoAcademico,
    EventoAcademico,
    PlanificacionAcademica,
    ActividadPlanificada,
    Recurrencia,
    EventoCalendarioAcademico,
)
from users.models import Usuario
from plan_de_estudio.models import MateriaEstudiante, Materia

# Factory para TipoEvento
class TipoEventoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TipoEvento

    nombre = factory.Sequence(lambda n: f"TipoEvento {n}")
    descripcion = factory.Faker('text')

# Factory para MetaAcademica
class MetaAcademicaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MetaAcademica

    estudiante = factory.Iterator(Usuario.objects.all())  # Selecciona un usuario existente
    descripcion = factory.Faker('sentence')
    tipo = factory.Iterator(['Examen', 'Tarea', 'Proyecto'])
    completada = factory.Faker('boolean')
    relacion_materia = factory.Iterator(MateriaEstudiante.objects.all())  # Selecciona una materia existente

# Factory para ProgresoMateria
class ProgresoMateriaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgresoMateria

    materia_estudiante = factory.Iterator(MateriaEstudiante.objects.all())  # Selecciona una materia existente
    completados = factory.Faker('random_int', min=0, max=100)
    totales = factory.Faker('random_int', min=1, max=200)

# Factory para Recordatorio
class RecordatorioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recordatorio

    usuario = factory.Iterator(Usuario.objects.all())  # Selecciona un usuario existente
    mensaje = factory.Faker('sentence')
    fecha_hora = factory.LazyFunction(datetime.now)
    repetir = factory.Iterator(['UNA_VEZ', 'DIARIO', 'SEMANAL', 'MENSUAL'])
    medio_de_notificacion = factory.Iterator(['EMAIL', 'PUSH', 'SMS'])

# Factory para TipoEventoAcademico
class TipoEventoAcademicoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TipoEventoAcademico

    nombre = factory.Sequence(lambda n: f"TipoEventoAcademico {n}")
    descripcion = factory.Faker('text')

# Factory para EventoAcademico
class EventoAcademicoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventoAcademico

    materia = factory.Iterator(Materia.objects.all())  # Selecciona una materia existente
    tipo = factory.SubFactory(TipoEventoAcademicoFactory)
    dia = factory.Iterator(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
    hora_inicio = factory.LazyFunction(lambda: (datetime.now() + timedelta(hours=1)).time())
    hora_fin = factory.LazyFunction(lambda: (datetime.now() + timedelta(hours=2)).time())
    es_obligatorio = factory.Faker('boolean')
    recursos = factory.Faker('text')

# Factory para PlanificacionAcademica
class PlanificacionAcademicaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlanificacionAcademica

    estudiante = factory.Iterator(Usuario.objects.all())  # Selecciona un usuario existente
    tipo = factory.Iterator(['SEMANAL', 'CUATRIMESTRAL', 'ANUAL'])
    cuatrimestre = factory.Maybe(
        factory.LazyAttribute(lambda o: o.tipo == 'CUATRIMESTRAL'),
        yes_declaration=factory.Iterator(['1', '2']),
        no_declaration=None
    )
    nombre = factory.Sequence(lambda n: f"Planificación {n}")
    semana = factory.Maybe(
        factory.LazyAttribute(lambda o: o.tipo == 'SEMANAL'),
        yes_declaration=factory.Faker('random_int', min=1, max=52),
        no_declaration=None
    )
    año = factory.LazyFunction(lambda: datetime.now().year)

    @factory.post_generation
    def actividades(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for actividad in extracted:
                self.actividades.add(actividad)

# Factory para ActividadPlanificada
class ActividadPlanificadaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActividadPlanificada

    planificacion = factory.SubFactory(PlanificacionAcademicaFactory)
    evento = factory.SubFactory(EventoAcademicoFactory)
    completada = factory.Faker('boolean')

# Factory para Recurrencia
class RecurrenciaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recurrencia

    frecuencia = factory.Iterator(['diaria', 'semanal', 'mensual', 'anual'])
    intervalo = factory.Faker('random_int', min=1, max=5)
    fin_recurrencia = factory.LazyFunction(lambda: (datetime.now() + timedelta(days=30)).date())

# Factory para EventoCalendarioAcademico
class EventoCalendarioAcademicoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventoCalendarioAcademico

    titulo = factory.Sequence(lambda n: f"Evento {n}")
    descripcion = factory.Faker("paragraph")
    inicio = factory.Faker("future_datetime", end_date="+30d")
    fin = factory.LazyAttribute(lambda o: o.inicio + timedelta(hours=2))
    todo_el_dia = factory.Faker("boolean")
    color = factory.Faker("hex_color")
    background_color = factory.Faker("hex_color")
    border_color = factory.Faker("hex_color")
    text_color = factory.Faker("hex_color")
    url = factory.Faker("url")
    tipo = factory.SubFactory("evento_academico.factories.TipoEventoFactory")
    recurrencia = factory.SubFactory("evento_academico.factories.RecurrenciaFactory", null=True)
    content_type = factory.LazyFunction(lambda: ContentType.objects.get(app_label="evento_academico", model="eventoacademico"))
    object_id = factory.Sequence(lambda n: n + 1)

    # Nuevos campos
    display = factory.Iterator(["block", "list-item", "background", "none"])
    editable = factory.Faker("boolean")
    start_editable = factory.Faker("boolean")
    duration_editable = factory.Faker("boolean")
    resource_editable = factory.Faker("boolean")
    exdate = factory.Faker("random_element", elements=[None, "2025-02-05T14:11:00Z"])
    class_names = factory.Faker("word")