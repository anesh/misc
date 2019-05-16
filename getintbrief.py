import os
import paramiko
import xlsxwriter
import socket
import re
import sys
import getpass
from ciscoconfparse import CiscoConfParse

username = raw_input('Enter username for device login:')
password =  getpass.getpass()

f1 = open('device2.txt','r')

book = xlsxwriter.Workbook('shipintbriefvlan.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","IPAddress","sh ip int brief Vlans"]
for col, text in enumerate(header):
	sheet.write(0, col, text, header_format)



devices = f1.readlines()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
row=0

for device in devices:
    row=row+1
    column = device.split()
    ip=column[1]
    print column[0]
    try:
	ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
	stdin,stdout,stderr = ssh.exec_command('show ip int brief ')
	routeoutput=stdout.readlines()
        routeparse = CiscoConfParse(routeoutput)
        connectedparams=routeparse.find_objects("Vlan")
	for connected in connectedparams:
		row=row+1
		sheet.write(row,0,column[0])
		sheet.write(row,1,column[1])
		sheet.write(row,2,connected.text)

	
    except socket.error, e:
        output = "Socket error"
    except paramiko.SSHException:
        output = "Issues with SSH service"
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
    except Exception as e: print(e)
    
book.close()    
f1.close()
