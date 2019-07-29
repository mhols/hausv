'''
Created on Oct 26, 2018

@author: hols
'''

import numpy as np
import os
import django
from django import db
from django.db.models import Sum

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

site = 'HV.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", site)
django.setup()
from booking.models import *
from goodies.util import *

from datetime import date

for b in Buchung.objects.all():
    b.beschreibung = b.beschreibung.replace(';',' ')
    b.save()
    
    