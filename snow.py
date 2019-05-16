import requests
import re
from bs4 import BeautifulSoup

url = 'https://cantire.service-now.com/api/now/table/sc_req_item?sysparm_query=request.number%3DREQ0267590&sysparm_limit=1'

user = 'anesh.ponnarasseryke'
pwd = 'Adimurai@888'

headers = {"Accept":"application/xml"}

response = requests.get(url, auth=(user, pwd), headers=headers)

if response.status_code != 200: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
    exit()

soup = BeautifulSoup(response.text,'xml')
titles = soup.find_all('description')
for title in titles:
	data = title.get_text()
	number=re.search(r"(?<=Number of IP's required\?\:)(.*)",data)
	fqdn=re.search(r"(?<=FQDN/Hostname/Device Name for which IP's are requested\?\:)(.*)",data)
	vlanid=re.search(r"(?<=VLAN ID\:)(.*)",data)
	ipsubnet=re.search(r"(?<=IP Subnet\:)(.*)",data)
	print number.group(0)
	print fqdn.group(0)
	print vlanid.group(0)
	print ipsubnet.group(0)

