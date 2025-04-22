import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

# Establecer el entorno de configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "procesar_csv.settings")

# Ejecutar collectstatic automáticamente al inicio
call_command('collectstatic', '--noinput')

application = get_wsgi_application()
