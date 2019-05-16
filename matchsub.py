import os
import re
import sys
from netaddr import IPNetwork, IPAddress

f1 = open('ips.txt','r')
f2= open('subnets.txt','r')
ips = f1.readlines()
subnets=f2.readlines()


for ip in ips:
	try:
		for subnet in subnets:
			if IPAddress(ip) in IPNetwork(subnet):
				print ip.strip(),subnet.strip()
	except:
		continue


