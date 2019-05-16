import os
import paramiko
import socket
import re
import sys
import time
import getpass
import xlsxwriter

f1 = open('device.txt','r')

username = raw_input('Enter username for device login:')
password =  getpass.getpass()


book = xlsxwriter.Workbook('enumreport.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","DeviceIP","Results"]
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
	sheet.write(row, 0,column[0] )
        sheet.write(row, 1,column[1] )


	try:
		print "connecting to", ip
        	ssh.connect(ip, username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
        	stdin,stdout,stderr = ssh.exec_command('show version ')
        	version=stdout.read()
		print version
		sheet.write(row, 2,version )
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

book.close()    
f1.close()
