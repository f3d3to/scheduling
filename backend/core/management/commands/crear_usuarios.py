from django.core.management.base import BaseCommand, CommandError
from users.models import Usuario  # Importa el modelo Usuario

class Command(BaseCommand):
    help = 'Crea usuarios con sus nombres como contraseñas si no existen'

    def handle(self, *args, **options):
        try:
            # Lista de nombres de usuario que se desean crear
            usernames = ["user1", "user2", "user3", "user4", "user5"]

            for username in usernames:
                # Crear el usuario si no existe, la contraseña será el mismo nombre de usuario
                usuario, created = Usuario.objects.get_or_create(
                    username=username,
                    defaults={
                        "password": username,  # Usamos el nombre de usuario como contraseña
                        "perfil": f"Perfil de {username}"  # Descripción básica del perfil
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Usuario creado: {usuario.username}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Usuario ya existe: {usuario.username}'))

        except Exception as e:
            raise CommandError(f'Error al crear usuarios: {e}')
