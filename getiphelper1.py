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

f1 = open('device.txt','r')

book = xlsxwriter.Workbook('iphelperphysical.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["DeviceIP","Hostname","Interface","IP Address","IPHelper address","Comments"]
for col, text in enumerate(header):
	sheet.write(0, col, text, header_format)



devices = f1.readlines()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
config =[]
row=0
timeout = 20
endtime = time.time() + timeout

for device in devices:
    row=row+1
    column = device.split()
    ip=column[1]
    print column[0]
    sheet.write(row, 0,ip )
    sheet.write(row, 1,column[0] )
    try:
	ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
	stdin,stdout,stderr = ssh.exec_command('show version ')
	version=stdout.read()
	if not re.search('Cisco Nexus Operating System \(NX-OS\) Software', version):
		ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
		stdin,stdout,stderr = ssh.exec_command('show running-config ')
		''' 
		while not stdout.channel.eof_received:
			if time.time() > endtime:
				sheet.write(row, 5,"EOF not reached" )
				#stdout.channel.close()
			break
		'''
		config = stdout.readlines()
		parse = CiscoConfParse(config)
		match= parse.find_objects_w_child(parentspec=r"^interface", childspec=r"ip helper-address")
		for parent in match:
			row=row+1
			print parent.text
			sheet.write(row,2,parent.text )
			for child in parent.children:
				ipaddress=re.findall(r'(?<=ip address)(.*)',child.text)
				helpers=re.findall(r'(?<=ip helper-address )(.*)',child.text)
				for value in ipaddress:
                                	print value
                                	sheet.write(row,3,value)
				for helper in helpers:
					print helper
					sheet.write(row,4,helper)
	else:
		ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
		stdin,stdout,stderr = ssh.exec_command('show running-config ')
                config = stdout.readlines()
                parse = CiscoConfParse(config)
                match= parse.find_objects_w_child(parentspec=r"^interface", childspec=r"ip dhcp relay address")
                for parent in match:
                        row=row+1
                        print parent.text
                        sheet.write(row,2,parent.text )
                        for child in parent.children:
                                ipaddress=re.findall(r'(?<=ip address)(.*)',child.text)
                                helpers=re.findall(r'(?<=ip dhcp relay address )(.*)',child.text)
                                for value in ipaddress:
                                        print value
                                        sheet.write(row,3,value)
                                for helper in helpers:
                                        print helper
                                        sheet.write(row,4,helper)

    except socket.error, e:
        output = "Socket error"
	sheet.write(row,5,output)
	ssh.close()
    except paramiko.SSHException:
        output = "Issues with SSH service"
	sheet.write(row,5,output)
	ssh.close()
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
	sheet.write(row,5,output)
	ssh.close()
    except: 
        print "error occured"   
	ssh.close()
        continue

    
book.close()    
f1.close()
