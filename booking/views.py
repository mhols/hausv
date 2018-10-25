from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

import django_tables2 as tables

from .models import Konto


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
        kurz = tables.Column()
        lang  = tables.Column()
        art   = tables.Column()
        soll  = tables.Column()
        haben = tables.Column()
        delta = tables.Column()
        url   = tables.Column()

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
    
        data = {}
        for k in self.object_list:
            data.update(
            {
                'kurz' : k.kurz,
                'lang' : k.lang,
                'soll' : sum ([b.wert for b in k.soll_buchungen.all() ])
            }    
            )
    
        return context
    
    
# Create your views here.
class KontoView(DetailView):
    
    model = Konto
    
    class KontoTable(tables.Table):
        datum = tables.Column(attrs={'td' : { 'style' : "text-align:right"} })
        soll  = tables.Column(attrs={'td' : { 'style' : "text-align:right"} })
        haben = tables.Column(attrs={'td' : { 'style' : "text-align:right"} })
        gegenk = tables.TemplateColumn('<a href="{% url \'konto\' record.gegenk.kurz %}">\
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
    
        print (self.request)
        knt = self.object
        
        #print ('last saldo ', knt.last_saldo())
        sb = knt.soll_buchungen.all()
        hb = knt.haben_buchungen.all()
        
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
        for d in sorted(bctime.keys()):
            for b in bctime[d]:
                if b in knt.soll_buchungen.all():
                    data.append (
                            { 'datum' : date_to_str(d),
                             'soll'  : "%10.2f"%(b.wert/100),
                             'erkl' : b.beschreibung,
                             'gegenk' : b.habenkonto } )
                else:
                    data.append({
                        'datum' : date_to_str(d),
                             'haben'  : "%10.2f"%(b.wert/100),
                            'erkl' : b.beschreibung,
                            'gegenk' : b.sollkonto
                            }
                        )
        soll, haben = knt.saldiere()
        
        data.append({'datum' : date_to_str(d),
                     'soll'  : "%10.2f"%(soll/100),
                     'erkl' : 'SUMME soll',
                     'gegenk' : knt})
        
        data.append({'datum' : date_to_str(d),
                     'haben'  : "%10.2f"%(haben/100),
                     'erkl' : 'SUMME haben',
                     'gegenk' : knt})
        
        if soll >= haben:
            data.append({'datum' : date_to_str(d),
                     'haben'  : "%10.2f"%((soll-haben)/100),
                     'erkl' : 'SALDO',
                     'gegenk' : knt})
        else:
            data.append({'datum' : date_to_str(d),
                     'soll'  : "%10.2f"%(haben/100),
                     'erkl' : 'SALDO',
                     'gegenk' : knt})
        
        
        
        
        tab = KontoView.KontoTable( data )
        context.update( {'tab' : tab, 
                         'konto' : knt.lang } )
        return context
