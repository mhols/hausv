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


class KontenView(ListView):
    
    model = Konto
    
    class KontenTable(tables.Table):
        kurz = tables.Column(attrs={'td' : { 'style' : "text-align:left"} })
        lang  = tables.TemplateColumn('<a href="{% url \'konto\' record.year record.lang.kurz %}">\
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

        year = self.kwargs['year']
    
        data = []
        for k in self.object_list:
            so, ha = k.saldiere((date(year,1,1),date(year,12,31)))
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
                    'year'  : year
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
        gegenk = tables.TemplateColumn('<a href="{% url \'konto\' record.year record.gegenk.kurz %}">\
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
    
        year = self.kwargs['year']
        knt = self.object
        
        #print ('last saldo ', knt.last_saldo())
        sb = knt.soll_buchungen.filter(datum__year=year).all()
        hb = knt.haben_buchungen.filter(datum__year=year).all()
        
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
        
        data = []
        d=date.today()
        year = self.kwargs['year']
        for d in sorted(bctime.keys()):
            for b in bctime[d]:
                if b in knt.soll_buchungen.all():
                    data.append (
                            { 'datum' : date_to_str(d),
                             'soll'  : "%10.2f"%(b.wert/100),
                             'erkl' : b.beschreibung,
                             'gegenk' : b.habenkonto,
                             'year' : year  } )
                else:
                    data.append({
                        'datum' : date_to_str(d),
                             'haben'  : "%10.2f"%(b.wert/100),
                            'erkl' : b.beschreibung,
                            'gegenk' : b.sollkonto,
                             'year' : year  
                            }
                        )
        soll, haben = knt.saldiere()
        
        data.append({'datum' : date_to_str(d),
                     'soll'  : "%10.2f"%(soll/100),
                     'erkl' : 'SUMME soll',
                     'gegenk' : knt,
                     'year' : year  
                     })
        
        data.append({'datum' : date_to_str(d),
                     'haben'  : "%10.2f"%(haben/100),
                     'erkl' : 'SUMME haben',
                     'gegenk' : knt,
                     'year' : year  
                     })
        
        if soll >= haben:
            data.append({'datum' : date_to_str(d),
                     'haben'  : "%10.2f"%((soll-haben)/100),
                     'erkl' : 'SALDO',
                     'gegenk' : knt,
                     'year' : year  
                     })
        else:
            data.append({'datum' : date_to_str(d),
                     'soll'  : "%10.2f"%(haben/100),
                     'erkl' : 'SALDO',
                     'gegenk' : knt,
                    'year' : year  
                    })
        
        
        
        
        tab = KontoView.KontoTable( data )
        context.update( {'tab' : tab, 
                         'konto' : knt.lang } )
        return context

class NKView(TemplateView):
    
    template_name = 'booking/nk.html'
    
    class NK_table(tables.Table):
        nk = tables.Column()
        Summe = tables.Column()
        
        class Meta:
                attrs = {'id' : 'example',
                             'class' : 'display',
                             'style' : 'width:100%',
                #             'cellspacing' : '0'
                }
        
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        
        nkbs = Buchung.objects.filter(sollkonto__kurz = 'NK')
        
        res = {}
        loc = []
        
        lomtr = []
        lonks = []
        for nk in nkbs.all():
            mtr = nk.beschreibung.split('#')[-1]
            nkn = nk.habenkonto.nicename()
            val = nk.wert

            if not mtr in lomtr:
                lomtr.append(mtr)
            if not nkn in lonks:
                lonks.append(nkn) 
            if not mtr in res:
                res[mtr] = {}
            res[mtr][nkn] = val


        print(res)
        
        print(lomtr)
        
        print(lonks)
                
        for mt in lomtr:
            loc.append((mt, tables.Column(
                attrs={'td' : { 'style' : "text-align:right"} })
            ))

        data = []
        for nk in lonks:
            line = { 'nk' : nk, 
                     'Summe' : "%10.2f"%(sum ([ res[mt][nk]  for mt in lomtr ])/100)
            }
            line.update({
                mt : "%10.2f"%(res[mt][nk]/100) for mt in lomtr
            } 
            )
            data.append (line)
        
        line = { 'nk' : 'SUMME',
                'Summe' : "%10.7f"%(sum([res[mt][nk] for mt in lomtr for nk in lonks])/100)}
        line.update({ mt : "%10.2f"%(sum ( [res[mt][nk] for nk in lonks ])/100) for mt in lomtr})
        data.append( line )
           
        ta = NKView.NK_table ( data, extra_columns = loc)
        
        context.update({ 'nktable' : ta })
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


