'''
Created on Oct 28, 2018

@author: hols
'''
import numpy as np
import os
import django
from django import db
from django.db.models import Sum
from django.template.loader import render_to_string
from django.shortcuts import render
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

site = 'HV.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", site)
django.setup()
from booking.models import *
from booking.views import get_TeX_report
from hv.models import *
from goodies.util import *

from datetime import date


haus = Haus.objects.get(kurz='H22')

d1 = date(2018, 4, 1)
d2 = date(2018, 12, 31)
datum_lb = date(2018, 12, 31)
datetoday = date(2020, 11, 1)
year = 2018

def make_letter():

    res = NebenKosten.distribute_all(haus, d1, d2)
    tex = NebenKosten.TeX_report_NK(haus, d1, d2)

    totnk = res['totnk']

    for m in res['mtrs']:
        anteil = res['sum_mtr'][m]
        geznk = m.get_nkf(d1, d2)
        qm = m.wohneinheit.qm
        pz = m.bz_days_in_period(d1, d2)

        if anteil > geznk:
            esbesteht = 'eine Nachforderung'
        else:
            esbesteht = 'ein Guthaben'

        nachf = geznk-anteil


        try:
            b = Buchung.objects.get(
                datum=d2,
                beschreibung="Ausgleich NK {} {}".format(d1.year, m.mieter.kurz)
            )
        except:
            b = Buchung (
                datum=d2,
                beschreibung="Ausgleich NK {} {}".format(d1.year, m.mieter.kurz
            ))
        if nachf > 0:
            b.habenkonto = m.fkonto
            b.sollkonto = Konto.objects.get(kurz='H22.EK.ER.NK')
        else:
            b.sollkonto = m.fkonto
            b.habenkonto = Konto.objects.get(kurz='H22.EK.ER.NK')
        b.wert = abs(nachf)
        b.save()

        noffen = m.fkonto.saldiere((date(2018,1,1), datum_lb))
        nachftot = noffen[0]-noffen[1]

        if (nachftot > 0):
            esbestehttot = 'eine Gesamtforderung'
        else:
            esbestehttot = 'ein Gesamtguthaben'

        kontoreport = get_TeX_report(m.fkonto, d1, d2)
        report = tex[m]

        context = {
            'liebermieter':     m.mieter.anrede,
            'heute':            "{0}".format(datetoday),
            'periode':          "{0} bis {1}".format(d1, d2),
            'totalnk':          "{:.2f}".format(totnk / 100),
            'anteil':           "{:.2f}".format(anteil / 100),
            'geznk':            "{:.2f}".format(geznk / 100),
            'esbesteht':        esbesteht,
            'nachf':            "{:.2f}".format(abs(nachf) / 100),
            'qm':               qm,
            'pz':               pz,
            'tabnk': report,
            'kontoreport': kontoreport,
            'mfg': m.mieter.mfg,
            'noffen': "{:.2f}".format(abs(nachftot)/100),
            'datum_lb': datum_lb,
            'esbestehttot': esbestehttot,
            'nachftot': "{:.2f}".format(abs(nachftot)/100),
        }


        texresult = render_to_string(template_name='TeX/nk.tex', context=context)
        texresult = texresult \
               .replace('&amp;', '&')  \
               .replace('&lt;', '$<$') \
               .replace('&gt;', '$>$')

        with open('nk-{0}-{1}.tex'.format(year, m.mieter.kurz), 'w') as f:
            f.write(texresult)
        os.system('pdflatex nk-{0}-{1}.tex'.format(year, m.mieter.kurz))

def transfer_gef_nk():
    for m in mieter:
        b = Buchung()
        b.buchungsnummer = 'to come'
        b.datum = d1
        b.beschreibung = 'geforderte Pauschale'
        b.sollkonto = nkkont
        b.habenkonto = nkkonto
        b.beleg = 'NK_{0}'.format(year)
        b.wert = gefnk[m]
        b.save()


def make_clean():
    os.system('rm *.aux *.log *.tex')

if __name__ == '__main__':
    # verteile_nk()
    # verteile_in_db()
    make_letter()
    make_clean()
