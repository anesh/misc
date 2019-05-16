import requests
import json
import re
from bs4 import BeautifulSoup

user = 'anesh.ponnarasseryke'
pwd = 'Adimurai@999'




url = 'https://cantiresb.service-now.com/api/now/table/change_task'


headers = {"Content-Type":"application/json","Accept":"application/json"}




task_data = {"parent":"09c46efddbdd730094e3755a8c9619dc",
             "change_request":"09c46efddbdd730094e3755a8c9619dc",
	     "short_description":"Implementation Task",
             "assignment_group":"b9c1fb43dbe55b004f8b3ebf9d961930",
	     "assigned_to":"a997cbd8db641b4c04215878dc961913",
             "state":"1",
	     "u_change_task_stage":"implement"}


taskpayload = json.dumps(task_data)
tskrsp =requests.post(url, auth=(user, pwd), headers=headers, data=taskpayload)
print tskrsp.text
