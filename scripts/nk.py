'''
Created on Oct 28, 2018

@author: hols
'''

from booking.models import NK, Konto, distribute
    
from datetime import date

def run():
    for nk in NK.objects.all():
        nk.delete()
    
    nk = NK(nk = Konto.objects.get(kurz='NK.VS'), key = NK.QM); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.GARTEN'), key = NK.PZ); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.KW'), key = NK.PZ); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.ML'), key = NK.PZ); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.HZ'), key = NK.IN); nk.save()
    
    #nk = NK(nk = Konto.objects.get(kurz='NK.HZ'), key = NK.IN); nk.save()
    
    knk = {}
    mtr = ['Holger', 'Peter', 'Roeder']
    knk['qm'] = [104.0, 102.3, 96.9]
    knk['pz'] = [2,2,1]
    knk['in'] = [1,1,1]
    
    period = (date(2017,4,1), date(2018,3,31))
    res = distribute(period, NK.objects.all(), knk)
    
    res[nk] = [986789, [99999, 32221, 34322]]
    
    print (res)
    