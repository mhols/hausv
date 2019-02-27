'''
Created on 15.10.2018

@author: hols
'''
from booking.models import Konto, Buchung,generate_buchung,NK
from datetime import date
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print (os.sys.argv)
#prefix='L3'
#prefix=os.sys.argv[-2]
workfile=os.sys.argv[-1]

def run(*args):
    print('we are up and runing working on %s'%(workfile))
    
    f = open(workfile, 'r', encoding='utf-8')
    alle = f.readlines()
    prefix = alle[0][1:-1]
    f.close()
    #for H in Haus.objects.all():
    #    H.delete()

    
    #for nk in NK.objects.all():
    #    nk.delete()
    
    for B in Buchung.objects.filter(sollkonto__kurz__regex=r"^%s"%(prefix,)).all():
        print ("deleting %s"%(B,))
        B.delete()
    
    for K in Konto.objects.filter(kurz__regex=r"^%s"%(prefix,)).all():
        print ("deleting %s"%(K))
        K.delete()

    f = open(os.path.join(BASE_DIR, 'exports-db/h22-2018-11-05b.txt'), 'r', encoding='latin-1')
    #f = open(os.path.join(BASE_DIR, 'exports-db/L3-2018-11-19-exp.txt'), 'r', encoding='utf-8')
    #f = open(os.path.join(BASE_DIR, 'exports-db/AIYCB-2018-11-20.txt'), 'r', encoding='utf-8')
    
    

    for n, b in enumerate(alle):
        try:
            art, kurz, lang = b.split(":")
            art = Konto.invartdic[art]
            Konto.create(art, kurz, lang)
        except:
            try:
                generate_buchung(b)
            except Exception as ex:
                print( "problem  with line:", n, ex, " text = ", b)
    
