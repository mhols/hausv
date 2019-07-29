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
        PETER  : 124,
        HOLGER : 124,
        ROEDER :  78
    },
    'pz' : {
        PETER  : 24,
        HOLGER : 36,
        ROEDER : 12
    },
    'hz' : {
        PETER  : 74960,
        HOLGER : 50261,
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
            totko = sum ( vertnk[m][kk] for mm in mieter)
            report += """
        {0} & {1:.2f} & {2:.2f} &{3} &{4} \\\\
        """.format(kk.lang, totko/100, vertnk[m][kk]/100, key[kk], keys[key[kk]][m])
        
        report += r"""
        \hline
        \end{longtable}
        """
        context = {
            'liebermieter' : anrede[m],
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
        
def run():
    year = 2017
    d1, d2 = date(year,1,1), date(year,12,31)
        
    mieter = {}
    mieter['UG'] = ['NEMETS']
    mieter['EG'] = ['ADELHEIM', 'NUERNBERG', 'HAIMERL',
                    'SELBACH', 'KIEFER']
    mieter['1OGL'] = ['SIMMINGER', 'HARGESHEIMER']
    mieter['1OGR'] = ['SCHMIDT']
    mieter['2OG'] = ['BARZ']
    
    MES = mieter.keys()
    
    TECHEM = {}
    TECHEM['UG'] = 79652
    TECHEM['EG'] = 177804
    TECHEM['1OGR'] = 23495
    TECHEM['1OGL'] = 112863
    TECHEM['2OG'] =  73687
    
    BZ = {
        'NEMETS' : 1,
        'KIEFER' : 1,
        'ADELHEIM': 1,
        'NUERNBERG' : 1,
        'HAIMERL' : 2,
        'SELBACH' : 1,
        'SCHMIDT' : 1,
        'SIMMINGER' : 2,
        'HARGESHEIMER' :  2,
        'BARZ' : 1
    }
    
    
    NK = ['DK', 'GS', 'VER', 'WA', 'STR', 'GARTEN']
    NKSQM = ['DK', 'GS', 'VER', 'GARTEN']
    NKSPZ = ['WA', 'STR']
    
    NKS = {
        n : Buchung.objects.filter(sollkonto__kurz='L3.EK.A.NK.%s'%(n))
          .filter(datum__range=(d1,d2)).aggregate(Sum('wert'))['wert__sum'] for n in NK
    }


    Monate={}
    Monate['NEMETS'] = 12
    Monate['KIEFER'] = 10
    Monate['ADELHEIM'] = 12
    Monate['NUERNBERG'] = 12
    Monate['HAIMERL'] = 2
    Monate['SELBACH'] = 12
    Monate['SCHMIDT'] = 12
    Monate['SIMMINGER'] = 2*9
    Monate['HARGESHEIMER'] = 2*3
    Monate['BARZ']=2*12
    SMT = sum([Monate[k] for k in Monate])
    
    mieterlist = Monate.keys()
    
    wohnungofmieter = { mt : next( wg for wg in mieter if mt in mieter[wg]) for  mt in mieterlist}
    
    QM = {}
    QM['UG'] = 38.29
    QM['EG'] = 132.95
    QM['1OGL'] = 96.58
    QM['1OGR'] = 36.37
    QM['2OG'] = 105.31
    SQM = sum([QM[k] for k in QM])
        
    MM={}
    MM['UG'] = 12
    MM['EG'] = 48
    MM['1OGL'] = 24
    MM['1OGR'] = 12
    MM['2OG'] = 24
   
    SMM = sum([MM[k] for k in MM])
    
    nkverteilung = {}
    for mt in mieterlist:
        nkverteilung[mt] = {}
        for nk in NKSPZ:
            nkverteilung[mt][nk] = NKS[nk]*Monate[mt] / float(SMT)
    
    nkverteilungme = {}
    for me in QM:
        nkverteilungme[me] = {}
        for nk in NKSQM:
            try:
                nkverteilungme[me][nk] = NKS[nk]*QM[me] / float(SQM)
            except:
                print( me, nk, SQM)
    
    for mt in mieterlist:
        for nk in NKSQM:
            nkverteilung[mt][nk] = 0
    for me in QM:
        for mt in mieter[me]:
            for nk in NKSQM:
                try:
                    nkverteilung[mt][nk] += nkverteilungme[me][nk] * float(Monate[mt]) / MM[me]
                except:
                    print( mt, nk, me)
    for mt in mieterlist:
        nkverteilung[mt]['TECHEM'] = 0
    for me in QM:
        for mt in mieter[me]:
            nkverteilung[mt]['TECHEM'] += TECHEM[me] * float(Monate[mt]) / MM[me]

    for mt in nkverteilung:
        print (mt, nkverteilung[mt])


    zuZahlendeNK = {mt : sum ([nkverteilung[mt][nk] for nk in nkverteilung[mt]]) for mt in mieterlist}
    
        
    alteForderungNK =  {
        mt : Buchung.objects
            .filter(datum__range=(d1,d2))
            .filter(sollkonto__kurz='L3.F.%s'%(mt))
            .filter(beschreibung__contains='Nebenkostenforderung')
            .aggregate(Sum('wert'))['wert__sum'] 
            for mt in mieterlist
        }
    
    print ('\n\n')
    
    for mt in zuZahlendeNK:
        print (mt, int(zuZahlendeNK[mt])/100)
    
    print ('\n\n')
    
    for mt in zuZahlendeNK:
        print (mt, int(alteForderungNK[mt])/100)
    
    print ('\n\n')
    
    for mt in zuZahlendeNK:
        try:
            print (mt, int(zuZahlendeNK[mt] - alteForderungNK[mt])/100)
        except:
            pass


    ANREDE = {
        'NEMETS' : 'Sehr geehrte Frau Nemets',
        'KIEFER' : 'Sehr geehrte Frau Kiefer',
        'ADELHEIM' : 'Sehr geehrte Frau Adelheim',
        'NUERNBERG' : 'Sehr geehrte Frau Nuernberg',
        'HAIMERL' : 'Sehr geehrte Frau Haimerl',
        'SELBACH' : 'Sehr geehrte Frau Selbach',
        'SCHMIDT' : 'Sehr geehrter Herr Dr. Schmidt',
        'SIMMINGER' : 'Sehr geehrte Frau Simminger',
        'HARGESHEIMER' : 'Sehr geehrte Frau Hargesheimer',
        'BARZ'    : "Sehr geehrte Frau Barz"    
    }


    def forderung_guthaben(n):
        if n >0 :
            return "eine Forderung von\n\n{\\bf $\mathbf %8.2f$ Euro}\n\nIch bitte um zeitnahen Ausgleich."%(n/100)
        else:
            return "ein Guthaben von\n\n{\\bf $\mathbf %8.2f$ Euro}\n\nIch bitte um Angabe der Bankverbindung."%(-n/100)
        
    for mt in mieterlist:
        text=r"""
\documentclass[english,10pt]{g-brief}
\usepackage[T1]{fontenc}
\usepackage[latin2]{inputenc}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Textclass specific LaTeX commands.
\newcommand{\LyxGruss}[1]{\Gruss{#1}{0.5cm}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% User specified LaTeX commands.
\lochermarke
\faltmarken
\fenstermarken
\trennlinien

\usepackage[english]{babel}

\begin{document}

\Name{Prof. Dr. Matthias Holschneider}
\Unterschrift{Matthias Holschneider}
\Strasse{Gieseler Stra{\ss}e 28}
\Zusatz{}
\Ort{10713 Berlin}
\Land{}
\RetourAdresse{Prof. Dr. M. Holschneider, Gieseler Str. 28, 10713 Berlin}
\Telefon{+49 175 1515 574}
\Telefax{+49 331 977 1578}
\Telex{}
\EMail{matthias.holschneider@gmail.com }
\HTTP{www.math.uni-potsdam.de/\textasciitilde{}hols}
\Bank{Sparkasse Freiburg}
\BLZ{680 501 01}
\Konto{12045802}


\Adresse{ %s\\Lerchenstrasse 3\\79104 Freiburg }
\Betreff{Nebenkosten 2017}
\Postvermerk{}
\MeinZeichen{}
\IhrZeichen{}
\IhrSchreiben{}
\Anlagen{Rechnung TECHEM}
\Verteiler{an alle Mieter}

\Datum{\today}


\Anrede{ %s, }

\LyxGruss{mit freundlichen Gr{\"u}{\ss}en aus Berlin,}
\begin{g-brief}

Hier die Nebenkosten Abrechnung f{\"u}r die Periode %s - %s.
In der Abrechnung ist eine Personenebelegung von %d Personen X Monaten 
zugrunde gelegt. Die Flaeche Ihrere Wohneinheit betraegt $%7.2fm^2$.
Die Pauschalforderung an Sie betrug $%8.2f$ Euro. Ihr Anteil 
an den Nebenkosten betraegt $%8.2f$ Euro. Es besteht somit %s



mfG

Matthias Holschneider
\vfill\eject

Tabelle der Nebenkosten

\begin{tabular}{l | c | r }
Kosten & Total & ihr Anteil \\
\hline
Grundsteuer & $%8.2f$ &$%8.2f$ \\
Versicherungen & $%8.2f$ &$%8.2f$ \\
Dachkaenel & $%8.2f$ &$%8.2f$ \\
Garten & $%8.2f$ &$%8.2f$ \\
Kaltwasser & $%8.2f$ &$%8.2f$ \\
Heizung & $%8.2f$ &$%8.2f$ \\
\hline
Summe & $%8.2f$ &$%8.2f$ \\
\end{tabular}

\end{g-brief}

\end{document}
"""%(mt, ANREDE[mt], str(d1), str(d2), Monate[mt], QM[wohnungofmieter[mt]],
     int(alteForderungNK[mt])/100, int(zuZahlendeNK[mt])/100,
    forderung_guthaben(int(zuZahlendeNK[mt]-alteForderungNK[mt])),
    NKS['GS']/100, nkverteilung[mt]['GS']/100,
    NKS['VER']/100, nkverteilung[mt]['VER']/100, 
    NKS['DK']/100, nkverteilung[mt]['DK']/100, 
    NKS['GARTEN']/100, nkverteilung[mt]['GARTEN']/100,
    NKS['WA']/100, nkverteilung[mt]['WA']/100, 
    sum( TECHEM[me] for me in TECHEM)/100, nkverteilung[mt]['TECHEM']/100,      
    sum([zuZahlendeNK[mt] for mt in mieterlist])/100, zuZahlendeNK[mt]/100           
                     )
    
        f = open(mt+'.tex','w')
        f.write(text)
        f.close()

        print ('2018-12-06 : L3.F.%s : L3.EK.ER.NK : %d : Ausgleich NK 2017 : None' %(mt, int(zuZahlendeNK[mt]-alteForderungNK[mt])))
           

if __name__ == '__main__':
    verteile_nk()
    #verteile_in_db()
    make_letter()
