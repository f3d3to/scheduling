"""
Script de inicio para la aplicación Django con el servidor Gunicorn.

Este script realiza varias tareas esenciales al iniciar la aplicación Django, como aplicar migraciones,
recopilar archivos estáticos, configurar datos de prueba y seleccionar entre el servidor de desarrollo y Gunicorn.

Uso:
    Este script se ejecuta al través del módulo 'docker-compose.yml'.
"""
# Python
import os
import subprocess
# Django
from django.core.management import execute_from_command_line
from django.conf import settings
# Proyecto
from dbwait import wait_for_databases

# Definir códigos ANSI para colores
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

# Imprimir todas las variables de entorno
if settings.DEBUG:
    print(f"{RED}Variables de entorno:{RESET}")
    for key, value in os.environ.items():
        print(f"{YELLOW}{key}: {value}{RESET}")
django_settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings_module)
wait_for_databases()

print(f"{BLUE}Aplicando migraciones...{RESET}")
subprocess.call(["python", "manage.py", "makemigrations"])

subprocess.call(["python", "manage.py", "migrate"])
print(f"{GREEN}Migraciones aplicadas exitosamente!{RESET}")

# print(f"{BLUE}Recopilando archivos estáticos...{RESET}")
# subprocess.call(["python", "manage.py", "collectstatic", "--noinput"])
# print(f"{GREEN}Archivos estáticos recopilados exitosamente!{RESET}")
subprocess.call(["python", "manage.py", "crear_usuarios"])
subprocess.call(["python", "manage.py", "crear_planes"])
subprocess.call(["python", "manage.py", "crear_planificadores"])
subprocess.call(["python", "manage.py", "crear_sesiones_tareas"])

# Verificar si DEBUG está en True para iniciar con Gunicorn
subprocess.call(["gunicorn", "core.wsgi", "--bind", "0.0.0.0:8000", "--reload"])
# if settings.DEBUG:
#     print(f"{BLUE}Iniciando la aplicación Django con Gunicorn...{RESET}")
#     subprocess.call(["gunicorn", "app.core.wsgi", "--bind", "0.0.0.0:8001", "--reload"])
# else:
#     print(f"{BLUE}Iniciando la aplicación Django con el servidor de desarrollo...{RESET}")
#     execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8001"])

print(f"{RED}Terminando proceso de la aplicación.{RESET}")