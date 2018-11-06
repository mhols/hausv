'''
Created on 15.10.2018

@author: hols
'''
from booking.models import Konto, Haus, Buchung,generate_buchung,NK
from datetime import date
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def run():
    print('we are up and runing')

    for H in Haus.objects.all():
        H.delete()

    for nk in NK.objects.all():
        nk.delete()
    
    for B in Buchung.objects.all():
        B.delete()
    
    for K in Konto.objects.all():
        K.delete()
#     
#     # Kontenplan
# 
#     H = Haus()
#     H.kurz = 'H22'
#     H.save()
#     
#     Konto.create(art=Konto.bilanzkonto,  kurz='BILANZ',    lang='Bilanzkonto'), 
#     Konto.create(art=Konto.aktiv_bestand,  kurz='B',         lang='Deutsche Bank Konto'), 
#     Konto.create(art=Konto.aktiv_bestand,  kurz='F',         lang='Forderungen'),
#     Konto.create(art=Konto.aktiv_bestand,  kurz='F.Holger',  lang='Forderungen an Holger'),
#     Konto.create(art=Konto.aktiv_bestand,  kurz='F.Holger.NK',  lang='NK Forderungen an Holger'),
#     Konto.create(art=Konto.aktiv_bestand,  kurz='F.Holger.NK.A',  lang='Ausgleich NK Forderungen Holger'),
#     Konto.create(art=Konto.aktiv_bestand,  kurz='F.Roeder',  lang='Forderungen an Roeder'),
#     Konto.create(art=Konto.aktiv_bestand,  kurz='F.Roeder.NK',  lang='NK Forderungen an Roeder'),
#     Konto.create(art=Konto.aktiv_bestand,  kurz='F.Roeder.NK.A',  lang='Ausgleich NK Forderungen Roeder'),
#     Konto.create(art=Konto.aktiv_bestand,  kurz='F.Peter',   lang='Forderungen Peter'),
#     Konto.create(art=Konto.aktiv_bestand,  kurz='F.Peter.NK',   lang='NK Forderungen an Peter'),
#     Konto.create(art=Konto.aktiv_bestand,  kurz='F.Peter.NK.A',   lang='Ausgleich NK Forderungen Peter'),
#     Konto.create(art=Konto.passiv_eigenkmain, kurz='EK',     lang='Gesellschafter Kapital'),
#     Konto.create(art=Konto.passiv_eigenk, kurz='EK.Peter',   lang='Gesellschafter Konto Peter'),
#     Konto.create(art=Konto.passiv_eigenk, kurz='EK.Alex',    lang='Gesellschafter Konto Alex'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A',    lang='Aufwendungen'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.RE',        lang='Instandhaltung, Reparaturen'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.RE.UG',     lang='Instandhaltung, Reparaturen UG'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.RE.1OG',    lang='Instandhaltung, Reparaturen 1OG'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.RE.2OG',    lang='Instandhaltung, Reparaturen 2OG'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.VERW',      lang='Verwaltungskosten'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK',        lang='Nebenkosten'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.DK',     lang='Dachkanel Reinigung'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.GS',     lang='Grundsteuer'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.VS',     lang='Versicherungen'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.ML',     lang='Hausmuell'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.KW',     lang='Kaltwasser'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.WK',     lang='Reinigung Waschkueche'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.HZ',     lang='Heizung'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.HZ.FL',  lang='Feuerloescher'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.HZ.GAS', lang='Gasverbrauch'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.HZ.WART',lang='Wartung HZ'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.HZ.KAMIN',lang='Kaminfeger'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.HZ.STR', lang='Heizstom'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.HZ.ABR', lang='Abrechnungsservice'),
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.STR',    lang='Hausstrom'),        
#     Konto.create(art=Konto.passiv_aufwand, kurz='EK.A.NK.GARTEN', lang='Gartenarbeiten'),
#     Konto.create(art=Konto.passiv_ertrag,  kurz='EK.ER',        lang='Ertraege'),
#     Konto.create(art=Konto.passiv_ertrag,  kurz='EK.ER.VER',    lang='Versicherungs Entschaedigung'),
#     Konto.create(art=Konto.passiv_bestand, kurz='V',         lang='Verbindlichkeiten'),
#     Konto.create(art=Konto.passiv_bestand, kurz='V.H',       lang='Verbindlichkeiten Handwerker'),
#     Konto.create(art=Konto.passiv_bestand, kurz='V.H.Kadel', lang='Verbindl Handwerker Kadel'),
#     Konto.create(art=Konto.passiv_bestand, kurz='V.H.Schmid', lang='Verbindl Handwerker Schmid'),        
#     Konto.create(art=Konto.passiv_bestand, kurz='V.H.Ruttkowski', lang='Verbindl Handwerker Ruttkowski'),
#     
#     for K in Konto.objects.all():
#         K.haus = H
#         K.kurz = "H22.%s"%K.kurz
#         K.save()
    
