'''
Created on Oct 28, 2018

@author: hols
'''
import numpy as np

from booking.models import NK, Konto, Buchung, distribute, compute_sums,\
    generate_buchung
generate_buchung
    
from datetime import date

def run():
    year = 2018
    nktag = "#Nebenkkosten-%d#"%year
    beztag = "#Rueckb.Pausch-%d#"%year
    
    
    for b in Buchung.objects.filter(beschreibung__contains="#").all():
        b.delete()
    
    for nk in NK.objects.all():
        nk.delete()
    
    nk = NK(nk = Konto.objects.get(kurz='NK.VS'), key = NK.QM); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.GARTEN'), key = NK.PZ); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.KW'), key = NK.PZ); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.ML'), key = NK.PZ); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.DK'), key = NK.PZ); nk.save()
    nkhz = NK(nk = Konto.objects.get(kurz='NK.HZ'), key = NK.IN); nkhz.save()
    
    #nk = NK(nk = Konto.objects.get(kurz='NK.HZ'), key = NK.IN); nk.save()
    
    
    period = (date(year-1,4,1), date(year,3,31))
    
    knk = {}
    mtrkonto = ['F.Holger', 'F.Peter', 'F.Roeder']
    totf = [ 12*20000, 12*22000, 12*14000]      # totale Forderung NK in periode
    knk['qm'] = [90.61, 90.61, 62.89]
    knk['pz'] = [2,2,1]
    knk['in'] = [1,1,1]
    
    res = distribute(period, NK.objects.all(), knk)
    
    hzg = [299683, np.array([84814, 142394, 72475])]
    res[nkhz] = hzg
    
    
    
    """
    saldo 582654
    
    4.1. 200 holger
    2.1. 220 peter
    2.1. -585.69 SV-Geb 
    
    2.1. 140 roeder
    2.1. -21.00 Badenova
    2.1. -74.00
    3.1. 70 einlage alex
    
    15.1 190.00 davon 40 Verwaltung / Rabe
    
    
    
    30.1. -21.00 Badenova
    30.1. -74.00 Bnetze
    31.1. -155 Gas
    """
    
    
    sumnk = compute_sums(res)
    for i, mtr in enumerate(mtrkonto):
        f, nmtr = mtr.split('.')
        for nk in res.keys():
            booking = "%s : NK : %s : %d : %s : None"\
                %(period[1], nk.nk.kurz, res[nk][1][i], nktag+nmtr)
            generate_buchung(booking)
        booking = "%s :  %s : NK : %d : %s : None"\
                %(period[1], mtr, sumnk[i], nktag+nmtr)
        generate_buchung(booking)
        
        booking = "%s : %s : ER : %d : %s : None"\
                %(period[1], mtr, -totf[i], beztag+nmtr)
        generate_buchung(booking)
        print(booking)
