from django.db import models
from django.core.validators import int_list_validator
from django.db.models import Sum

from datetime import date
import numpy as np
# Create your models here.


class Konto(models.Model):

    aktiv_bestand = 'ab'
    passiv_bestand = 'pb'
    passiv_ertrag = 'pe'
    passiv_aufwand = 'pa'
    passiv_eigenk  = 'pk'
    passiv_eigenkmain = 'em'
    bilanzkonto = 'bk'
    arten = ((aktiv_bestand,'aktiv'), 
             (passiv_bestand,'passiv bestand'),
             (passiv_eigenkmain,'passiv eigenkapital hauptkonto'),
             (passiv_eigenk,'passiv eigenkapital'),
             (passiv_ertrag, 'passiv ertrag'), 
             (passiv_aufwand, 'passiv aufwand'),
             (bilanzkonto, 'bilanzkonto'))

    artendic = { a:b for a, b in arten}
    art = models.CharField(max_length=2, choices=arten, default=aktiv_bestand)
    
    kurz = models.CharField(max_length=20, unique=True)
    nice = models.CharField(max_length=30, default="")
    lang = models.TextField()
    
    #anfangssoll  = models.IntegerField(default=0)
    #anfangshaben = models.IntegerField(default=0)
    
    oberkonto = models.ForeignKey('Konto', null=True, on_delete = models.SET_NULL, related_name='unterkonten')
    #lastsaldo = models.OneToOneField('Saldo', null=True, on_delete = models.PROTECT, 
    #                                 related_name='last_saldo_of')


    @classmethod
    def create(cls, art,  kurz, lang):
        k = Konto(art=art,kurz=kurz,lang=lang)
        oberk = ".".join( kurz.split('.')[:-1])
        try:
            obk = Konto.objects.get(kurz=oberk)
            k.oberkonto = obk
        except:
            print (kurz + " does not seem to have an oberkonto")
        k.save()
        return k
    
    def nicename(self):
        if self.nice is "":
            return self.lang
        else:
            return self.nice
    def last_saldo(self): 
        s = self.salden.exclude(in_bilanz__isnull=True).latest('in_bilanz__datum')
        return s
    
    def is_active(self):
        return self.art == Konto.aktiv_bestand
    
    def is_passive(self):
        return not (self.is_active() or self.art == Konto.bilanzkonto)
    
    def is_bestand(self):
        return self.art == Konto.aktiv_bestand or \
               self.art == Konto.passiv_bestand or \
               self.art == Konto.passiv_eigenk 
    
    def is_eigenk(self):
        return (self.art == Konto.passiv_eigenk) | (self.art == Konto.passiv_eigenkmain)
    
    def is_eigenkmain(self):
        return self.art == Konto.passiv_eigenkmain
    
    def is_aufwand(self):
        return self.art == Konto.passiv_aufwand
    
    def is_ertrag(self):
        return self.art == Konto.passiv_ertrag

    def is_erfolg(self):
        return (self.is_aufwand() | self.is_ertrag())

    def is_bilanz(self):
        return self.art == Konto.bilanzkonto
    
    def level(self):
        count=0
        k = self
        while not (k.oberkonto is None):
            count += 1
            k = k.oberkonto
        return count
    
    def saldiere(self, dates = (date(2017,1,1), date(2017,12,31))):
        if self.is_bestand():
            sb = self.soll_buchungen.filter(datum__lte=dates[1])
            hb = self.haben_buchungen.filter(datum__lte=dates[1])
        else:
            sb = self.soll_buchungen.filter(datum__range=dates)
            hb = self.haben_buchungen.filter(datum__range=dates)
        
        soll  = sb.aggregate(Sum('wert'))['wert__sum']
        haben = hb.aggregate(Sum('wert'))['wert__sum']
    
        if soll==None:
            soll = 0
        if haben==None:
            haben=0
        return (soll, haben)
    
    def has_unterkonten(self):
        try:
            return len(self.unterkonten.all()) > 0
        except:
            return False
    
    def saldiere_incl_unterkonten(self, dates = ( date(2017,1,1), date(2017,12,31))):
        
        def _saldiere(konto, dates, los):
            
            los.append(konto.saldiere(dates))
            if konto.has_unterkonten():
                for k in konto.unterkonten.all():
                    _saldiere(k,dates, los)
        
        los = [ ]
        _saldiere(self, dates, los)
        
        soll, haben = 0,0
        for so, ha in los:
            soll += so
            haben += ha
        return soll, haben
    
    def get_soll_buchungen(self, period=(date(2017,1,1), date(2017,1,31))):
        return self.soll_buchungen.filter(datum__range=period)
    
    def get_haben_buchungen(self, period=(date(2017,1,1), date(2017,1,31))):
        return self.haben_buchungen.filter(datum__range=period)
    
    def get_all_sollbuchungen(self, period=(date(2017,1,1), date(2017,1,31))):
        
        
        def _get_bookings(konto, sbs, period):
            sbs.append( konto.soll_buchungen.filter(datum__range=period))
            for k in konto.unterkonten.all():
                _get_bookings(k, sbs, period)
        sbs = []
        _get_bookings(self, sbs, period)
        res = Buchung.objects.none()
        for b in sbs:
            res = res | b
        return res
    
    def get_all_habenbuchungen(self, period=(date(2017,1,1), date(2017,1,31))):
        
        
        def _get_bookings(konto, sbs, period):
            sbs.append( konto.haben_buchungen.filter(datum__range=period))
            for k in konto.unterkonten.all():
                _get_bookings(k, sbs, period)
        
        sbs = []
        _get_bookings(self, sbs, period)
        print (sbs)
        res = sbs[0]#Buchung.objects.none()
        for b in sbs:
            print (b)
            res = b | res
        return res
    
