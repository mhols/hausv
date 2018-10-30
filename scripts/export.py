'''
Created on Oct 26, 2018

@author: hols
'''


from booking.models import Konto, Buchung, Bilanz, Saldo, generate_buchung,\
    make_bilanz, saldiere_buchungen
from datetime import date


def run():
    
    res = ""
    for b in Buchung.objects.order_by('datum').all():
        res += "%s\n"%str(b)
    print (res)