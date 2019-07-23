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

kb = Konto.objects.get(kurz='L3.B')

kurz = 'BONK'
kk = Konto.objects.get(kurz='L3.F.{0}'.format(kurz))
for i in range(5,13):
	d = date(2019,i,1)
	mf = Buchung()
	mf.datum = d
	mf.sollkonto = kk
	mf.habenkonto = Konto.objects.get(kurz='L3.EK.ER.MIETE')
	mf.sollkonto  = kk
	mf.beschreibung = 'Mietforderung {0}'.format(kurz)
	mf.beleg = 'None'
	mf.wert = 31000
	mf.save()
	
	mf = Buchung()
	mf.datum = d
	mf.sollkonto = kk
	mf.habenkonto = Konto.objects.get(kurz='L3.EK.ER.NK')
	mf.sollkonto  = kk
	mf.beschreibung = 'Nebenkosten Pauschale {0}'.format(kurz)
	mf.beleg = 'None'
	mf.wert = 6000
	mf.save()
	