'''
Created on 15.10.2018

@author: hols
'''
from booking.models import Konto, Buchung, Bilanz, Saldo, generate_buchung,\
    make_bilanz, saldiere_buchungen
from datetime import date

def run():
    print('we are up and runing')
    
    
    for B in Buchung.objects.all():
        B.delete()
    
    for S in Saldo.objects.all():
        S.delete()
    
    for K in Konto.objects.all():
        K.delete()
    
    # Kontenplan
    
    Kontenplan = [
        Konto.create(art=Konto.bilanzkonto,  kurz='BILANZ',    lang='Bilanzkonto'), 
        Konto.create(art=Konto.aktiv_bestand,  kurz='B',         lang='Deutsche Bank Konto'), 
        Konto.create(art=Konto.aktiv_bestand,  kurz='F',         lang='Forderungen'),
        Konto.create(art=Konto.aktiv_bestand,  kurz='F.Holger',  lang='NK Forderungen Holger'),
        Konto.create(art=Konto.aktiv_bestand,  kurz='F.Roeder',  lang='NK Forderungen Roeder'),
        Konto.create(art=Konto.aktiv_bestand,  kurz='F.Peter',   lang='NK Forderungen Peter'),
        Konto.create(art=Konto.passiv_eigenkmain, kurz='EK',     lang='Gesellschafter Kapital'),
        Konto.create(art=Konto.passiv_eigenk, kurz='EK.Peter',   lang='Gesellschafter Konto Peter'),
        Konto.create(art=Konto.passiv_eigenk, kurz='EK.Alex',    lang='Gesellschafter Konto Alex'),
        Konto.create(art=Konto.passiv_bestand, kurz='V',         lang='Verbindlichkeiten'),
        Konto.create(art=Konto.passiv_bestand, kurz='V.H',       lang='Verpflichtungen Handwerker'),
        Konto.create(art=Konto.passiv_bestand, kurz='V.H.Kadel', lang='Verbindl Handwerker Kadel'),
        Konto.create(art=Konto.passiv_ertrag,  kurz='ER',        lang='Allgemeines Gegenkonto fuer Ertraege'),
        Konto.create(art=Konto.passiv_aufwand, kurz='RE',        lang='Instandhaltung, Reparaturen'),
        Konto.create(art=Konto.passiv_aufwand, kurz='RE.UG',     lang='Instandhaltung, Reparaturen UG'),
        Konto.create(art=Konto.passiv_aufwand, kurz='RE.1OG',    lang='Instandhaltung, Reparaturen 1OG'),
        Konto.create(art=Konto.passiv_aufwand, kurz='RE.2OG',    lang='Instandhaltung, Reparaturen 2OG'),
        Konto.create(art=Konto.passiv_aufwand, kurz='VERW',      lang='Verwaltungskosten'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK',        lang='Nebenkosten'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.GS',     lang='Grundsteuer'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.VS',     lang='Versicherungen'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.ML',     lang='Hausmuell'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.KW',     lang='Kaltwasser'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.HZ',     lang='Heizung'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.HZ.FL',  lang='Feuerloescher'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.HZ.GAS', lang='Gasverbrauch'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.HZ.WART',lang='Wartung HZ'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.HZ.KAMIN',lang='Kaminfeger'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.HZ.STR', lang='Heizstom'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.HZ.ABR', lang='Abrechnungsservice'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.STR',    lang='Hausstrom'),        
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.GARTEN', lang='Gartenarbeiten'),
        Konto.create(art=Konto.passiv_aufwand, kurz='NK.TECHEM', lang='Abrechnung NK'),
    ]
    for K in Kontenplan:
        try:
            K.save()
        except:
            print('ooops')
    
    # Anfangsbilanz
    Anfangsbilanz = {'B' :  558585, 'EK' : 558585}
    
    Anfangssalden = []
    for K in Kontenplan:
        if not (K.art == Konto.bilanzkonto):
            if K.kurz in Anfangsbilanz:
                S = Saldo.create_unsigned(K, Anfangsbilanz[K.kurz])
            else:
                S = Saldo.create_unsigned(K, 0)
            S.save()
            Anfangssalden.append(S)
    
    Banfang = Bilanz.create( date(2018,1,1), 'H22-2018', Anfangssalden )
    
    
    
    print (Banfang)
    
    
    
    Buchungen = [
" 30.1.2018 : B : BILANZ : 558585 : Anfangsbilanz: None ",        
" 30.1.2018 : BILANZ : EK : 558585 : Anfangsbilanz: None ",        
" 1.1.2018 : NK.ML : EK.Peter : 13400 : Muell Gebuehren gezahlt von Peter: None ",        
" 1.10.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
" 1.10.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
" 1.10.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
" 1.10.2018 : NK.HZ.STR : B : 1800 : Badenova : None ",
" 1.10.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
" 1.2.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
" 1.2.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
" 1.3.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
" 1.3.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
" 1.3.2018 : NK.HZ.WART : V.H.Kadel : 72060 : Handwerker Kadel: None ",
" 1.3.2018 : V.H.Kadel : B : 72060 : Handwerker Kadel: None ",
" 1.6.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
" 1.6.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
" 1.8.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
" 1.8.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
" 10.4.2018 : B : NK.HZ.STR : 1742 : Badenova : None ",
" 15.2.2018 : NK.GARTEN : B : 15000 : Rabe Garten bezahlt von Peter: None ",
" 15.2.2018 : VERW : B : 4000 : Verwalung Peter: None ",
" 15.3.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
" 15.3.2018 : VERW : B : 4000 : Verwalung Peter: None ",
" 15.5.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
" 15.5.2018 : VERW : B : 4000 : Verwalung Peter: None ",
" 15.6.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
" 15.6.2018 : VERW : B : 4000 : Verwalung Peter: None ",
" 15.8.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
" 15.8.2018 : VERW : B : 4000 : Verwalung Peter: None ",
" 16.4.2018 : B : NK.HZ.GAS  : 7055 : Stadtwerke Waldkirch Gas (erst.): None ",
" 16.4.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
" 16.4.2018 : VERW : B : 4000 : Verwalung Peter: None ",
" 16.7.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
" 16.7.2018 : VERW : B : 4000 : Verwalung Peter: None ",
" 17.4.2018 : NK.HZ.ABR : B : 33092 : Abrechnungsservice: None ",
" 17.9.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
" 17.9.2018 : NK.VS : B : 7057 : Helvetia Versicherung: None ",
" 17.9.2018 : VERW : B : 4000 : Verwalung Peter: None ",
" 2.10.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
" 2.2.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
" 2.3.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
" 2.5.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
" 2.5.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
" 2.7.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
" 2.7.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
" 2.7.2018 : NK.HZ.STR : B : 1800 : Badenova : None ",
" 2.7.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
" 2.8.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
" 25.9.2018 : NK.HZ.KAMIN : B : 5512 : Kaminfeger: None ",
" 25.9.2018 : NK.VS : B : 19673 : Alte Leipziger : None ",
" 26.3.2018 : VERW : B : 9 : Konto Fuehrung SMS TAN : None ",
" 26.4.2018 : NK.KW : B : 6064 : Kaltwasser bnNETZE: None ",
" 28.2.2018 : NK.HZ.GAS : B : 15500 : Stadtwerke Waldkirch Gas: None ",
" 28.2.2018 : NK.HZ.STR : B : 2100 : Badenova : None ",
" 28.2.2018 : NK.KW : B : 7400 : Kaltwasser bnNETZE: None ",
" 28.9.2018 : VERW : B : 2547 : Konto Fuehrung : None ",
" 29.3.2018 : NK.HZ.GAS : B : 15500 : Stadtwerke Waldkirch Gas: None ",
" 29.3.2018 : VERW : B : 2397 : Konto Fuehrung : None ",
" 29.6.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
" 29.6.2018 : VERW : B : 2397 : Konto Fuehrung : None ",
" 3.4.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
" 3.4.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
" 3.5.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
" 3.7.2018 : B : EK : 9 : STORNO : None ",
" 3.7.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
" 3.9.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
" 3.9.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
" 30.1.2018 : NK.HZ.STR : B : 2100 : Badenova : None ",
" 30.1.2018 : NK.KW : B : 7400 : Kaltwasser bnNETZE: None ",
" 30.4.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
" 30.4.2018 : NK.HZ.STR : B : 1800 : Badenova : None ",
" 30.4.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
" 30.5.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
" 30.5.2018 : NK.HZ.STR : B : 1800 : Badenova : None ",
" 30.5.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
" 30.7.2018 : NK.HZ.STR : B : 1800 : Badenova : None ",
" 30.7.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
" 30.8.2018 : NK.HZ.STR : B : 1800 : Badenova: None ",
" 30.8.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
" 31.1.2018 : NK.HZ.GAS : B : 15500 : Stadtwerke Waldkirch Gas: None ",
" 31.7.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
" 31.8.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
" 4.10.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
" 4.4.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
" 4.4.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
" 4.5.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
" 4.6.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
" 4.6.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
" 4.7.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
" 4.9.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
" 4.9.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
" 5.2.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
" 5.3.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
" 6.8.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
"1.1.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
"1.1.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
"1.1.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
"1.2.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
"1.2.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
"1.2.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
"1.3.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
"1.3.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
"1.3.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
"1.4.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
"1.4.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
"1.4.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
"1.5.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
"1.5.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
"1.5.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
"1.6.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
"1.6.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
"1.6.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
"1.7.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
"1.7.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
"1.7.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
"1.8.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
"1.8.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
"1.8.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
"1.9.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
"1.9.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
"1.9.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
]

    for b in Buchungen:
        generate_buchung(b)
        
    Bende = make_bilanz(Banfang, Buchung.objects.all(), date(2018,12,31), 'H22-2019')


    
    print (Bende)
    