from datetime import date

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

import django_tables2 as tables

from .models import Konto, Buchung

oneday = date(2000,1,2)-date(2000,1,1)

def date_to_str(da):
    def pretty(i):
        if i<10:
            return "0%d"%i
        else:
            return "%d"%i
    
    return "%s-%s-%s"%(da.year, pretty(da.month), pretty(da.day))


def str_to_date(s):
    y,m,d = s.split('-')
    return date(int(y), int(m), int(d))
    

class KontenView(ListView):
    
    model = Konto
    
    class KontenTable(tables.Table):
        id = tables.Column()
        kurz = tables.Column(attrs={'td' : { 'style' : "text-align:left"} })
        lang  = tables.TemplateColumn('<a href="{% url \'konto\' record.d1 record.d2 record.lang.kurz %}">\
                                      {{record.lang.lang}}</a>', \
                                      attrs={'td' : { 'style' : "text-align:left"} })
        art   = tables.Column(attrs={'td' : { 'style' : "text-align:left"} })
        saldo = tables.Column(attrs={'td' : { 'style' : "text-align:right"} })
    
        class Meta:
                attrs = {'id' : 'example',
                             'class' : 'display',
                             'style' : 'width:100%',
                #             'cellspacing' : '0'
                }
    
    def get_queryset(self):
        return Konto.objects.exclude(art=Konto.bilanzkonto).order_by('id').all()

    def get_context_data(self, *args, **kwargs):
        context = super(ListView, self).get_context_data(*args, **kwargs)

        d1 = str_to_date(self.kwargs['d1'])
        d2 = str_to_date(self.kwargs['d2'])
    
        data = []
        for k in self.object_list.order_by('pk'):
            if k.is_bestand() or k.is_eigenk():
                so, ha = k.saldiere_bis_incl_unterkonten(d2)
            else:
                so, ha = k.saldiere_incl_unterkonten((d1-oneday, d2))
            
                # = sum ([b.wert for b in k.soll_buchungen.all()])
            #ha = sum ([b.wert for b in k.haben_buchungen.all()])
            de = abs(so-ha)
            if k.is_active():
                de = so-ha
            else:
                de = ha-so
            kurz = k.level()*"--|"+k.kurz
            data.append(
                {
                    'id'   : k.pk,
                    'kurz' : kurz,
                    'lang' : k,
                    'art'  : Konto.artendic[k.art],
                    'soll' : "%10.2f"%(so/100),
                    'haben' :"%10.2f"%(ha/100),
                    'saldo' : "%10.2f"%(de/100),
                    'd1'  : d1,
                    'd2'  : d2
                }
            )
        
        ktb = KontenView.KontenTable(data)
        context.update({'ktb' : ktb})
        return context
    
    
