import os
import re
import sys
from netaddr import IPAddress

f1 = open('netmaskips.txt','r')
ips = f1.readlines()

for ip in ips:
	column=ip.split()
	print column[0]+"/"+str(IPAddress(column[1]).netmask_bits())


