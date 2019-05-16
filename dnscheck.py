import dns.resolver

f1 = open('appserver.txt','r')

fqdns = f1.read().splitlines() 

resolver = dns.resolver.Resolver()
#resolver.nameservers = ['199.202.145.0']
resolver.timeout = 2
resolver.lifetime = 2

for fqdn in fqdns:
	try:
		host= fqdn +".net.forzanigroup.net"
		answers= resolver.query(host, 'A')
		for answer in answers:
			print host,answer

	except:
		print fqdn,"cannotberesolved"	  

