import os
import paramiko
import xlsxwriter
import socket
import re
import sys
import getpass
from ciscoconfparse import CiscoConfParse
from multiprocessing import Pool


username = raw_input('Enter username for device login:')
password =  getpass.getpass()

f1 = open('device2.txt','r')

book = xlsxwriter.Workbook('VLANinfo.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","IP Address","VLAN ID","VLAN Description","VLAN IP"]
for col, text in enumerate(header):
	sheet.write(0, col, text, header_format)



devices = f1.readlines()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
deviceslist = []
data= []

for device in devices:
    column = device.split()
    deviceslist.append(column[1])
    #print column[0]

def processfunc(devicelist):
    try:
	print devicelist
	ssh.connect(devicelist, username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
        stdin,stdout,stderr = ssh.exec_command('sh run')
        hostname = stdout.readlines()
	runconfigparse = CiscoConfParse(hostname)
        hostnamefind = runconfigparse.find_objects("^hostname")
        for hostname in hostnamefind:
                hostnameval=re.search(r'(?<=hostname\s)(\S*)',hostname.text)
		data.append(hostnameval.group(0)+".hostname")
		print hostnameval.group(0)
	ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
        stdin,stdout,stderr = ssh.exec_command('show run vlan')
        arpoutput=stdout.readlines()
        configparse = CiscoConfParse(arpoutput)
        vlanparams=configparse.find_objects("^vlan")
	vlanname=configparse.find_objects("name")
        for vlan,name in zip(vlanparams,vlanname):
                vlanidfind=re.search(r'(^vlan\s\d*)',vlan.text)
                vlanid=vlanidfind.group(0)
		data.append(vlanid+".vid")
		vlannamefind=re.search(r'(?<=name)(.*)',name.text)
                nameid=vlannamefind.group(0)
		data.append(nameid+".descp")


	ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
	stdin,stdout,stderr = ssh.exec_command('show ip int brief')
	arpoutput=stdout.readlines()
        configparse = CiscoConfParse(arpoutput)
        vlanparams=configparse.find_objects("^Vlan")
	for vlan in vlanparams:
		row=row+1
		vlanidfind=re.search(r'(^Vlan\d*)',vlan.text)
		vlanid=vlanidfind.group(0)
		sheet.write(row,2,vlanid)
		if vlanid:
			ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
       			stdin,stdout,stderr = ssh.exec_command('show run interface'+" "+vlanid)
			vlanoutput = stdout.readlines()
			vlanconfigparse = CiscoConfParse(vlanoutput)
			vlandescp = vlanconfigparse.find_objects("description")
			for descp in vlandescp:
				descpfind=re.search(r'(?<=description)(.*)',descp.text)
				description=descpfind.group(0)
				#print description
				sheet.write(row,3,description)
			vlanipaddress = vlanconfigparse.find_objects("ip address")
			for vlanipaddr in vlanipaddress:
				vlanipfind=re.search(r'(?<=ip address)(.*)',vlanipaddr.text)
				vlanip=vlanipfind.group(0)
				#print vlanip	
				sheet.write(row,4,vlanip)
			
	
    except socket.error, e:
        output = "Socket error"
	print output
    except paramiko.SSHException:
        output = "Issues with SSH service"
	print output
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
	print output
    except Exception as e: print(e)
    
    return data



pool = Pool(9)
results=pool.map(processfunc,deviceslist, 1)
pool.close()
pool.join()

row=0
for result in results:
	for listval in result:
		row=row+1
		if 'descp' in listval:
			host=listval.replace('.descp','')
			print host
			sheet.write(row,3,host)




book.close()
f1.close()

