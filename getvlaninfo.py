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

book = xlsxwriter.Workbook('VLANinfo.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","IP Address","VLAN ID","VLAN Description","VLAN IP & MASK"]
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
        stdin,stdout,stderr = ssh.exec_command('sh run')
        hostname = stdout.readlines()
        runconfigparse = CiscoConfParse(hostname)
        hostnamefind = runconfigparse.find_objects("^hostname")
        for hostname in hostnamefind:
                hostnameval=re.search(r'(?<=hostname\s)(\S*)',hostname.text)
		sheet.write(row,0,hostnameval.group(0))
		sheet.write(row,1,column[1])
	ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
        stdin,stdout,stderr = ssh.exec_command('show run vlan')
        arpoutput=stdout.readlines()
        configparse = CiscoConfParse(arpoutput)
        vlanparams=configparse.find_objects("^vlan")
	vlanname=configparse.find_objects("name")
        for vlan,name in zip(vlanparams,vlanname):
                row=row+1
                vlanidfind=re.search(r'(^vlan\s\d*)',vlan.text)
                vlanid=vlanidfind.group(0)
		sheet.write(row,0,hostnameval.group(0))
                sheet.write(row,1,column[1])
                sheet.write(row,2,vlanid)
		vlannamefind=re.search(r'(?<=name)(.*)',name.text)
                nameid=vlannamefind.group(0)
                sheet.write(row,3,nameid)


	vlandescp = runconfigparse.find_objects(r"^interface Vlan")
	for descp in vlandescp:
		row=row+1
		sheet.write(row,0,hostnameval.group(0))
                sheet.write(row,1,column[1])

		sheet.write(row,2,descp.text)
		for child in descp.children:
			descpfind=re.search(r'(?<=description)(.*)',child.text)
			if descpfind:
				description=descpfind.group(0)
				sheet.write(row,3,description)
			
			vlanipfind=re.search(r'(?<=ip address)(.*)',child.text)
			if vlanipfind:
				vlanip=vlanipfind.group(0)
				sheet.write(row,4,vlanip)
	
    except socket.error, e:
	print e
    except paramiko.SSHException, ssj:
	print ssj
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
	print output
    except Exception as e: print(e)
    
book.close()    
f1.close()
