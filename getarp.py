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

f1 = open('device.txt','r')

book = xlsxwriter.Workbook('arpentries.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","ARP Entries"]
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
	stdin,stdout,stderr = ssh.exec_command('show ip arp ')
	arpoutput=stdout.readlines()
        arpentriesparse = CiscoConfParse(arpoutput)
        arpparams=arpentriesparse.find_objects("ARPA")
	for arp in arpparams:
		row=row+1
		sheet.write(row,0,column[0])
		sheet.write(row,1,arp.text)

	
    except socket.error, e:
        output = "Socket error"
    except paramiko.SSHException:
        output = "Issues with SSH service"
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
    except Exception as e: print(e)
    
book.close()    
f1.close()
