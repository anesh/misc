import os
import paramiko
import xlsxwriter
import socket
import re
import sys
import time
from ciscoconfparse import CiscoConfParse
import getpass


username = raw_input('Enter username for device login:')
password =  getpass.getpass()


book = xlsxwriter.Workbook('hostnameverify.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["DeviceIP","Hostname"]
for col, text in enumerate(header):
        sheet.write(0, col, text, header_format)



f1 = open('device.txt','r')


devices = f1.readlines()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
row=0


for device in devices:
    row=row+1
    column = device.split()
    print column[0]
    sheet.write(row, 0,column[0] )

    try:
        out=ssh.connect(column[0], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
	stdin,stdout,stderr = ssh.exec_command('sh run')
        hostname = stdout.readlines()
	configparse = CiscoConfParse(hostname)
       	hostnamefind = configparse.find_objects("^hostname")
	domainfind = configparse.find_objects("^ip domain")
	for hostname in hostnamefind:
		hostnameval=re.search(r'(?<=hostname\s)(\S*)',hostname.text)
		print  hostnameval.group(0)
        	sheet.write(row, 1,hostnameval.group(0) )               
    except socket.error, e:
        output = "Socket error"
	sheet.write(row, 2,output )
    except paramiko.SSHException:
        output = "Issues with SSH service"
	sheet.write(row, 2,output )
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
	sheet.write(row, 2,output )
    except:
        print "error occured"
        continue


f1.close()
book.close()
