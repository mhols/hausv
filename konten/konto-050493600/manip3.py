'''
Created on Oct 19, 2018

@author: hols
'''

from datetime import date


def date_to_str(d):
    return "%d.%d.%d"%(d.day, d.month, d.year)
    #return "%d.%d.%d"%(d.year, d.month, d.day)

def booking( d, soll, haben, wert, beschreibung, beleg='None' ):
    if wert > 0:
        b = "%s : %s : %s : %d : %s : %s"%(date_to_str(d), soll, haben, wert, beschreibung, beleg)
    else:
        b = "%s : %s : %s : %d : %s : %s"%(date_to_str(d), haben, soll, -wert, beschreibung, beleg)
    
    return b


f = open('old-2017.csv', 'r', encoding='latin-1')

lines = f.readlines()
f.close()

map = {}

for l in lines:
    try:
        a,b,c,d,e = l.split(',')
        da,mo = a.split('-')
        da = date( 2017, int(mo), int(da))
        va = int(float(c)*100)
    except:
        continue
    
    if b=='Ruttkowski':
        bl = [
            booking(da, 'RE', 'V.H.Ruttkowski', -va, 'Dachkaenel'),
            booking(da, 'V.H.Ruttkowski', 'B', -va, 'bez. Rechnung Dachkaenel')
            ]
    elif b=='NKPETER':
        bl = booking(da, 'B', 'F.Peter', va, 'bez NK Pauschale Peter')
    elif b=='GRABPFLEGE':
        bl = booking(da, 'B', 'EK', -va, 'Grabpflege')
    elif b=='NKROEDER':
        bl = booking(da, 'F.Roeder', 'B', va, 'bez NK Pauschale Roeder')
    elif b=='BNETZE':
        bl = booking(da, 'NK.KW', 'B', -va, 'Kaltwasser bNetze')
    elif b=='GRABBUERO':
        bl = [ booking(da, "VERW", 'B', 2500, 'Verwaltung'),
              booking(da, "EK", 'B', -va-2500, 'Verwaltung')
            ]
    elif b=='DIEKUECHE':
        bl = booking(da, 'EK', 'B', -va, 'WASSERSCHADEN')
    elif b=='RITTER':
        bl = booking(da, 'NK.HZ.ABR', 'B', -va, 'Ablesung Ritter')
    elif b=='BADENOVA':
        bl = booking(da, 'NK.STR', 'B', -va, 'Hausstrom')
    elif b=='RABEVIAPETER':
        bl = booking(da, 'NK.GARTEN', 'B', -va, 'Hausstrom')
    elif b=='NKHOLGER':
        bl = booking(da, 'B', 'F.Holger', va, 'Bezahlung NK Holger')
    elif b=='KADEL':
        bl = [ booking(da, 'V.H.Kadel', 'B', -va, 'Bezahlung Rechnung Kadel'),
               booking(da, 'NK.HZ.WART', 'V.H.Kadel', -va, 'Wartung Heizung')]
    elif b=='VerwaltunRabe':
        bl = [ booking(da, 'VERW', 'B', 4000, 'Verwaltung'),
               booking(da, 'NK.GARTEN', 'B', -va-4000, 'Gartenpflege')]
    elif b=='ALTELEIPZIGER':
        bl = booking(da, 'NK.VS', 'B', -va, 'Alte Leipziger')
    elif b=='AUSGLNKHOLGER':
        bl = booking(da, 'F.Holger', 'B', -va, 'Ausgleich NK Holger')
    elif b=='EINLAGENALEX':
        bl = booking(da, 'B', 'EK.Alex', va, 'Einlage Alex')
    elif b=='ALLIANZ':
        bl = booking(da, 'NK.VS', 'B', -va, 'Allianz Versicherung')
    elif b=='AUSGLNKPETER':
        bl = booking(da, 'F.Peter', 'B', -va, 'Ausgleich NK Peter')
    elif b=='AUSGLNKROEDER':
        bl = booking(da, 'F.Roeder', 'B', -va, 'Ausgleich NK Roeder')
    elif b=='SOREXFEUERL':
        bl = booking(da, 'NK.HZ.FL', 'B', -va, 'Sorex Wartung')
    elif b=='SVGEBAEUDE':
        bl = booking(da, 'NK.VS', 'B', -va, 'SV Gebaeude Versicherung')
    elif b=='BARPRIVAT':
        bl = booking(da, 'EK.Peter', 'B', -va, 'Privatentname')
    elif b=='PlusKonto':
        bl = booking(da, 'VERW', 'B', -va, 'Kontofuehrung')
    elif b=='GEBUERNBANK':
        bl = booking(da, 'VERW', 'B', -va, 'Kontofuehrung')
    elif b == 'HELVETIA':
        bl = booking(da, 'NK.V', 'B', -va, 'Helvetia Versicherung')
    elif b == 'BUEROBEDVIAPETER':
        bl = booking(da, 'VERW', 'B', -va, 'Buerobedarf an Peter ueberwiesen')
    elif b == 'STADTWERKEWALDKIRCH':
        bl = booking(da, 'NK.HZ.GAS', 'B', -va, 'Gas Stadtwerke Waldkirch')
    elif b== 'EINLAGENPETER':
        bl = booking(da, 'B', 'E.Peter', va, 'einlage Peter')
    elif b == 'LERNER':
        bl = booking(da, 'RE', 'B', -va, 'Handwerker Lerner')
    elif b == 'EPRIMO':
        bl = booking(da, 'EK', 'B', -va, 'EPRIMO')
    elif b == 'WASSERZAEHLERVIAALEX':
        bl = booking(da, 'E.Alex', 'B', -va, 'Wasserzaehler')
    elif b == "DRYTEC":
        bl = booking(da, 'EK', 'B', -va, 'Drytec')
    elif b == "SCHMID":
        bl = booking(da, 'R', 'V.H.Schmid', -va, 'Rechnung Handwerker SCHMID')
        bl = booking(da, 'V.H.Schmid', 'B', -va, 'bez. Handwerker SCHMID')    
    else:
        print ('oooop s ', b)
        
    if type(bl) is str:
        bl = [bl]
    for b in bl:
        print ('"',b,'",')
        
    
for k in map.keys():
    
    print (k)
    
    for l in map[k]:
        print ('\t', l)

    
    
    