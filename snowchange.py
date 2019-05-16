import requests
import json
import re
from bs4 import BeautifulSoup

user = 'anesh.ponnarasseryke'
pwd = 'Adimurai@999'




updateurl = 'https://cantiresb.service-now.com/api/now/table/change_request'


headers = {"Content-Type":"application/json","Accept":"application/json"}

json_data = {"short_description":"APK-CTC-PROD-AJ-DDI-Gird Master-Create DNS records",
             "description":"Create Host rercords for <fqdn>",
	     "start_date":"2019-05-21 06:45:00",
	     "end_date": "2019-05-21 10:45:00",
	     "u_standard_id":"Enterprise - Standard",
	     "u_standard_change":"true",
	     "u_change_environment":"prod",
	     "reason":"enhancements",
	     "u_ci_change_type":"existing_ci",
	     "category":"commission",
	     "assignment_group":"b9c1fb43dbe55b004f8b3ebf9d961930",
	     "assigned_to":"a997cbd8db641b4c04215878dc961913",
	     "cmdb_ci":"d870eba54f09120c3e76926ca310c7f5",
             "impact":"1",
	     "risk":"3",
	     "u_service_criticality":"0",
	     "u_impact_assessment":"4",
             "u_ctr_impacting":"No",
	     "u_impact_description":"No impact expected",
             "u_is_there_a_backout_plan":"6",
             "u_duration_of_backout":"1970-01-01 00:10:00",
             "u_was_backout_tested":"6",
             "u_scope_of_change":"4",
	     "u_groups_invloved":"4",
	     "u_degree_of_testing_done":"6",
	     "change_plan":"run playbook infoblox-host.yml",
	     "backout_plan":"run playbook infoblox-delete-host.yml",
	     "test_plan":"DNS validation will happen as part of playbook",
	     "u_gold_or_platinum":"200",
	     "u_dr_plan_changes_required":"No",
	     "u_san_replication_in_place":"No",
	     "u_app_replication_exists":"Yes",
	     "u_is_this_a_ctb_change":"No"}





payload = json.dumps(json_data)
response = requests.post(updateurl, auth=(user, pwd), headers=headers, data=payload)
print response.text
