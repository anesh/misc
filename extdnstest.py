import dns.resolver

f1 = open('external.txt','r')

fqdns = f1.read().splitlines() 

ips=['199.202.145.0','199.202.145.1','199.202.145.2','199.202.145.3']


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

