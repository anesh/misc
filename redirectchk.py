import requests
import re
from bs4 import BeautifulSoup

f1 = open('fqdns','r')

fqdns = f1.read().splitlines()


for fqdn in fqdns:
	try:
		r = requests.get('http://'+fqdn,timeout=5,allow_redirects=False)
	except Exception as e: print(e)
	soup = BeautifulSoup(r.text, 'html.parser')
	code=r.status_code
        if code == 301:         
                print fqdn,r.headers['Location']
	

	search1=soup.find(text=re.compile('This website is under development.'))
	if search1 == 'This website is under development.':
		print fqdn,search1
	
	search2=soup.find(text=re.compile('DNSadmin'))
	if search2 is not None:
		value=search2.strip()
		print fqdn,"Business Card"	

	search3= soup.find_all('iframe')
	if search3 is not None:
		for url in search3:
			iframe=url.get('src')
			try:	
				r1 = requests.get(iframe)
			except Exception as e: print(e)
			soup1 = BeautifulSoup(r1.text, 'html.parser')
			search4=soup1.find(text=re.compile('This website is under development.'))
		        if search4 == 'This website is under development.':	
				print fqdn,search4
			else:
				search4=soup1.find(text=re.compile('DNSadmin'))
				if search4 is not None:
					value=search4.strip()
					print fqdn,value
				else:
					print fqdn,search4
