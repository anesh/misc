import requests
from bs4 import BeautifulSoup

reqnum = "REQ0262190"
user = 'anesh.ponnarasseryke'
pwd = 'Adimurai@888'


sysidurl = 'https://cantiresb.service-now.com/api/now/table/sc_req_item?sysparm_query=request.number='+reqnum

headers = {"Accept":"application/xml"}

response = requests.get(sysidurl, auth=(user, pwd), headers=headers)
xmldata = response.text

soup = BeautifulSoup(xmldata,'xml')
getsysidtag = soup.find_all('sys_id')
sysid = ""
for sysidtag in getsysidtag:
        sysid = sysidtag.get_text()


servicenowupdatelist = ["test: 1.1.1.1", "test: 2:2:2:2"] 
updateurl = 'https://cantiresb.service-now.com/api/now/table/sc_req_item/'+sysid
headers = {"Content-Type":"application/xml","Accept":"application/xml"}
values = ''.join(servicenowupdatelist)
print type(values)
payload = "<request><entry><comments>"+values+"</comments></entry></request>"
response = requests.put(updateurl, auth=(user, pwd), headers=headers, data=payload)
print response.text


