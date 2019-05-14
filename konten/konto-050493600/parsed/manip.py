from datetime import date

class NoLine(Exception):
	pass


files = [
'Kontoumsaetze_130_050493600_20180313_202236.csv',
'Kontoumsaetze_130_050493600_20181010_140339.csv',
'Transactions_130_050493600_20180210_182949.csv',
'Transactions_130_050493600_20180210_182949-utf8.csv',
'Transactions_130_050493600_20180427_070942.csv',
'Transactions_130_050493600_20180627_051706.csv',
'Kontoumsaetze_130_050493600_20190123_121253.csv'
]

def str_to_date(s):
	if '/' in s:
		m, d, y = s.split('/')
	elif '.' in s:
		d, m, y = s.split('.')
	else:
		return 0
	
	return date( int(y), int(m), int(d))

def date_to_str(d):
	def pretty(i):
		if i<10:
			return '0%d'%(i)
		else:
			return i
	return "%d-%s-%s"%(d.year, pretty(d.month), pretty(d.day))
	#return "%d.%d.%d"%(d.year, d.month, d.day)

def buchungssatz( d, soll, haben, wert, beschreibung, beleg ):
	if wert > 0:
		b = "%s|%s|%s|%d|%s|%s"%(date_to_str(d), soll, haben, wert, beschreibung, beleg)
	else:
		b = "%s|%s|%s|%d|%s|%s"%(date_to_str(d), haben, soll, -wert, beschreibung, beleg)
	
	return b

def map_to_buchung(line):
	line = line.split(';')
	
	if len(line)<7:
		raise NoLine('no booking line')
	try:
		d    = str_to_date(line[0])
	except:
		raise Exception('no date in ', line)
	iban = line[5]
	value = None
	try:
		value =  int( line[-2].replace('.','').replace(',',''))
	except:
		try:
			value = int( line[-3].replace('.','').replace(',',''))
		except Exception as ex:
			raise Exception('No value ', line, ex)
	b = ''
	if iban == 'DE77300606010002115700': #Alex
		b = "%s : B : EK.Alex : %d : EK Beitrag Alex: None"\
		     %(date_to_str(d), value)
	elif iban == 'DE18500500000025192030':
		b = "%s : NK.VS : B : %d : Helvetia Versicherung: None"\
		     %(date_to_str(d), -value)
	elif iban == 'DE47680501010012366990':
		b = "%s : B : F.Holger : %d : Vorauszahlung NK Holger: None"\
		     %(date_to_str(d), value)
	elif iban == 'DE50680501010012809062':
		b = "%s : NK.GARTEN : B : %d : Rabe Ladislav: None"\
		     %(date_to_str(d), -value)
	elif iban == 'DE08680501010012163313':
		b = "%s : NK.HZ.KAMIN : B : %d : Kaminfeger: None"\
		     %(date_to_str(d), -value)
	elif iban == 'DE59680400070160055000':
		b = buchungssatz(d, 'NK.HZ.STR', 'B', -value, 'Badenova', 'None')
	elif iban == 'DE89680501010002010029':
		b = "%s : NK.HZ.STR : B : %d : Badenova: None"\
		     %(date_to_str(d), -value)
	elif iban == 'DE78760300800210056466':
		b = "%s : B : F.Roeder : %d : NK Voraus Roeder: None"\
		     %(date_to_str(d), value)
	elif iban == 'DE96680700300013254800':
		if value == -4000:
			b = "%s : VERW : B : %d : Verwalung Peter: None"\
			     %(date_to_str(d), 4000)
		elif value == -19000:
			b = ["%s : VERW : B : %d : Verwalung Peter: None"\
			     %(date_to_str(d), 4000),
			     "%s : NK.GARTEN : B : %d : Rabe Garten bezahlt von Peter: None"\
			     %(date_to_str(d), 15000) ]
		elif value == 22000:
			b = "%s : B : F.Peter : %d : NK Voraus Peter: None"\
			     %(date_to_str(d), 22000)
		else:
			raise Exception('DE96680700300013254800')

	elif iban == 'DE23680501010013337519':
		b = "%s : NK.KW : B : %d : Kaltwasser bnNETZE: None"\
		     %(date_to_str(d), -value)
		     
	elif iban == 'DE37680920000000514500':
		b = "%s : NK.HZ.ABR : B : %d : Abrechnungsservice: None"\
		     %(date_to_str(d), -value)

	elif iban == 'DE80680501010002077024':
		b = ["%s : V.H.Kadel : B : %d : Handwerker Kadel: None"\
		     %(date_to_str(d), -value),
		     "%s : NK.HZ.WART : V.H.Kadel : %d : Handwerker Kadel: None"\
		     %(date_to_str(d), -value)
		     ]
	
	elif iban == 'DE94680501010021000405':
		if value <0:
			b = "%s : NK.HZ.GAS : B : %d : Stadtwerke Waldkirch Gas: None"\
			     %(date_to_str(d), -value)
		else:
			b = "%s : B : NK.HZ.GAS  : %d : Stadtwerke Waldkirch Gas (erst.): None"\
			     %(date_to_str(d), value)
	elif iban == 'DE94680501010021000405':
		if value < 0:
			b = "%s : NK.HZ.GAS : B : %d : Stadtwerke Waldkirch Gas: None"\
			     %(date_to_str(d), -value)
		else:
			b = "%s : B : NK.HZ.GAS  : %d : Stadtwerke Waldkirch Gas, erst.: None"\
			     %(date_to_str(d), value)
	elif iban == 'DE46500100600997060607':
		b = buchungssatz(d, 'NK.VS', 'B',  -value, 'Alte Leipziger', 'None')
	elif 'mobileTAN' in line[4]:
		b = buchungssatz(d, 'VERW', 'B', -value, 'Konto Fuehrung SMS TAN', 'None')
	elif 'Abschlussposten' in line[4]:
		b = buchungssatz(d, 'VERW', 'B', -value, 'Konto Fuehrung', 'None')
	elif 'STORNO vom 26' in line[4]:
		b = buchungssatz(d, 'B', 'EK', value, 'STORNO', 'None')
	else:
		raise Exception( "Problem %s "%str(line))
	
	if type(b) is str:
		b = [b]
	
	return iban, value, b

bookings = {}

allbookings=[]

lines=[]

ibans = {}

su = 0

for fi in files:
	f = open(fi, 'r', encoding="latin-1")
	lines = f.readlines()
	for l in lines:
		try:
			iban, value, bs = map_to_buchung(l)
		except NoLine as ex:
			print (ex, l)
			continue
		except Exception as ex:
			print (ex, l)
			continue
		su += value
		
		for b in bs:
			allbookings.append(b)
			try:
				ibans[iban].append(b)
			except:
				ibans[iban] = [b]
			try:
				bookings[b] += 1
			except:
				bookings[b] = 0
	

	f.close()

for b in sorted(bookings.keys()):
	print ('"','None|'+b.replace(' : ','|').replace(': ','|'),'",')

#for i in range(1,10):
#	print ( '"1.%d.2018 : F.Holger : ER : 20000 : Nebenkosten Pauschale Holger : None",'%i)
#	print ( '"1.%d.2018 : F.Peter : ER : 22000 : Nebenkosten Pauschale Peter : None",'%i)
#	print ( '"1.%d.2018 : F.Roeder : ER : 14000 : Nebenkosten Pauschale Roeder : None",'%i)


print ('\n\n====================\n\n')

print (su + 571361)

#for k in sorted(ibans.keys()):
#	print (k)
#	for b in ibans[k]:
#		print (b)


