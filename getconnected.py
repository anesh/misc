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

book = xlsxwriter.Workbook('shiprouteconnected.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","IPAddress","sh ip route connected"]
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
        stdin,stdout,stderr = ssh.exec_command('show version ')
        version=stdout.read()
        if not re.search('Cisco Nexus Operating System \(NX-OS\) Software', version):

		ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
		stdin,stdout,stderr = ssh.exec_command('show ip route connected ')
		routeoutput=stdout.readlines()
        	routeparse = CiscoConfParse(routeoutput)
        	connectedparams=routeparse.find_objects("connected")
		for connected in connectedparams:
			row=row+1
			sheet.write(row,0,column[0])
			sheet.write(row,1,column[1])
			sheet.write(row,2,connected.text)

	else:
		ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
                stdin,stdout,stderr = ssh.exec_command('sh ip route direct vrf all')
                routeoutput=stdout.readlines()
                routeparse = CiscoConfParse(routeoutput)
                connectedparams=routeparse.find_objects("attached")
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
