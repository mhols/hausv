from django.shortcuts import render
from django.views.generic.detail import DetailView
import django_tables2 as tables

from .models import Konto


# Create your views here.
class KontoView(DetailView):
    
    model = Konto
    
    class KontoTable(tables.Table):
        datum = tables.Column()
        soll  = tables.Column()
        haben = tables.Column()
        
        class Meta:
            orderable = False
    
    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
    
        print (self.request)
        knt = self.object
        
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
                            { 'datum' : d,
                             'soll'  : b.wert} )
                else:
                    data.append({
                        'datum' : d,
                             'haben'  : b.wert}
                    )
        tab = KontoView.KontoTable( data )
        context.update( {'tab' : tab } )
        return context
