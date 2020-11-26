import os
import django
from django import db
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

site = 'HV.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", site)
django.setup()
from booking.models import *
from goodies.util import *
from hv.models import *

from datetime import date

for mf in MonthlyForderung.objects.all():
    for y in [2017, 2018, 2019, 2020]:
        for m in range (1,13):
            d = date(y, m, 1)
            try:
                b = Buchung.objects.get(
                    datum=d,
                    wert=mf.betrag,
                    sollkonto=mf.mfkonto,
                    habenkonto=mf.gegenk
                )
                if mf.datum1 > d or mf.datum2 < d:
                    b.delete()
            except Exception as ex:
                print(mf, d, ex)

