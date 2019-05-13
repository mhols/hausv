import xlrd
import sys
from datetime import date
import os

proj_path = "/home/hols/Documents/Lerchenstrasse/djangoadmin/L3ADMIN/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "L3ADMIN.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
#os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import l3hv.models as models

sheet = xlrd.open_workbook(sys.argv[1]).sheet_by_index(0)

eventmap = {
	'VerwaltunRabe' : ('Z_UNSPEC',   'PETER'),
	'NKHOLGER'	: ('Z_MN', 'HOLGER'),
	'EINLAGENALEX'  : ('Z_EINLAGE', 'ALEX'),
	'HELVETIA'	  : ('Z_HELVETIA_GEBAEUDE', None),
	'BNETZE'	: ('Z_BNNETZE_WASSER', None),
	'BADENOVA'	: ('Z_BADENOVA_STROM', None),
	'NKPETER'	   : ('Z_MN', 'PETER'),
	'NKROEDER'	: ('Z_MN', 'ROEDER'),
	'GEBUERNBANK'	: ('Z_KONTOFUEHRUNG', None),
	'ALTELEIPZIGER'	: ('Z_ALTE_LEIPZIGER', None),
	'STADTWERKEWALDKIRCH' : ('Z_STADTWERKE_WALDKIRCH_GAS',None),
	'Ruttkowski'	: ('Z_HANDWERKER_RUTKOWSKI', None),
	'SOREXFEUERL'   : ('Z_HANDWERKER_SOREX', None),
	'BUEROBEDVIAPETER' : ('Z_BUEROBEDARF', 'PETER'),
	'AUSGLNKHOLGER' : ('Z_AUSGLEICH_NK', 'HOLGER'),
	'AUSGLNKPETER' : ('Z_AUSGLEICH_NK', 'PETER'),
	'AUSGLNKROEDER' : ('Z_AUSGLEICH_NK', 'ROEDER'),
	'ALTELEIPZIGER'	: ('Z_ALTELEIPZIGER', None),
	'ALLIANZ'		: ('Z_ALLIANZ_HAFT', None),
	'DIEKUECHE'		: ('Z_UNSPEC', None),
	'DRYTEC'		: ('Z_UNSPEC', None),
	'KADEL'			: ('Z_HANDWERKER_KADEL', None),
	'SVGEBAEUDE'	: ('Z_SV_FEUER', None),
	'EPRIMO'		: ('Z_UNSPEC', None),
	'RITTER'		: ('Z_RITTER', None),
	'LERNER'		: ('Z_HANDWERKER_LERNER', None),
	'WASSERZAEHLERVIAALEX' : ('Z_UNSPEC', 'ALEX'),
	'EINLAGENPETER' : ('Z_EINLAGE', 'PETER'),
	'GRABPFLEGE'    : ('Z_GRABPFLEGE', 'PETER'),
	'GRABBUERO'     : ('Z_UNSPEC', 'PETER'),
	'SCHMID'		: ('Z_HANDWERKER_SCHMIDT', None),
	'BUEROBEDVIAPETER' : ('Z_BUEROMATERIAL', 'PETER'),
	'BARPRIVAT'		: ('Z_PRIVAT', 'PETER')
}


d2i = {
	'01' : 1,
	'02' : 2,
	'03' : 3,
	'04' : 4,
	'05' : 5,
	'06' : 6,
	'07' : 7,
	'08' : 8,
	'09' : 9,
	}
y,m,d = 1,2,3
amount = 0
for i in range(1, sheet.nrows):
	
	ddd,verw,amount = sheet.row_values(i)
	try:
		y,m,d = ddd.split('-')
	except:
		continue
#	print (y, m, d)
	try:
		amount = float(amount)
	except:
		pass
	# print (amount)
	try:
		m=d2i[m]
	except:
		m = int(m)
	try:
		d=d2i[d]
	except:
		d = int(d)
			
	dd = date(int(y),m,d)
	try:
		#print (eventmap[verw][0] )
		et = models.EventType.objects.get(art=eventmap[verw][0])
		e = models.Event()
		e.d0 = dd
		e.art = et
		e.menge = amount
		e.zuordnungHaus = models.Haus.objects.get(kurz='H22')
		try:
			e.zuordnungMieter = models.Mieter.objects.get(kurz=eventmap[verw][1])
		except:
			e.zuordnungMieter = None
		try:
			e.zuordnungMietEinheit = e.zuordnungMieter.mieteinheit
		except:
			e.zuordnungMietEinheit = None
		print ('OK ', e)
		e.save()
	except Exception as ex:
		print (ddd, verw, amount,ex)
	
	