import os
from pathlib import Path
import django
from django import db
import pathlib
from itertools import chain
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

import numpy as np
from datetime import date
#site = 'HV.settings'
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", site)
#django.setup()

#from models import *

def split_line(line):
    try:
       Auftragskonto, Buchungstag, Valutadatum, Buchungstext, \
       Verwendungszweck, BeguenstigterZahlungspflichtiger, \
       Kontonummer, BLZ, Betrag, Waehrung, Info = line.replace('"','').split(';')
       return Kontonummer, Buchungstag, Betrag
    except:
        return '','','0,00'

def read_files():
    """
    returns : list of file contents
    """
    dirs = ['2018',] # 'tobetreated', 'utf8']
    encoding = 'iso-8859-1'
    basepath = [ Path(di) for di in dirs] 
    
    for bpath in basepath:
        for f in ( ff for ff in bpath.iterdir() if ff.is_file()):
            yield f

def read_lines(f):
    for l in open(f, 'br'):
        try:
            s = l.decode(encoding)
        except:
            try:
                s = l.decode('utf-8')
            except:
                s =''
        yield s

def read_all_lines():
    files = read_files()
    for f in files:
        for s in read_lines(f):
            yield f, s 

"""
    
    files = chain.from_iterable ( [
        (ff for ff in bpath.iterdir() if ff.is_file()) for bpath in basepath])
    
    for f in files:
        print(f)
        
    try:
        return ((f,open(f, 'r', encoding=encoding).readlines()[1:]) for f in files)
    except:
        return ((f,open(f, 'r', encoding='utf-8').readlines()[1:]) for f in files)
"""
"""
def check_interval():
    days = np.zeros(1000)
    d0 = date(2017,1,1)
    for f in read_files():
        for ff, l in read_lines(f):
        ko, bu1, be = split_line(tmp[0])
        ko, bu0, be = split_line(tmp[-1])
        try:
            d,m,y = bu0.split('.')
            d0 = date(int(y)+2000, int(m), int(d))
            d,m,y = bu1.split('.')
            d1 = date(int(y)+2000, int(m), int(d))
        except:
            continue    
        
        print (f, d0,d1)
            
"""

def check_umsaetze():
    for f in read_files():
        res = {}
        for l in read_lines(f):
            ko, bu, be = split_line(l)
            if be == '0,00':
                continue
            key = ko+bu+be
            try:
                res[key].append(l)
            except:
                res[key] = [l]
        for k in res.keys():
            if len(res[k])>1:
                print ('\n'.join(res[k]),'\n-------------\n')

def sum_umsaetze():
    d0 = date(2018,1,1)
    d1 = date(2019,7,1)
    
    sup, sum = 0, 0
    keys = []
    res = []
    for f in read_files():
        new_keys = []
        for l in read_lines(f):
            ko, bu, be = split_line(l)
            if be == '0,00':
                continue
            try:
                d,m,y = bu.split('.')
                da = date(int(y)+2000, int(m), int(d))
            except:
                print ('could not parse ', bu)
                continue
        
            if da < d0 or da > d1:
                continue
            
            key = ko+bu+':'+be
            key.replace('"','').replace(' ','')
            if key in keys:
                continue
            
            new_keys.append(da)
            keys.append(key)
            be = int(be.replace(',',''))
            if be>0:
                sup += be
            else:
                sum += -be
            res.append( (da, be) )
        #keys.extend(new_keys)
    
    print ('\n'.join(['{0}'.format(s) for s in \
                      (sorted( res, key=lambda d: d[0]))]))
    #print ('\n'.join(['{0}'.format(s) for s in \
    #                  (sorted( keys ))]))
    
    
    print (sup, sum, sup-sum)
            
#check_umsaetze()
#check_interval()
sum_umsaetze()