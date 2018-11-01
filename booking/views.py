from datetime import date

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

import django_tables2 as tables

from .models import Konto, Buchung


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
        kurz = tables.Column(attrs={'td' : { 'style' : "text-align:left"} })
        lang  = tables.TemplateColumn('<a href="{% url \'konto\' record.d1 record.d2 record.lang.kurz %}">\
                                      {{record.lang.lang}}</a>', \
                                      attrs={'td' : { 'style' : "text-align:left"} })
        art   = tables.Column(attrs={'td' : { 'style' : "text-align:left"} })
        #soll  = tables.Column(attrs={'td' : { 'style' : "text-align:right"} })
        #haben = tables.Column(attrs={'td' : { 'style' : "text-align:right"} })
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
        for k in self.object_list:
            so, ha = k.saldiere((d1,d2,))
                # = sum ([b.wert for b in k.soll_buchungen.all()])
            #ha = sum ([b.wert for b in k.haben_buchungen.all()])
            de = abs(so-ha)
            if k.is_active():
                de = so-ha
            else:
                de = ha-so
            kurz = k.level()*" "+k.kurz
            data.append(
                {
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
        gegenk = tables.TemplateColumn('<a href="{% url \'konto\'  record.d1 record.d2 record.gegenk.kurz %}" class="not-active">\
                                      {{record.gegenk.lang}}</a>', \
                                      attrs={'td' : { 'style' : "text-align:right"} })
        erkl  = tables.Column(attrs= {'td' : { 'style' : "text-align:right"} })
        
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
        
        #print ('last saldo ', knt.last_saldo())
        data = []
        
        if knt.is_bestand():
            soll, habe = knt.saldiere((d1,d1))
            sol = "%10.2f"%(soll/100)
            hab = "%10.2f"%(habe/100)
        
            data.append({'datum' : date_to_str(d1),
                         'soll'  : sol,
                         'haben'  : hab,
                         'erkl' : 'bestand am %s'%date_to_str(d1),
                         'gegenk' : knt
                         })
            
            sol =  hab = "%10.2f"%(abs(soll-habe)/100)
            if soll >= habe:
                hab='--'
            else:
                sol='--'
            data.append({'datum' : date_to_str(d1),
                         'soll'  : sol,
                         'haben'  : hab,
                         'erkl' : 'saldo am %s'%date_to_str(d1),
                         'gegenk' : knt
                         })
            
            
        
        sb = knt.soll_buchungen.filter(datum__range=period).all()
        hb = knt.haben_buchungen.filter(datum__range=period).all()
        
        bctime = {}
        for b in sb:
            if b.datum in bctime:
                bctime[b.datum].append(b)
            else:
                bctime[b.datum] = [b]
        for b in hb:
            if b.datum in bctime:
                bctime[b.datum].append(b)
            else:
                bctime[b.datum] = [b]
        
        d=date.today()
        for d in sorted(bctime.keys()):
            for b in bctime[d]:
                if b in knt.soll_buchungen.all():
                    soll = "%10.2f"%(b.wert/100)
                    habe = ''
                    genk = b.habenkonto
                else:
                    soll = ''
                    habe = "%10.2f"%(b.wert/100)
                    genk = b.sollkonto
                data.append (
                        { 'datum' : date_to_str(d),
                         'soll'  : soll,
                         'haben'  : habe,
                         'erkl' : b.beschreibung,
                         'gegenk' : genk
                        } )
        soll, habe = knt.saldiere(period)
        sol = "%10.2f"%(soll/100)
        hab = "%10.2f"%(habe/100)
        
        data.append({'datum' : date_to_str(d),
                     'soll'  : sol,
                     'haben'  : hab,
                     'erkl' : 'SUMME soll/haben',
                     'gegenk' : knt
                     })
        
        sol = "%10.2f"%(abs(soll-habe)/100)
        hab = sol
        if soll >= habe:
            sol = ''
        else:
            hab = ''
        data.append({'datum' : date_to_str(d),
                     'haben'  : hab,
                     'soll'  : sol,
                     'erkl' : 'SALDO',
                     'gegenk' : knt
                     })
        
        for d in data:
            d.update({'d1' : d1, 'd2' : d2})
                
        tab = KontoView.KontoTable( data )
        context.update( {'tab' : tab, 
                         'konto' : knt.lang } )
        return context

class NKView(TemplateView):
    
    template_name = 'booking/nk.html'
    
    class NK_table(tables.Table):
        nk = tables.Column(attrs={'td' : { 'style' : "text-align:left"} })
        nk = tables.TemplateColumn('<a href="{% url \'konto\' record.d1 record.d2 record.kurz %}">\
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
        
        line = { 'nk' : 'SUMME', 'kurz' : 'B',
                'Summe' : "%10.2f"%(summ/100)}
        line.update({ mt : "%10.2f"%(sumnks[mt]/100) for mt in lomtr})
        data.append( line )
        
        # payed NK...
        line = {'nk' : 'Voraus', 'kurz' : 'B', 'Summe' : "%10.2f"%(sum(payd.values()) / 100)}
        line.update(
            { mt : "%10.2f"%(payd[mt]/100) for mt in lomtr }
        )
        data.append(line)
        
        line = {'nk' : '+Guth/-Ford', 'kurz' : 'B', 'Summe' : "%10.2f"%(sum([ payd[mt] - totf[mt] for mt in lomtr]) / 100)}
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


