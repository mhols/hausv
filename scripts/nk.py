'''
Created on Oct 28, 2018

@author: hols
'''
import numpy as np

from booking.models import NK, Konto, Buchung, distribute, compute_sums,\
    generate_buchung
generate_buchung

from django.db.models import Sum

from datetime import date

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
