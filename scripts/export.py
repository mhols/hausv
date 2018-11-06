'''
Created on Oct 26, 2018

@author: hols
'''


from booking.models import Haus, Konto, Buchung, generate_buchung
from datetime import date


H = Haus.objects.get(kurz = 'H22')

def run():
    
    print ("# generating map for "+H.kurz)
    
    print (H.kurz)
    
    res = ""
    
    for k in H.konten.all():
        res += "%s\n"%str(k)
    
    res += "\n------------------\n"
    for b in Buchung.objects.order_by('datum').all():
        res += "%s"%str(b)
    print (res)
