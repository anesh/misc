import whois

f1 = open('fqdns','r')

fqdns = f1.read().splitlines() 


for fqdn in fqdns:
	try:
		w = whois.whois(fqdn)
		print  w['emails'],w['registrar'] 
		#print w['registrar']
	except Exception as e: print(e)	
