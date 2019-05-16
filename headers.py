import requests

f1 = open('fqdns','r')

fqdns = f1.read().splitlines()


for fqdn in fqdns:
	r = requests.get(fqdn ,allow_redirects=False)
	code=r.status_code
	if code == 301:		
		print "Domain:"+fqdn +"  "+"status:301"+"  "+"Redirect:"+r.headers['Location']
	else:
		print "Domain:"+fqdn +"  "+"status:"+str(code)

		
