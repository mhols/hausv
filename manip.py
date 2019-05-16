import os
import django
from django import db
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

site = 'HV.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", site)
django.setup()
from booking.models import *
from goodies.util import *

from datetime import date



def upload():
	workfile=os.sys.argv[-1]

	f = open(workfile, 'r', encoding='utf-8')
	alle = f.readlines()

	for n, b in enumerate(alle):
		try:
			generate_buchung(b, delimiter=':')
		except Exception as ex:
			print( "problem  with line:", n, ex, " text = ", b)

upload()