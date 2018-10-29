'''
Created on Oct 26, 2018

@author: hols
'''

from booking.models import Konto, Buchung, Bilanz, Saldo, generate_buchung,\
    make_bilanz, saldiere_buchungen
from datetime import date

oneday = date(2018,2,2)-date(2018,2,1)

def run():
    
    B = Konto.objects.get(kurz='B')
    for d in [date(2017,4,4), date(2017,5,15), date(2017,7,4), date(2017,9,4),
              date(2017,9,15), date(2017, 9,27), date(2017,10,6), 
              date(2017,10,27), date(2017,11,2), date(2017,11,6),
              date(2017,11,17), date(2017,11,21), date(2017,12,4),
              date(2017,12,6), date(2017,12,29)]:
        salden = saldiere_buchungen(Buchung.objects.filter(datum__lte=d))
        print ( d, salden[B][0]-salden[B][1] )

if __name__ == '__main__':
    pass