#     [
# "1.1.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.1.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.1.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.2.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.2.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.2.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.3.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.3.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.3.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.4.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.4.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.4.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.5.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.5.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.5.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.6.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.6.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.6.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.7.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.7.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.7.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.8.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.8.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.8.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.9.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.9.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.9.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.10.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.10.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.10.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.11.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.11.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.11.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.12.2017 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.12.2017 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.12.2017 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# 
# " 1.1.2017 : B : BILANZ : 590677 : Anfangsbilanz: None ",
# " 1.1.2017 : BILANZ : EK :590677 : Anfangsbilanz: None ",
# " 29.12.2017 : VERW : B : 2397 : Kontofuehrung : None ",
# " 12.12.2017 : RE : V.H.Ruttkowski : 12281 : Dachkaenel : None ",
# " 12.12.2017 : NK.DK : RE : 12281 : Dachkaenel als NKs: None ",
# " 12.12.2017 : V.H.Ruttkowski : B : 12281 : bez. Rechnung Dachkaenel : None ",
# " 15.12.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 15.12.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 28.12.2017 : NK.HZ.GAS : B : 15500 : Gas Stadtwerke Waldkirch : None ",
# " 29.12.2017 : B : F : 373042 : Alte Leipziger Wasserschaden: None ",
# " 24.11.2017 : RE : B : 5474 : Handwerker Lerner : None ",
# " 30.11.2017 : NK.STR : B : 2100 : Hausstrom : None ",
# " 30.11.2017 : NK.KW : B : 7400 : Kaltwasser bNetze : None ",
# " 30.11.2017 : NK.HZ.GAS : B : 15500 : Gas Stadtwerke Waldkirch : None ",
# " 1.12.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 1.12.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 1.12.2017 : NK.VS : B : 9862 : Allianz Versicherung : None ",
# " 4.12.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 4.12.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 17.11.2017 : VERW : B : 400 : Kontofuehrung : None ",
# " 13.11.2017 : B : NK.VS : 19500 : Alte Leipziger : None ",
# " 14.11.2017 : RE : B : 13240 : EPRIMO Wasserschaden : None ",
# " 14.11.2017 : F  : ER.VER : 13240 : EPRIMO Wasserschaden : None ",
# " 15.11.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 15.11.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 17.11.2017 : RE : V.H.Schmid  : 126309 : Wasserschaden : None ",
# " 17.11.2017 : V.H.Schmid : B : 126309 : Wasserschaden: None ",
# " 17.11.2017 : F : ER.VER : 126309 : Schmid Wasserschaden F an ALTELEIPZIGER: None ",
# " 3.11.2017 : RE : B : 73950 : Wassersch. die Kueche: None ",
# " 3.11.2017 : F : ER.VER : 73950 : Wassersch. die Kueche F an ALTELEIPZIG: None ",
# " 6.11.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 30.10.2017 : NK.VS : B : 19500 : Alte Leipziger : None ",
# " 30.10.2017 : NK.VS : B : 19500 : Alte Leipziger II: None ",
# " 1.11.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 2.11.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 2.11.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 30.10.2017 : NK.STR : B : 2100 : Hausstrom : None ",
# " 30.10.2017 : NK.KW : B : 7400 : Kaltwasser bNetze : None ",
# " 30.10.2017 : NK.HZ.GAS : B : 15500 : Gas Stadtwerke Waldkirch : None ",
# " 25.10.2017 : RE : B : 88227 : Drytec Rep Wassersch: None ",
# " 25.10.2017 : F : ER.VER : 88227 : Drytec Rep Wassersch: None ",
# " 16.10.2017 : VERW : B : 4000 : Verwaltung II : None ",
# " 16.10.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 2.10.2017 : NK.STR : B : 2100 : Hausstrom : None ",
# " 2.10.2017 : NK.KW : B : 7400 : Kaltwasser bNetze : None ",
# " 3.10.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 4.10.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 29.9.2017 : VERW : B : 2397 : Kontofuehrung : None ",
# " 29.9.2017 : NK.HZ.GAS : B : 15500 : Gas Stadtwerke Waldkirch : None ",
# " 29.9.2017 : V.H.Kadel : B : 106916 :  Rechnung Kadel WASSERS: None ",
# " 29.9.2017 : RE : V.H.Kadel : 106916 : Bezahlung Rechnung Kadel WASSERS: None ",
# " 29.9.2017 : F : ER.VER : 106916 : Ford. Rueckerstattung Kadel WASSERS: None ",
# " 2.10.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 2.10.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 26.9.2017 : RE : V.H.Ruttkowski : 17993 : Dachkaenel : None ",
# " 26.9.2017 : NK.DK : RE : 17993 : Dachkaenel als NK : None ",
# " 26.9.2017 : V.H.Ruttkowski : B : 17993 : bez. Rechnung Dachkaenel : None ",
# " 27.9.2017 : NK.VS : B : 6415 : Helvetia Versicherung : None ",
# " 12.9.2017 : NK.GARTEN : B : 10500 : Buesche Vorgarten : None ",
# " 12.9.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 12.9.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 4.9.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 30.8.2017 : NK.KW : B : 7400 : Kaltwasser bNetze : None ",
# " 30.8.2017 : VERW : B : 3015 : Buerobedarf an Peter ueberwiesen : None ",
# " 30.8.2017 : EK : B  : 3200 : Grabpflege : None ",
# " 31.8.2017 : NK.HZ.GAS : B : 15500 : Gas Stadtwerke Waldkirch : None ",
# " 1.9.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 1.9.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 4.9.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 1.8.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 1.8.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 2.8.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 4.8.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 11.8.2017 : NK.HZ.FL : B : 3957 : Sorex Wartung : None ",
# " 15.8.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 15.8.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 30.8.2017 : NK.STR : B : 2100 : Hausstrom : None ",
# " 31.7.2017 : NK.STR : B : 2100 : Hausstrom : None ",
# " 31.7.2017 : NK.KW : B : 7400 : Kaltwasser bNetze : None ",
# " 31.7.2017 : NK.HZ.GAS : B : 15500 : Gas Stadtwerke Waldkirch : None ",
# " 17.7.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 17.7.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 4.7.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 3.7.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 3.7.2017 : B : F.Roeder : 20703 : Ausgleich NK Roeder : None ",
# " 3.7.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 3.7.2017 : EK.Peter : B : 2000 : Privatentname : None ",
# " 3.7.2017 : F.Holger : B : 52162 : Ausgleich NK Holger : None ",
# " 3.7.2017 : F.Peter : B : 54133 : Ausgleich NK Peter : None ",
# " 4.7.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 30.6.2017 : NK.STR : B : 2100 : Hausstrom : None ",
# " 30.6.2017 : NK.KW : B : 7400 : Kaltwasser bNetze : None ",
# " 30.6.2017 : NK.HZ.GAS : B : 15500 : Gas Stadtwerke Waldkirch : None ",
# " 30.6.2017 : VERW : B : 2397 : Kontofuehrung : None ",
# " 15.6.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 6.6.2017 : VERW : B : 7023 : Buero Peter : None ",
# " 6.6.2017 : EK :  B : 7827 : Grabpflege : None ",
# "8.6.2017 : F.Roeder : B : 16722 : Ausgleich NK Roeder : None", 
# " 15.6.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 6.6.2017 : F.Peter : B : 57394 : Ausgleich NK Peter : None ",
# " 1.6.2017 : B : F.Roeder: 14000 : bez NK Pauschale Roeder : None ",
# " 1.6.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 2.6.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 6.6.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 6.6.2017 : B : F.Holger : 25613 : Ausgleich NK Holger : None ",
# " 30.5.2017 : NK.STR : B : 2100 : Hausstrom : None ",
# " 30.5.2017 : NK.KW : B : 7400 : Kaltwasser bNetze : None ",
# " 31.5.2017 : NK.HZ.GAS : B : 15500 : Gas Stadtwerke Waldkirch : None ",
# " 15.5.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 15.5.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 10.5.2017 : NK.HZ.ABR : B : 1386 : Ablesung Ritter : None ",
# " 12.5.2017 : NK.VS : B : 704 : Alte Leipziger : None ",
# " 2.5.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 4.5.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 2.5.2017 : NK.STR : B : 7400 : Hausstrom : None ",
# " 3.5.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 29.4.2017 : NK.HZ.GAS : B : 15500 : Gas Stadtwerke Waldkirch : None ",
# " 2.5.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 2.5.2017 : NK.STR : B : 2100 : Hausstrom : None ",
# " 2.5.2017 : NK.KW : B : 6311 : Kaltwasser bNetze : None ",
# " 15.4.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 15.4.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 19.4.2017 : B : NK.STR : 882 : Hausstrom : None ",
# " 19.4.2017 : NK.HZ.ABR : B : 31592 : Ablesung Ritter : None ",
# " 27.4.2017 : NK.HZ.GAS : B : 10394 : Gas Stadtwerke Waldkirch : None ",
# " 4.4.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 4.4.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 3.4.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 3.4.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 3.4.2017 : V.H.Kadel : B : 46529 : Bezahlung Rechnung Kadel : None ",
# " 3.4.2017 : NK.HZ.WART : V.H.Kadel : 46529 : Wartung Heizung : None ",
# " 15.3.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 15.3.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 24.3.2017 : B : EK.Peter : 168000 : einlage Peter : None ",
# " 24.3.2017 : EK.Alex : B : 33598 : Wasserzaehler : None ",
# " 31.3.2017 : NK.HZ.GAS : B : 15000 : Gas Stadtwerke Waldkirch : None ",
# " 31.3.2017 : VERW : B : 2397 : Kontofuehrung : None ",
# " 1.3.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 2.3.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 2.3.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 6.3.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 28.2.2017 : NK.STR : B : 2300 : Hausstrom : None ",
# " 28.2.2017 : NK.KW : B : 6600 : Kaltwasser bNetze : None ",
# " 28.2.2017 : NK.HZ.GAS : B : 15000 : Gas Stadtwerke Waldkirch : None ",
# " 9.2.2017 : VERW : B : 5778 : Verwaltung : None ",
# " 9.2.2017 : EK : B : 5282 : Grab Mami : None ",
# " 15.2.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 15.2.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 5.2.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 31.1.2017 : NK.HZ.GAS : B : 15000 : Gas Stadtwerke Waldkirch : None ",
# " 1.2.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 2.2.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 2.2.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 16.1.2017 : VERW : B : 4000 : Verwaltung : None ",
# " 16.1.2017 : NK.GARTEN : B : 10520 : Gartenpflege : None ",
# " 30.1.2017 : NK.STR : B : 2300 : Hausstrom : None ",
# " 30.1.2017 : NK.KW : B : 6600 : Kaltwasser bNetze : None ",
# " 3.1.2017 : B : EK.Alex : 7000 : Einlage Alex : None ",
# " 3.1.2017 : B : F.Roeder : 14000 : bez NK Pauschale Roeder : None ",
# " 4.1.2017 : B : F.Holger : 20000 : Bezahlung NK Holger : None ",
# " 2.1.2017 : B : F.Peter : 22000 : bez NK Pauschale Peter : None ",
# " 2.1.2017 : NK.VS : B : 50061 : SV Gebaeude Versicherung : None ",
# 
# #
# " 1.3.2017 : F.Roeder : ER : 20703 : NK Ausgleich :  None ",
# " 1.8.2017 : ER : F.Roeder : 16722  : Rueckzahlung NK Ausgleich : None",
# " 1.3.2017 : ER : F.Holger :  52162 : NK Ausgleich : None",
# " 1.6.2017 : F.Holger : ER : 25613  : Rueckzahlung NK Ausgleich : None",
# " 1.3.2017  : ER : F.Peter : 54133 : NK Ausgleich : None",
# " 1.8.2017 : ER : F.Peter : 57394  : Rueckzahlung NK Ausgleich : None",
# #
# " 1.10.2018 : NK.ML : EK.Peter : 13400 : Muell Gebuehren gezahlt von Peter: None ",        
# " 1.1.2018 : NK.ML : EK.Peter : 13400 : Muell Gebuehren gezahlt von Peter: None ",        
# " 1.10.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
# " 1.10.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
# " 1.10.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
# " 1.10.2018 : NK.HZ.STR : B : 1800 : Badenova : None ",
# " 1.10.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
# " 1.2.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
# " 1.2.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
# " 1.3.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
# " 1.3.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
# " 1.3.2018 : NK.HZ.WART : V.H.Kadel : 72060 : Handwerker Kadel: None ",
# " 1.3.2018 : V.H.Kadel : B : 72060 : Handwerker Kadel: None ",
# " 1.6.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
# " 1.6.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
# " 1.8.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
# " 1.8.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
# " 10.4.2018 : B : NK.HZ.STR : 1742 : Badenova : None ",
# " 15.2.2018 : NK.GARTEN : B : 15000 : Rabe Garten bezahlt von Peter: None ",
# " 15.2.2018 : VERW : B : 4000 : Verwalung Peter: None ",
# " 15.3.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
# " 15.3.2018 : VERW : B : 4000 : Verwalung Peter: None ",
# " 15.5.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
# " 15.5.2018 : VERW : B : 4000 : Verwalung Peter: None ",
# " 15.6.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
# " 15.6.2018 : VERW : B : 4000 : Verwalung Peter: None ",
# " 15.8.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
# " 15.8.2018 : VERW : B : 4000 : Verwalung Peter: None ",
# " 16.4.2018 : B : NK.HZ.GAS  : 7055 : Stadtwerke Waldkirch Gas (erst.): None ",
# " 16.4.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
# " 16.4.2018 : VERW : B : 4000 : Verwalung Peter: None ",
# " 16.7.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
# " 16.7.2018 : VERW : B : 4000 : Verwalung Peter: None ",
# " 17.4.2018 : NK.HZ.ABR : B : 33092 : Abrechnungsservice: None ",
# " 17.9.2018 : NK.GARTEN : B : 15000 : Rabe Ladislav: None ",
# " 17.9.2018 : NK.VS : B : 7057 : Helvetia Versicherung: None ",
# " 17.9.2018 : VERW : B : 4000 : Verwalung Peter: None ",
# " 2.10.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
# " 2.2.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
# " 2.3.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
# " 2.5.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
# " 2.5.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
# " 2.7.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
# " 2.7.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
# " 2.7.2018 : NK.HZ.STR : B : 1800 : Badenova : None ",
# " 2.7.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
# " 2.8.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
# " 25.9.2018 : NK.HZ.KAMIN : B : 5512 : Kaminfeger: None ",
# " 25.9.2018 : NK.VS : B : 19673 : Alte Leipziger : None ",
# " 26.3.2018 : VERW : B : 9 : Konto Fuehrung SMS TAN : None ",
# " 26.4.2018 : NK.KW : B : 6064 : Kaltwasser bnNETZE: None ",
# " 28.2.2018 : NK.HZ.GAS : B : 15500 : Stadtwerke Waldkirch Gas: None ",
# " 28.2.2018 : NK.HZ.STR : B : 2100 : Badenova : None ",
# " 28.2.2018 : NK.KW : B : 7400 : Kaltwasser bnNETZE: None ",
# " 28.9.2018 : VERW : B : 2547 : Konto Fuehrung : None ",
# " 29.3.2018 : NK.HZ.GAS : B : 15500 : Stadtwerke Waldkirch Gas: None ",
# " 29.3.2018 : VERW : B : 2397 : Kontofuehrung : None ",
# " 29.6.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
# " 29.6.2018 : VERW : B : 2397 : Kontofuehrung : None ",
# " 3.4.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
# " 3.4.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
# " 3.5.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
# " 3.7.2018 : B : VERW : 9 : STORNO : None ",
# " 3.7.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
# " 3.9.2018 : B : F.Peter : 22000 : NK Voraus Peter: None ",
# " 3.9.2018 : B : F.Roeder : 14000 : NK Voraus Roeder: None ",
# " 30.1.2018 : NK.HZ.STR : B : 2100 : Badenova : None ",
# " 30.1.2018 : NK.KW : B : 7400 : Kaltwasser bnNETZE: None ",
# " 30.4.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
# " 30.4.2018 : NK.HZ.STR : B : 1800 : Badenova : None ",
# " 30.4.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
# " 30.5.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
# " 30.5.2018 : NK.HZ.STR : B : 1800 : Badenova : None ",
# " 30.5.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
# " 30.7.2018 : NK.HZ.STR : B : 1800 : Badenova : None ",
# " 30.7.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
# " 30.8.2018 : NK.HZ.STR : B : 1800 : Badenova: None ",
# " 30.8.2018 : NK.KW : B : 8200 : Kaltwasser bnNETZE: None ",
# " 31.1.2018 : NK.HZ.GAS : B : 15500 : Stadtwerke Waldkirch Gas: None ",
# " 31.7.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
# " 31.8.2018 : NK.HZ.GAS : B : 14200 : Stadtwerke Waldkirch Gas: None ",
# " 4.10.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
# " 4.4.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
# " 4.4.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
# " 4.5.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
# " 4.6.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
# " 4.6.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
# " 4.7.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
# " 4.9.2018 : B : EK.Alex : 7000 : EK Beitrag Alex: None ",
# " 4.9.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
# " 5.2.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
# " 5.3.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
# " 6.8.2018 : B : F.Holger : 20000 : Vorauszahlung NK Holger: None ",
# "1.1.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.1.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.1.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.2.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.2.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.2.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.3.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.3.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.3.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.4.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.4.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.4.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.5.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.5.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.5.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.6.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.6.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.6.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.7.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.7.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.7.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.8.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.8.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.8.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# "1.9.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",
# "1.9.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",
# "1.9.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",
# ]

    #f = open(os.path.join(BASE_DIR, 'exports-db/h22-2018-11-05b.txt'), 'r', encoding='latin-1')
    f = open(os.path.join(BASE_DIR, 'exports-db/L3-2018-11-06.txt'), 'r', encoding='latin-1')
    all = f.readlines()
    f.close()

    for n, b in enumerate(all):
        try:
            art, kurz, lang = b.split(":")
            art = Konto.invartdic[art]
            Konto.create(art, kurz, lang)
        except:
            try:
                generate_buchung(b)
            except:
                print( "problem  with line:", n, " text = ", b)
    