class Saldo(models.Model):
    
    konto = models.ForeignKey( Konto, 
                               related_name='salden', 
                               on_delete=models.PROTECT )
    
    in_bilanz = models.ForeignKey('Bilanz', on_delete=models.PROTECT, 
                                  null=True, related_name='salden')
    
    soll   = models.IntegerField()
    haben  = models.IntegerField()
    
    @classmethod
    def create(cls, konto, soll, haben):
        return cls(konto=konto, soll=soll, haben=haben)

    @classmethod
    def create_unsigned(cls, konto, wert):
        """
        wert may be positive or negative
        depending on its sign and the active passive nature
        of the konto it will be put into soll or haben
        """
        if wert >=0:
            if konto.is_active():
                return Saldo.create(konto, wert, 0)
            elif konto.is_passive():
                return Saldo.create(konto, 0, wert)
            else:
                raise Exception('Bilanz konto...')
        else:
            if konto.is_active():
                return Saldo.create(konto, 0, -wert)
            elif konto.is_passive():
                return Saldo.create(konto, -wert, 0)
            else:
                raise Exception('Bilanz konto...')

    @classmethod
    def create_signd(cls, konto, wert):
        if konto.is_active():
            return Saldo.create(konto, wert, 0)
        elif konto.is_passive():
            return Saldo.create(konto, 0, wert)
        else:
            raise Exception('Bilanz konto...')

    def wert(self):
        if self.konto.is_active():
            return self.soll-self.haben
        else:
            return self.haben-self.soll

    def abswert(self):
        """
        the signed value
        """
        return abs(self.haben-self.soll)
    
    def is_bilanz_active(self):
        return ( self.wert()>=0 and self.konto.is_active())

    def is_erfolg(self):
        return self.konto.is_erfolg()

    def is_eigenk(self):
        return self.konto.is_eigenk()
    
    def is_eigenkmain(self):
        return self.konto.is_eigenkmain()
    
    def is_bilanz_passive(self):
        return ( self.wert()>=0 and self.konto.is_passive()) \
                and ( not self.is_erfolg() ) \
                and ( not self.is_eigenk()) 

    def __str__(self):
        return "%s %d %d"%(self.konto.kurz, self.soll, self.haben)
    
class Buchung(models.Model):
    datum  = models.DateField()
    beschreibung = models.CharField(max_length=120)
    beleg = models.CharField(max_length=20)
    sollkonto   = models.ForeignKey(Konto, related_name='soll_buchungen', on_delete=models.PROTECT)
    habenkonto  = models.ForeignKey(Konto, related_name='haben_buchungen', on_delete=models.PROTECT)
    wert = models.IntegerField()

    @classmethod
    def create(cls, datum, sollkonto, habenkonto, wert, beschreibung, beleg):
        bchng = cls(datum=datum, beschreibung=beschreibung, beleg=beleg, sollkonto=sollkonto, habenkonto=habenkonto, wert=wert)
        # do something with the book
        return bchng
    
    def __str__(self):
        return "%s : %s : %s : %d : %s : %s" %(str(self.datum), self.sollkonto.kurz, self.habenkonto.kurz, self.wert, 
                                                   self.beschreibung, self.beleg)
    
    #class Meta:
    #    unique_together = ('datum', 'beschreibung', 'beleg', 'sollkonto', 'habenkonto', 'wert')

class NK(models.Model):

    QM = 'qm'
    PZ = 'pz'
    IN = 'in'
    dist = (
        ('qm', 'Flaeche X Zeit'), 
        ('pz', 'Personen X Zeit'),
        ('in', 'Individuel')
    )
    nk  =  models.ForeignKey(Konto, on_delete=models.PROTECT, null=True)
    key = models.CharField(max_length=2, choices=dist)


def distribute_keys(tot, keys):
    totk = float(sum(keys))
    res = [ int(k * tot / totk)  for k in keys ]
    res[-1] = tot - sum(res[:-1])

    return res

