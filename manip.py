import os
import django
from django import db
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

site = 'HV.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", site)
django.setup()
from booking.models import *
from goodies.util import *

from datetime import date

for b in Buchung.objects.filter(datum__lt=date(2018,1,1)).all():
	b.delete()

	


