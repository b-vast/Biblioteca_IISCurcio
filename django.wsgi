import os, sys

DJANGO_ROOT = os.getenv('DJANGO_ROOT')
paths = [DJANGO_ROOT,
         DJANGO_ROOT+"/Biblioteca_IISCurcio"]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_ROOT'] = DJANGO_ROOT
os.environ['DJANGO_SETTINGS_MODULE'] = 'Biblioteca_IISCurcio.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

