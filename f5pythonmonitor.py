import requests
import time
#times=4

while true:
	response = requests.request("GET","http://10.18.57.217/f5")
	print response.text
	#times = times-1
	time.sleep(5)  # suspend execution for 5 secs
