'''
Created on Oct 28, 2018

@author: hols
'''
import numpy as np

from booking.models import NK, Konto, distribute, compute_sums
    
from datetime import date
from zope.component.tests.examples import comp

def run():
    for nk in NK.objects.all():
        nk.delete()
    
    nk = NK(nk = Konto.objects.get(kurz='NK.VS'), key = NK.QM); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.GARTEN'), key = NK.PZ); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.KW'), key = NK.PZ); nk.save()
    nk = NK(nk = Konto.objects.get(kurz='NK.ML'), key = NK.PZ); nk.save()
    nkhz = NK(nk = Konto.objects.get(kurz='NK.HZ'), key = NK.IN); nkhz.save()
    
    #nk = NK(nk = Konto.objects.get(kurz='NK.HZ'), key = NK.IN); nk.save()
    
    period = (date(2017,4,1), date(2018,3,31))
    
    knk = {}
    mtrkonto = ['F.Holger', 'F.Peter', 'F.Roeder']
    knk['qm'] = [104.0, 102.3, 96.9]
    knk['pz'] = [2,2,1]
    knk['in'] = [1,1,1]
    
    res = distribute(period, NK.objects.all(), knk)
    
    hzg = np.array([99999, 32221, 34322])
    res[nkhz] = hzg
    
    sumnk, summt, anteil = compute_sums(res)
    for nk in res.keys():
        
        booking = "%s : "
    
    print (res, anteil)
    