def distribute(period, nks, keys):
    """
    keys is associative array
    """
    res = {}
    sunk = np.zeros(len(keys))
    for nk in nks:
        tot = nk.nk.saldiere(period)
        tot = tot[0]-tot[1]
        li = distribute_keys(tot, keys[nk.key])
        res[nk] = [tot, np.array(li)]
    return res
    
def compute_sums(nk):
    
    anteil = {}
    sumnk = 0.0
    
    for i, li in enumerate(nk.keys()):
        sumnk += nk[li][1]

    return sumnk

class Bilanz(models.Model):
    """
    Bianz and GuV
    GuV is a view
    contains only a collection of links on salden at a specific instance 
    """
    kurz = models.CharField(max_length=20)
    datum = models.DateField()
    #salden = models.ManyToManyField ( Saldo, related_name='bilanzen')
   
    @classmethod
    def create(cls, datum, kurz, salden):
        B = Bilanz(datum=datum, kurz=kurz)
        B.save()
        for s in salden:
            s.in_bilanz=B
            s.save()
        return B 

    @classmethod
    def create_zero(cls, datum, kurz, konten):
        salden = []
        for k in konten:
            s = Saldo.create(k,0, 0)
            s.save()
            salden.append(s)
        return Bilanz.create(datum, kurz, salden)

    def activa(self):
        return [s for s in self.salden.all() if s.is_bilanz_active()]

    def passiva(self):
        return [s for s in self.salden.all() if s.is_bilanz_passive()]
    
    def eigenk(self):
        return [s for s in self.salden.all() if s.is_eigenk()]
    
    def eigenkmain(self):
        return [s for s in self.salden.all() if s.is_eigenkmain()][0]
    
    def erfolg(self):
        return [s for s in self.salden.all() if s.is_erfolg()]
    
    def bilanz_konto(self, konto):
        return self.salden.get(konto=konto)


    def __str__(self):
        
        res = "Aktiva:\n"
        for s in self.activa():
            res += "\t%10s\t%12.2f\n"%(s.konto.kurz, s.abswert()/100)
        res += "\nPassiva:\nEigenkapital/GuV:\n"
        
        for s in self.eigenk():
            res += "\t%10s\t%12.2f\n"%(s.konto.kurz, s.wert()/100)
        res += "Fremdkapital\n"
        for s in self.passiva():
            res += "\t%10s\t%12.2f\n"%(s.konto.kurz, s.abswert()/100)
        return res
        
def saldiere_buchungen(buchungen):
    """
    soll und haben aufsummiert nach konten geordnet
    """
    salden = {}
    for b in buchungen:
        if b.sollkonto in salden:
            salden[b.sollkonto][0] += b.wert
        else:
            salden[b.sollkonto] = [b.wert, 0]
        if b.habenkonto in salden:
            salden[b.habenkonto][1] += b.wert
        else:
            salden[b.habenkonto] = [0, b.wert]
    
    return salden

def summiere_salden(salden):
    soll = sum([s.soll for s in salden])
    haben = sum([s.haben for s in salden ])

    return soll, haben

def make_bilanz(ausgangsbilanz, buchungen, datum, name):
    """
    
    """
    sa  = saldiere_buchungen(buchungen)

    S = []
    
    SMain = None
    for s in ausgangsbilanz.salden.all():
        k = s.konto
        if k in sa:
            ss = Saldo.create(s.konto, s.soll + sa[k][0], s.haben + sa[k][1])
            ss.saldiere()
        else:
            ss = Saldo.create(s.konto, s.soll, s.haben)
            ss.save()
        S.append ( ss)
        if ss.is_eigenkmain():
            Smain = ss
        
    B = Bilanz.create(datum, name, S)
    aufert = summiere_salden( B.erfolg())
    Smain.soll += aufert[0]
    Smain.haben += aufert[1]
    Smain.saldiere()
    return B
        
def generate_buchung(buchungstext):
    
    #buchungstext = buchungstext.replace(' ','')
    #print ('line ', buchungstext)
    try:
        d, sk, hk, w, bsr, bel = buchungstext.split(':')
    except:
        raise Exception('could not split '+buchungstext)
    d, sk, hk, w, bel = [ s.replace(' ','') for s in [d, sk, hk, w, bel]]
    #d,m,y = d.split('.')
    y,m,d = d.split('-')
    d = date(int(y), int(m), int(d))
    try:
        sk = Konto.objects.get( kurz = sk)
    except:
        raise Exception( sk )
    try:
        hk = Konto.objects.get( kurz = hk)
    except:
        raise Exception( "---%s---"%(hk) )
    w=w.replace('.','')
    w = int( w )
    
    b = Buchung.create( d, sk, hk, w, bsr, bel )
    try:
        b.save()
    except Exception as ex:
        raise Exception('could not save ' + str(b) + str(ex))
