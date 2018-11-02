'''
Created on Oct 26, 2018

@author: hols
'''


from booking.models import Konto, Buchung, generate_buchung
from datetime import date


def run():
    
    res = ""
    for b in Buchung.objects.order_by('datum').all():
        res += "%s\n"%str(b)
    print (res)