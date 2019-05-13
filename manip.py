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



for b in Buchung.objects.filter(habenkonto__kurz__startswith='H22', datum__gte=date(2018,1,30)).all():
	b.delete()
for b in Buchung.objects.filter(sollkonto__kurz__startswith='H22', datum__gte=date(2018,1,30)).all():
	b.delete()


for r in RawUmsatz.objects.all():
	r.delete()

