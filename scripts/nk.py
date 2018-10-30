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
    nktag = "Nebenkkosten-%d"%year
    
    
    for b in Buchung.objects.filter(beschreibung__contains=nktag).all():
        b.delete()
    
    for nk in NK.objects.all():
        nk.delete()
    
    nk = NK(nk = Konto.objects.get(kurz='NK.VS'), key = NK.QM); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.GARTEN'), key = NK.PZ); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.KW'), key = NK.PZ); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.ML'), key = NK.PZ); nk.save()
    nkhz = NK(nk = Konto.objects.get(kurz='NK.HZ'), key = NK.IN); nkhz.save()
    
    #nk = NK(nk = Konto.objects.get(kurz='NK.HZ'), key = NK.IN); nk.save()
    
    
    period = (date(year-1,4,1), date(year,3,31))
    
    knk = {}
    mtrkonto = ['F.Holger', 'F.Peter', 'F.Roeder']
    knk['qm'] = [104.0, 102.3, 96.9]
    knk['pz'] = [2,2,1]
    knk['in'] = [1,1,1]
    
    res = distribute(period, NK.objects.all(), knk)
    
    hzg = [89898, np.array([99999, 32221, 34322])]
    res[nkhz] = hzg
    
    sumnk = compute_sums(res)
    for i, mtr in enumerate(mtrkonto):
        f, nmtr = mtr.split('.')
        nmtr = "#"+nmtr
        for nk in res.keys():
        
            booking = "%s : NK : %s : %d : %s : None"\
                %(period[1], nk.nk.kurz, res[nk][1][i], nktag+nmtr)
    
            print (booking)
            generate_buchung(booking)
        booking = "%s :  %s : NK : %d : %s : None"\
                %(period[1], mtr, sumnk[i], nktag+nmtr)
        generate_buchung(booking)
        print(booking)
