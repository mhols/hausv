'''
Created on Nov 5, 2018

@author: hols
'''

from datetime import date
import os


parserules = {
"DE94100500006600046463" : [("" ,"B : EK : Steuer")],
"DE24600400710510439300" : [("" ,"B : V.WR : Kredit Wuestenrot")],
"DE77660908000013724352" : [("" ,"B : F.MALLMANN : Miet und NK")],
"DE58670505050063027618" : [("" ,"B : EK.A.H.KADEL : Kadel")],
"DE38500700100093778901" : [("" ,"B : EK.A.NK.VER : Zuerich Versicherung")],
"DE18500500000025192030" : [("" ,"B : EK.A.NK.VER : SV-Gebaeude")],
"DE92680501010010106468" : [("" ,"B : EK.A.H.HERDEL : Herdel")],
"DE51680501013205197966" : [("" ,"B : EK.KAU : Sparkassenbuch 3205197966")],
"DE94680501010021000405" : [("" ,"B : EK.A.NK.HZ.GAS : Gasrechnung")],
""                       : [("BAR" ,"B : EK.MATTHIAS : Barentnahme"),
                            (""    ,"B : EK.A.VER : Verwaltung")] ,
"DE02100500009000481705" : [("" ,"B : EK.MATTHIAS : Privatentnahme")],
"DE51680900000038226908" : [("" ,"B : EK.A.H : Elektro Schmidt")],
"DE41660501010009124900" : [("" ,"B : EK.A.VER : Online Mietvertraege")],
"DE43120800004084300300" : [("" ,"B : EK.MATTHIAS : Privatentnahme (DB)")],
"DE89680501010002010029" : [("" ,"B : EK.A.NK.STR : Strom Badenova")],
"DE97500500000003200029" : [("" ,"B : EK.A.NK.VER : Feuer Versicherung")],
"DE93500105175423163373" : [("" ,"B : F.HARGESHEIMER : Miet und NK Hargesheimer")], 
"DE48680501010012648175" : [("" ,"B : EK.A.H.SOREX : Sorex")], 
"DE94310108337125580820" : [("" ,"B : F.LAMIN : Garage Lamin")],
"DE75200411440614992600" : [("" ,"B : F.SIMMINGER : Miete und NK Simminger")],
"DE86680501010002147435" : [("" ,"B : EK.A.H.RUTTKOWSKI : DACHDECKER")],
"DE08680501010012163313" : [("" ,"B : EK.A.H.DITTRICH : Schornsteinfeger")],
"DE59680400070160055000" : [("" ,"B : EK.A.NK.STR : BADENOVA SONDERRECHNUNG")],
"DE96680700300013254800" : [("" ,"B : EK.MATTHIAS : Papi BAR einzahlung")],
"DE66680900000038114409" : [("" ,"B : F.NUERNBERG : Miete und NK Victoria Nuernberg")],
"DE03200907002535050071" : [("" ,"B : EK.MATTHIAS : Privatentnahme")],
"DE35600908000104668412" : [("" ,"B : F.BARZ : Miete und NK Barz")],    
"DE50130700000450400708" : [("" ,"B : EK.MATTHIAS : Pivat NETTO")],
"DE92604200002080452635" : [("" ,"B : V.WR : Kredit Wuestenrot")],
"DE63680501010002010012" : [("" ,"B : EK.A.NK.GS : Grundsteuer")],
"DE74600600000455500100" : [("" ,"B : V.WR : Kredit Wuestenrot")],
"DE02680642220000309508" : [("" ,"B : F.BRAENDLE : Miet und NK")],
"DE23680501010013337519" : [("" ,"B : EK.A.NK.WA : Wasser bnNetze")],
"DE97680800300400803000" : [("" ,"B : F.NEMETS : Miet und Nebenkosten")],
"DE43680501013205198013" : [("" ,"B : EK.KAU : Kautionsanlage")],
"DE16604200002073982939" : [("" ,"B : V.WR : Sondertilgung")],
"DE87680501013205197997" : [("" ,"B : EK.KAU : Kaution")],
"DE21680700240268962800" : [("" ,"B : F.SCHMIDT : Miete und NK")],
"DE50680501010012809062" : [("" ,"B : EK.A.NK.GARTEN : Rabe")],
"DE45664500501004370233" : [("" ,"B : F.HARGESHEIMER : Miete und NK")],
"DE34120300001009351063" : [("" ,"B : F.MINGIRULLI : NK Ausgleich")],
"DE80500105175414995625" : [("" ,"B : F.KIEFER : Miete und NK")],
"DE87700100800183070800" : [("" ,"B : F.HAIMERL : Miete und NK")],
"3204853050"             : [("" ,"B : EK.KAU : Kautionskonto")],
"DE36620500000010173422" : [("" ,"B : F.KUERTI : Miete")],
"DE44500700100961353001" : [("" ,"B : EK.MATTHIAS : Herold LV")],
"DE16500400000582454500" : [("" ,"B : EK.A.NK.HZ.ABR : Techem Ablese Service")],
"DE94673900000086317109" : [("" ,"B : F.SELBACH : Miete und NK Selbach")],
"DE92660908000003724352" : [("" ,"B : F.MALLMANN : Miete und NK Mallmann")],
"DE53600501010001366705" : [("200000435392CRED" , "B : WR : Bausparvertrag"), 
                            ("220000077620CRED" , "B : V.WR : Kredit Tilgung und Zins")],
"DE80680501010002077024" : [("" ,"B : EK.A.H.KADEL : Kadel")],
"DE88690500010024799991" : [("" ,"B : F.ADELHEIM : Miete und NK Adelheim")],
"DE76680900000002829800" : [("" ,"B : EK.A.H.KADEL : Kadel")],
"DE77100500009000481713" : [("" ,"B : EK.MATTHIAS : Bar Abhebung Berlin")],
}

