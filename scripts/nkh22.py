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
from goodies.util import *

from datetime import date


d0 = date(2018,4,1)
d1 = date(2018,12,31)

datetoday = date(2019,7,28)
year = 2018

nkkont  = Konto.objects.get(kurz = 'H22.EK.ER.NK')
nkkonto = Konto.objects.get(kurz = 'H22.EK.NK2018')


DK = Konto.objects.get(kurz = 'H22.EK.A.NK.DK')
VS = Konto.objects.get(kurz = 'H22.EK.A.NK.VS')
ML = Konto.objects.get(kurz = 'H22.EK.A.NK.ML')
GT = Konto.objects.get(kurz = 'H22.EK.A.NK.GARTEN')
KW = Konto.objects.get(kurz = 'H22.EK.A.NK.KW')
HZ = Konto.objects.get(kurz = 'H22.EK.A.NK.HZ')
GS = Konto.objects.get(kurz = 'H22.EK.A.NK.GS')

lok = [VS, DK, ML, GT, GS, KW, HZ]

kuerzel = { k : k.kurz.split('.')[-1] for k in lok}

# mieter konten
PETER  = Konto.objects.get(kurz = 'H22.F.Peter')
HOLGER = Konto.objects.get(kurz = 'H22.F.Holger')
ROEDER = Konto.objects.get(kurz = 'H22.F.Roeder')

mieter =  [PETER, HOLGER, ROEDER]

kuerzel.update( 
    { k : k.kurz.split('.')[-1] for k in mieter} 
)

name = {
    PETER : 'PETER',
    HOLGER : 'HOLGER',
    ROEDER : 'ROEDER'
}

anrede = {
    PETER : 'Lieber Papi',
    HOLGER : 'Lieber Holger',
    ROEDER : 'Sehr geehrter Herr Roder'
}

dein = {
    PETER : 'dein',
    HOLGER : 'dein',
    ROEDER : 'Ihr'
}

signature = {
    PETER : 'Kuss, \n\n \\bigskip \\bigskip \n \n Dein Matthias \n\n <matthias.holschneider@gmail.com>',
    HOLGER : 'alles Gute aus Berlin, \n\n \\bigskip \\bigskip \n \n Matthias \n\n <matthias.holschneider@gmail.com>',
    ROEDER : 'mfG\n\n \\bigskip \\bigskip \n \n  Matthias Holschneider \n\n <matthias.holschneider@gmail.com>'    
}

# Schluessel der NKs
key = {
    DK : 'qm',
    VS : 'qm',
    ML : 'pz',
    GT : 'pz',
    HZ : 'hz',
    GS : 'gs',
    KW : 'kw' 
}

# gesamtkosten (handisch or aggregate)
zvkosten = {
    DK : 15738,
    VS : 85299,
    ML : 18276,
    GT : 135000,
}

# direkt abgerechnete Kosten
# einzelposten werden eingegragen
dkonto = {
    'hz' : HZ,
    'kw' : KW,
    'gs' : GS
}

# Schluessel und direkte kosten
keys = {
    'qm' : {
        PETER  : 325,
        HOLGER : 385,
        ROEDER : 286,
    },
    'pz' : {
        PETER  : 24,
        HOLGER : 24,
        ROEDER : 12,
    },
    'hz' : {
        PETER  :  74960,
        HOLGER :  50261,
        ROEDER  : 33072
    },
    'kw' : {
        PETER  : 46381,
        HOLGER : 45892,
        ROEDER  : 10257
    },
    'gs' : {
        PETER  : 14895,
        HOLGER : 24912,
        ROEDER : 14013 
    },
}


# gefordertenk
gefnk  = {
    PETER   : 9*22000,
    HOLGER  : 9*20000,
    ROEDER  : 9*14000
}

vertnk = {
    m : {
        k : 0
        for k in lok
    }
    for m in mieter
}

def verteile_nk():
    for ko in lok:
        k = key[ko]
        for m in mieter:
            if k in dkonto:
                tot = keys[k][m]
            else:
                tot = zvkosten[ko]*keys[k][m] / sum(keys[k][mm] for mm in mieter )
                tot = np.round(tot)
            
            vertnk[m][ko] = tot
        
        #if k in dkonto:
        #    tot = sum( keys[k][m] for m in mieter)
        #else:
        #    tot = zvkosten[ko]

