"""
WSGI config for sescca project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sescca.settings')

application = get_wsgi_application()
# sys.path.append('/home/pi/sescca/sescca_web/sescca')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'sescca.settings'

# os.environ.setdefault("LANG", "en_US.UTF-8")
# os.environ.setdefault("LC_ALL", "en_US.UTF-8")

# activate_this = '/home/pi/django/sescca/bin/activate_this.py'
# exec(open(activate_this).read())

#application = get_wsgi_application()
