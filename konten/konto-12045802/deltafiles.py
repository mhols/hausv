'''
Created on Nov 12, 2018

@author: hols
'''

import sys

a, b = sys.argv[1:3]

fa = open(a, 'r')
fb = open(b, 'r')

la = fa.readlines()
lb = fb.readlines()


inter_ab = []
a_w_b = []
b_w_a = []

ka = []
kb = []

for l in la:
    if not l in ka:
        ka.append(l)
    if l in lb:
        if not (l in inter_ab):
            inter_ab.append(l)
    else:
        a_w_b.append(l)

for l in lb:
    if not l in kb:
        kb.append(l)
    if l in la:
        if not (l in inter_ab):
            inter_ab.append(l)
    if not (l in la):
        b_w_a.append(l)

print (len(la), len(ka), len(a_w_b), len(inter_ab))

print (len(lb), len(kb), len(b_w_a), len(inter_ab))

print ( a_w_b)

