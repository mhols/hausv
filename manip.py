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

for y in [2018, 2019]:
	for m in range(1,13):
		dd = date( y, m, 1)
		for w, k in zip([22000, 20000, 14000], [ 'Peter', 'Holger', 'Roeder']):
			kk = Konto.objects.get(kurz='H22.F.'+k)
			knk = Konto.objects.get(kurz='H22.EK.ER.NK')
			
			b = Buchung()
			b.datum = dd
			b.sollkonto = kk
			b.habenkonto = knk
			b.wert = w
			b.beschreibung = 'Nebenkosten Pauschale '+ k
			try:
				b.save()
			except:
				pass
			
		for w, k in zip([14000, 7000], [ 'Peter', 'Alex']):
			kk = Konto.objects.get(kurz='H22.F.'+k)
			knk = Konto.objects.get(kurz='H22.EK.'+k)
			
			b = Buchung()
			b.datum = dd
			b.sollkonto = kk
			b.habenkonto = knk
			b.wert = w
			b.beschreibung = 'Hausgeld Pauschale '+ k
			try:
				b.save()
			except:
				pass
		for w, k in zip([4000,], [ 'Peter',]):
			kk = Konto.objects.get(kurz='H22.F.'+k)
			knk = Konto.objects.get(kurz='H22.EK.A.VERW')
			
			b = Buchung()
			b.datum = dd
			b.sollkonto = knk
			b.habenkonto = kk
			b.wert = w
			b.beschreibung = 'Verwaltungs Pauschale '+ k
			try:
				b.save()
			except:
				pass