def date_to_str(d):
    #return "%d.%d.%d"%(d.day, d.month, d.year)
    return "%d-%d-%d"%(d.year, d.month, d.day)

def booking( d, soll, haben, wert, beschreibung, beleg='None' ):
    if wert > 0:
        b = "%s : %s : %s : %d : %s : %s"%(date_to_str(d), soll, haben, wert, beschreibung, beleg)
    else:
        b = "%s : %s : %s : %d : %s : %s"%(date_to_str(d), haben, soll, -wert, beschreibung, beleg)
    
    return b

def parse_line(l):
    """
"12045802";"02.01.15";"02.01.15";
"GUTSCHRIFT";"SVWZ+rent";"DEREK MICHIO AOKI";
"DE14680501010013449328";"FRSPDE66XXX";"380,00";"EUR";"Umsatz gebucht"

"12045802";"01.09.16";"30.08.16";"ENTGELTABSCHLUSS";
"Entgeltabrechnung siehe Anlage ";
"";
"";
"";
"";
"";
"";
"";
"0000000000";
"68050101";"-7,20";"EUR";"Umsatz gebucht"
    """
    try:
        Auftragskonto, Buchungstag, Valutadatum, \
        Buchungstext, Verwendungszweck, Beguenstigter, \
        Kontonummer, BLZ, Betrag, \
        Waehrung, Info = l.split(';')

        #IBAN, d1, d2, text, info, ref, IBAN2, BIC, wert, waehrung, comment = l.split(';')
    except:
        raise Exception('\ncould not split\n'+l)
    d,m,y = Valutadatum[1:-1].split(".")
    d1 = date( 2000 + int(y), int(m), int(d))
    IBAN = Kontonummer[1:-1]
    a,b = Betrag[1:-1].split(",")
    wert2 = int(Betrag[1:-1].replace(',','').replace('.',''))
    #print (b)
    #print (wert, wert2)
    ref = Buchungstext[1:-1]
    return IBAN, d1, ref, wert2, Verwendungszweck, l

# generating list of parsable distincs lines
lines = []
for f in os.listdir(os.getcwd()):
    f = open(f,'r',encoding='windows-1252') #'utf-8')
    for l in f.readlines():
        #print(l)
        #l = l.encode('iso-8859-1').decode('utf-8')
        try:
            parse_line(l)
        except BaseException as ex:
            #print (ex, l)
            continue
        if not l in lines:
            lines.append(l)

#print (lines)
# uniqueness based on a key
lines2=[]
keys = []
for l in lines:
    try:
        ll = parse_line(l)
    except:
        print ('problem ', ll)
        continue
    key = date_to_str(ll[1])+" " + ll[0]+ " " +str(ll[3]) + " " + str(ll[4])
    if (ll[1]>=date(2017,1,1)):
        if not (key in keys):
            lines2.append(l)
            keys.append(key)
            
su = 0

bookings = []

book_OK  = open('bookings.txt', 'w', encoding='UTF-8')
problems = open('problems.txt', 'w', encoding='UTF-8')

for l in lines2:
    IBAN, datum, ref, wert, vwzk, l = parse_line(l)
    su += wert
    found = False
    for key, sht in parserules[IBAN]:
        if key in l:
            soll, haben, text = sht.split(":")
            found = True
            break # at first match
    if not found:
        problems.write('no parsing found:' + IBAN + '\n')
        continue
    soll = "L3."+soll.replace(' ','')
    haben = 'L3.'+haben.replace(' ','')
    beschreibung=text + " " + ref
    beleg = l[:-1]
    b = booking( datum, soll, haben, wert, beschreibung, beleg )
    if b in bookings:
        problems.write('double booking found ' + b)
    bookings.append(b)

    book_OK.write(b+'\n')

book_OK.close()
problems.close()
print (su)