# Create your views here.
class KontoView(DetailView):
    
    model = Konto
    
    class KontoTable(tables.Table):
        datum = tables.Column(attrs={'td' : { 'style' : "text-align:right"} })
        soll  = tables.Column(attrs={'td' : { 'style' : "text-align:right"} })
        haben = tables.Column(attrs={'td' : { 'style' : "text-align:right"} })
        gegenk = tables.TemplateColumn('<a href="{% url \'konto\'  record.d1 record.d2 record.gegenk.kurz %}">\
                                      {{record.gegenk.lang}}</a>', \
                                      attrs={'td' : { 'style' : "text-align:right"} })
        erkl  = tables.Column(attrs= {'td' : { 'style' : "text-align:right"} })
        beleg = tables.Column()
        
        class Meta:
            attrs = {'id' : 'example',
                         'class' : 'display',
                         'style' : 'width:100%',
            #             'cellspacing' : '0'
            }
    
    def get_object(self, queryset=None):
        return Konto.objects.get(kurz=self.kwargs['pk'])
    #    return DetailView.get_object(self, queryset=queryset)
    
    def get_context_data(self, *args, **kwargs):
        
        context = super(DetailView, self).get_context_data(*args, **kwargs)
    
        d1 = str_to_date(self.kwargs['d1'])
        d2 = str_to_date(self.kwargs['d2'])
        
        KontoView.KontoTable.d1 = d1
        KontoView.KontoTable.d2 = d2
        
        period = (d1, d2)
        knt = self.object
        
        data = [] # container list of dictionaries for the table
        
        delta = 0
        habe_a = 0
        soll_a = 0
        soll_e = 0
        habe_e = 0
        if knt.is_bestand() or knt.is_eigenkmain() or knt.is_bilanz():
            #soll_a, habe_a = knt.saldiere_bis_incl_unterkonten(d1-oneday)
            soll_a, habe_a = knt.saldiere_bis(d1-oneday)
            line = {'datum' : date_to_str(d1),
                         'erkl' : 'Bestand am %s'%date_to_str(d1),
                         'gegenk' : knt
                  }
            delta = min(soll_a, habe_a)
            hab = habe_a - delta
            sol = soll_a - delta
            hab = "%10.2f"%(hab/100)
            sol = "%10.2f"%(sol/100)
            if soll_a >= habe_a:
                line.update({'soll' : sol})
            else:
                line.update({'haben' : hab})
            data.append(line)
            
            
        soll_e = soll_a-delta
        habe_e = habe_a-delta
        sb = knt.get_soll_buchungen(period).all()
        hb = knt.get_haben_buchungen(period).all()
        
        #sb = knt.get_all_sollbuchungen(period)
        #hb = knt.get_all_habenbuchungen(period)
        
        bctime = {}
        for b in sb.all():
            if b.datum in bctime:
                bctime[b.datum].append(b)
            else:
                bctime[b.datum] = [b]
        for b in hb.all():
            if b.datum in bctime:
                bctime[b.datum].append(b)
            else:
                bctime[b.datum] = [b]
        
        d=date.today()
        for d in sorted(bctime.keys()):
            for b in bctime[d]:
                if b in knt.soll_buchungen.all():
                    soll_e += b.wert
                    soll = "%10.2f"%(b.wert/100)
                    habe = ''
                    genk = b.habenkonto
                else:
                    soll = ''
                    habe_e += b.wert
                    habe = "%10.2f"%(b.wert/100)
                    genk = b.sollkonto
                data.append (
                        { 'datum' : date_to_str(d),
                         'soll'  : soll,
                         'haben'  : habe,
                         'erkl' : b.beschreibung,
                         'gegenk' : genk,
                         'beleg' : b.beleg
                        } )

        soll, habe = knt.saldiere(period) # ohne unterkonten
        
        # adding one level of Unterkonten
        if knt.has_unterkonten():
            for k in knt.unterkonten.all():
                if k.is_bestand():
                    soll_a, habe_a = k.saldiere_bis_incl_unterkonten(d1-oneday)
                    line = {'datum' : date_to_str(d1),
                                 'erkl' : 'Bestand am %s'%date_to_str(d1),
                                 'gegenk' : k
                          }
                    delta = min(soll_a, habe_a)
                    hab = habe_a - delta
                    sol = soll_a - delta
                    hab = "%10.2f"%(hab/100)
                    sol = "%10.2f"%(sol/100)
                    if soll_a >= habe_a:
                        line.update({'soll' : sol})
                    else:
                        line.update({'haben' : hab})
                    data.append(line)

                sol, hab = k.saldiere_incl_unterkonten(period)
                delt = min(sol, hab)
                sol-=delt
                hab-=delt
                line = {'erkl' : 'Veraend. %s - %s '%(date_to_str(d1),date_to_str(d2)),
                         'gegenk' : k
                         }
                soll_e+=sol
                habe_e+=hab
                if sol>=hab:
                    sol = "%10.2f"%(sol/100)
                    line.update({'soll' : sol})
                else:
                    hab = "%10.2f"%(hab/100)
                    line.update({'haben' : hab})
                data.append(line)

                if k.is_bestand():
                    soll_a, habe_a = k.saldiere_bis_incl_unterkonten(d2)
                    line = {'datum' : date_to_str(d2),
                                 'erkl' : 'Bestand am %s'%date_to_str(d2),
                                 'gegenk' : k
                          }
                    delta = min(soll_a, habe_a)
                    hab = habe_a - delta
                    sol = soll_a - delta
                    hab = "%10.2f"%(hab/100)
                    sol = "%10.2f"%(sol/100)
                    if soll_a >= habe_a:
                        line.update({'soll' : sol})
                    else:
                        line.update({'haben' : hab})
                    data.append(line)

        sol = "%10.2f"%(soll_e/100)
        hab = "%10.2f"%(habe_e/100)
        
        erkl = 'SUMME soll/haben'
        if knt.is_bilanz():
            erkl = 'BLANZ / Veraenderung'
        data.append({'datum' : date_to_str(d2),
                     'soll'  : sol,
                     'haben'  : hab,
                     'erkl' : erkl,
                     'gegenk' : knt
                     })
        
        sol = "%10.2f"%(abs(soll_e-habe_e)/100)
        hab = sol
        if soll_e >= habe_e:
            sol = ''
        else:
            hab = ''
        if not knt.is_bilanz():
            data.append({'datum' : date_to_str(d2),
                         'haben'  : hab,
                         'soll'  : sol,
                         'erkl' : 'SALDO',
                         'gegenk' : knt
                         })
            
        for d in data:
            d.update({'d1' : d1, 'd2' : d2})
                
        tab = KontoView.KontoTable( data )
        context.update( {'tab' : tab, 
                         'konto' : knt.lang,
                         'd1' : date_to_str(d1),
                         'd2' : date_to_str(d2),
                         } )
        if knt.oberkonto is None:
            context.update({
                'oberkonto' : knt
            }
        )
        else:
            context.update({
                'oberkonto' : knt.oberkonto
            })
             

        
        return context

