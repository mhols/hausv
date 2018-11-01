'''
Created on Oct 26, 2018

@author: hols
'''

from booking.models import Konto, Buchung, Bilanz, Saldo, generate_buchung,\
    make_bilanz, saldiere_buchungen
from datetime import date

oneday = date(2018,2,2)-date(2018,2,1)

def run():
    
    d0 = date(2017,1,1)
    B = Konto.objects.get(kurz='B')
    for d in [date(2018,10,4)]:
        salden = saldiere_buchungen(Buchung.objects.filter(datum__range=(d0,d)))
        print ( d,  salden[B][0]-salden[B][1] )
582654
558585
if __name__ == '__main__':
    pass