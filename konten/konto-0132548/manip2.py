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

import l3hv.models as mods

sheet = xlrd.open_workbook(sys.argv[1]).sheet_by_index(0)

for i in range(1, sheet.nrows):
	#22.10.2017	-63.51	Versicherungs Kammer Bayern GEBAEUDE BRAND P	P	P	Z_VKB_BRAND	NONE

	ddd,amount,blabla,haus,art,me = sheet.row_values(i)
	d,m,y = ddd.split('.')
	d0=date(int(y),int(m),int(d))
	print (d0)
	amount = float(amount)
	et = mods.EventType.objects.get(art=art)
	e = mods.Event()
	e.d0 = d0
	e.art = et
	e.menge = amount
	e.verteilung = 'UNIQUE'
	e.zuordnungHaus = mods.Haus.objects.get(kurz=haus)
	try:
		e.zuordnungMietEinheit = mods.MietEinheit.objects.get(kurz=me)
	except:
		pass
	print (e)
	e.save()
	