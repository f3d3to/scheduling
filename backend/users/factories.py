import pytz
# Third-party imports
import factory
from faker import Faker
from factory.fuzzy import FuzzyText

# Proyecto imports
from .models import Usuario

fake = Faker()

class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    perfil = factory.Faker('text', max_nb_chars=200)

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password("password")