class NKView(TemplateView):
    
    template_name = 'booking/nk.html'
    
    class NK_table(tables.Table):
        nk = tables.Column(attrs={'td' : { 'style' : "text-align:left"} })
        nk = tables.TemplateColumn('<a href="{% url \'konto\' record.d1 record.d2 record.kurz %}" class="{{record.class}}">\
                                      {{record.lang}}</a>', \
                                      attrs={'td' : { 'style' : "text-align:right"} })

        Summe = tables.Column(attrs={'td' : { 'style' : "text-align:right"} })
        
        class Meta:
                attrs = {'id' : 'example',
                             'class' : 'display',
                             'style' : 'width:100%',
                             'orderalbe' : 'False'
                }


    def get_lomtr(self):
        pass
    
    def vert_kosten(self):
        nkbs = Buchung.objects.filter(sollkonto__kurz = 'NK', 
                    beschreibung__contains="#Nebenkkosten-%d#"%self.year) #TODO better filtering...
        
        lomtr = [] # list of mieter
        lonks = [] # list of nks
        res   = {} # list (over NK) of dicts of kosts
        lonkkont = []
        for nk in nkbs.all():
            mtr = nk.beschreibung.split('#')[-1]
            nkn = nk.habenkonto.nicename()
            val = nk.wert
            if not mtr in lomtr:
                lomtr.append(mtr)
            if not nkn in lonks:
                lonks.append(nkn)
                lonkkont.append(nk.habenkonto) 
            if not mtr in res:
                res[mtr] = {}
            res[mtr][nkn] = val
            
        sumnks = { mtr : sum ([ res[mtr][nks] for nks in lonks])  for mtr in lomtr}
        summtr = { nks : sum ([ res[mtr][nks] for mtr in lomtr])  for nks in lonks}
        summ = sum (sumnks.values())
        return res, lomtr, lonks, sumnks, summtr, summ, lonkkont
        
    def payednk(self):
        
        rueckb = Buchung.objects.filter(habenkonto__kurz = 'ER', 
                    beschreibung__contains="#Rueckb.Pausch-%d#"%self.year)
        payd = {}
        for b in rueckb.all():
            mtr = b.beschreibung.split('#')[-1]
            payd[mtr] = -b.wert
        return payd
        
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        
        self.year = self.kwargs['year']
        
        d1 = date(self.year-1,4,1)
        d2 = date(self.year,3,31)
        
        res, lomtr, lonks, sumnks, summtr, summ, lonkkont = self.vert_kosten()
        
        payd = self.payednk()
        
        loc = [] # list of dynamically generated columns
        for mt in lomtr:
            loc.append((mt, tables.Column(
                attrs={'td' : { 'style' : "text-align:right"} })
            ))

        data = []
        for nkko, nk in zip (lonkkont, lonks):
            line = { 'nk' : nk, 
                     'Summe' : "%10.2f"%(summtr[nk]/100),
                     'kurz'  : nkko.kurz,
                     'lang'  : nk
            }
            line.update({
                mt : "%10.2f"%(res[mt][nk]/100) for mt in lomtr
            } 
            )
            data.append (line)
        
        totf = {mt : sum ( [res[mt][nk] for nk in lonks ]) for mt in lomtr}
        
        line = { 'nk' : 'SUMME', 'kurz' : 'B', 'lang' : "SUMME", 'class' : "not-active", 
                'Summe' : "%10.2f"%(summ/100)}
        line.update({ mt : "%10.2f"%(sumnks[mt]/100) for mt in lomtr})
        data.append( line )
        
        # payed NK...
        line = {'nk' : 'Voraus', 'kurz' : 'B', 'lang' : 'Vorauszahlung', 'class' : "not-active", 'Summe' : "%10.2f"%(sum(payd.values()) / 100)}
        line.update(
            { mt : "%10.2f"%(payd[mt]/100) for mt in lomtr }
        )
        data.append(line)
        
        line = {'nk' : '+Guth/-Ford', 'kurz' : 'B', 'lang' : 'Guthaben(+)/Nachz(-)', 'class' : "not-active", 'Summe' : "%10.2f"%(sum([ payd[mt] - totf[mt] for mt in lomtr]) / 100)}
        line.update(
            { mt : "%10.2f"%((payd[mt]-totf[mt])/100) for mt in lomtr}
        )
        data.append(line)
        
        for line in data:
            line.update({'d1' : date_to_str(d1), 'd2' : date_to_str(d2) })
        ta = NKView.NK_table ( data, extra_columns = loc)
        
        context.update({ 'nktable' : ta, 'year' : self.year, 'pyear' : self.year-1})
        return context

class BilanzView(TemplateView):
    
    tempmplate_name = 'bilanz.html'
    
    class BilanzTable(tables.Table):
        Konto = tables.Column()
        Saldo = tables.Column()
    
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
    
        datum = date(
            self.kwargs['year'], 
            self.kwargs['month'], 
            self.kwargs['day']
        )
        
        return context
    
class GuVView(TemplateView): 
    pass


