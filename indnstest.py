import dns.resolver

f1 = open('internal.txt','r')

fqdns = f1.read().splitlines() 

ips=['10.255.255.254','10.255.255.253','10.126.4.105','10.126.4.109','10.17.4.105','10.17.4.109']


resolver = dns.resolver.Resolver()
#resolver.timeout = 1
#resolver.lifetime = 1

while True:
	for fqdn in fqdns:
		for ip in ips:
			try:
				resolver.nameservers = [ip]
				answers= resolver.query(fqdn, 'SOA')
				for rdata in answers:
    					print fqdn,rdata.mname,ip

			except Exception as e:
				print fqdn,str(e)	  

