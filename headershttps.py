import requests

f1 = open('fqdns','r')

fqdns = f1.read().splitlines()

a=0
while a< 100:
	a=a+1
	for fqdn in fqdns:
		r = requests.get(fqdn ,allow_redirects=False,verify=False)
		code=r.status_code
		if code == 301:		
			print "Domain:"+fqdn +"  "+"status:301"+"  "+"Redirect:"+r.headers['Location']
		else:
			print "Domain:"+fqdn +"  "+"status:"+str(code)

		