def verteile_in_db():    
    for ko in lok:
        k = key[ko]
        
        tot = sum( vertnk[m][ko] for m in mieter)
        b = Buchung()
        b.buchungsnummer = 'to come'
        b.datum = datetoday
        b.beschreibung = 'verrechung {0}'.format(kuerzel[ko])
        b.sollkonto = nkkonto
        b.habenkonto = ko
        b.beleg = '#NK_{0}_{1}'.format(year,kuerzel[ko])
        b.wert = tot
        b.save()
            
        for m in mieter:
            tot = vertnk[m][ko]
            
            b = Buchung()
            b.buchungsnummer = 'to come'
            b.datum = datetoday
            b.beschreibung = 'verrechung {0}'.format(kuerzel[ko])
            b.sollkonto = nkkonto
            b.habenkonto = nkkonto
            b.beleg = '#NK_{0}_{1}_{2}'.format(year,kuerzel[ko],kuerzel[m])
            b.wert = tot
            b.save()
    
    for m in mieter:
        b = Buchung()
        b.buchungsnummer = 'to come'
        b.datum = datetoday
        b.beschreibung = 'geforderte Pauschale'
        b.sollkonto = nkkont
        b.habenkonto = nkkonto
        b.beleg = '#NK_{0}'.format(year)
        b.wert = gefnk[m]
        b.save()

    
    
    for m in mieter:
        bk = sum (vertnk[m][ko] for ko in lok) # berechnete kosten
        gk = gefnk[m]
        
        if bk == gk:
            continue
        b = Buchung()
        b.buchungsnummer = 'to come'
        b.datum = datetoday
        b.beschreibung = 'verrechung {0}'.format(kuerzel[ko])
        if bk > gk:
            b.sollkonto = m
            b.habenkonto = nkkonto
        else:
            b.sollkonto = nkkonto
            b.habenkonto = m
            
        b.beleg = '#NKAUSG_{0}_{1}'.format(year,kuerzel[m])
        b.wert = abs(bk-gk)
        b.save()

def make_letter():
    
    totnk = sum( sum ( vertnk[mm][kk] for kk in lok) for mm in mieter)
            
    for m in mieter:
        anteil = sum ( vertnk[m][kk] for kk in lok)
        geznk  = gefnk[m]
        qm     = keys['qm'][m]
        pz     = keys['pz'][m]
        if anteil > geznk:
            esbesteht = 'eine Nachforderung'
        else:
            esbesteht = 'ein Guthaben'
        
        kontoreport = get_TeX_report(m, d1=date(2018,1,1), d2=date(2019,7,29), withbeleg=False)
        
        report = r"""
            \begin{longtable}{|l | r | r| r | r |}
            \hline
            {\bf Kosten} & {\bf Haus} & {\bf Anteil} & {\bf Schl. Art} & {\bf Schl. Wert}  \\
            \hline
            \hline
        """
        for kk in lok:
            totko = sum ( vertnk[mm][kk] for mm in mieter)
            report += """
        {0} & {1:.2f} & {2:.2f} &{3} &{4} \\\\
        """.format(kk.lang, totko/100, vertnk[m][kk]/100, key[kk], keys[key[kk]][m])
        
        report += r"""
        \hline
        \end{longtable}
        """
        context = {
            'liebermieter' : anrede[m],
            'heute'        : "{0}".format(datetoday),
            'periode'      : "{0} bis {1}".format(d0,d1),
            'totalnk'      : "{:.2f}".format(totnk/100),
            'anteil'       : "{:.2f}".format(anteil/100),
            'geznk'        : "{:.2f}".format(geznk/100),
            'esbesteht'    : esbesteht, 
            'nachf'        : "{:.2f}".format(abs(geznk-anteil)/100),
            'qm'           : qm,
            'pz'           : pz,
            'tabnk'        : report,
            'kontoreport'  : kontoreport,
            'mfg'          : signature[m]
        }
        texresult = render_to_string(template_name='TeX/nk.tex', context=context)
        texresult = texresult \
               .replace('&amp;', '&')  \
               .replace('&lt;', '$<$') \
               .replace('&gt;', '$>$')
        
        with open('nk-{0}-{1}.tex'.format(year, kuerzel[m]), 'w') as f:
            f.write(texresult)

def transfer_gef_nk():
    for m in mieter:
        b = Buchung()
        b.buchungsnummer = 'to come'
        b.datum = datetoday
        b.beschreibung = 'geforderte Pauschale'
        b.sollkonto = nkkont
        b.habenkonto = nkkonto
        b.beleg = 'NK_{0}'.format(year)
        b.wert = gefnk[m]
        b.save()

if __name__ == '__main__':
    verteile_nk()
    #verteile_in_db()
    make_letter()