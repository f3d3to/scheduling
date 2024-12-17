"""
Módulo para comprobar la disponibilidad de bases de datos PostgreSQL y MSSQL.

Este módulo proporciona funciones para esperar y verificar la disponibilidad de bases de datos PostgreSQL y MSSQL.

Incluye:
    wait_for_databases: Espera la disponibilidad de las bases de datos configuradas en Django.
    wait_for_db: Espera la disponibilidad de una base de datos específica.
    wait_for_postgres: Espera la disponibilidad de una base de datos PostgreSQL.
    wait_for_mssql: Espera la disponibilidad de una base de datos MSSQL.
"""
# Python
from time import sleep
# Third party
import psycopg2
# Django
from django.conf import settings

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def wait_for_databases():
    """Espera la disponibilidad de las bases de datos configuradas en Django."""
    wait_for_db('default', 'PostgreSQL')

def wait_for_db(db_alias, db_type):
    db_settings = settings.DATABASES[db_alias]
    db_engine = db_settings['ENGINE']

    if 'postgresql' in db_engine:
        wait_for_postgres(db_settings, db_type)
    else:
        print(f"{RED}ERROR {RESET}")

def wait_for_postgres(db_settings, db_type, max_attempts=10):
    db_host = db_settings['HOST']
    db_port = db_settings['PORT']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    db_name = db_settings['NAME']

    attempts = 0
    connected = False

    while attempts < max_attempts and not connected:
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                dbname=db_name
            )
            conn.close()
            connected = True
        except psycopg2.OperationalError:
            attempts += 1
            if attempts == max_attempts:
                print(f"{RED}No se pudo establecer conexión con la base de datos {db_type} después de {max_attempts} intentos.{RESET}")
            else:
                print(f"{BLUE}Esperando a que la base de datos {db_type} esté disponible... (Intento {attempts}) {RESET}")
                sleep(1)

    if connected:
        print(f"{GREEN}Conexión exitosa a la base de datos {db_type} {RESET}")