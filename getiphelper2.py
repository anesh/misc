import os
import paramiko
import xlsxwriter
import re
import sys
import time
import getpass
import socket
from ciscoconfparse import CiscoConfParse

username = raw_input('Enter username for device login:')
password =  getpass.getpass()

f1 = open('device1.txt','r')
vlans=""
version=""
vlan=""
row=0

try:
	book = xlsxwriter.Workbook('iphelperv1.xlsx')
	sheet = book.add_worksheet("report")

	header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
	header = ["DeviceIP","Hostname","Interface","IPaddress","IPHelper address","Comments"]
	for col, text in enumerate(header):
    		sheet.write(0, col, text, header_format)


	devices = f1.readlines()
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


	for device in devices:

    		not_done = True
    		row=row+1
    		column = device.split()
    		ip=column[1]
    		sheet.write(row, 0,ip )
    		try:
        		ssh.connect(column[1], username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
        		remote_conn = ssh.invoke_shell()
        		output = remote_conn.recv(1000)
			remote_conn.send("term length 0")
        		remote_conn.send("\n")
			print column[0]
                        sheet.write(row, 1,column[0] )
			not_done = True
        		remote_conn.send("show running-config")
        		remote_conn.send("\n")
			i = 1
			time.sleep(1)
			while (not_done) and (i <= 30):
				time.sleep(4)
				i+=1
				if remote_conn.recv_ready():
        				config = remote_conn.recv(65535)
				else:
					not_done = False
			lines = config.splitlines()
			parse = CiscoConfParse(lines)
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



        		ssh.close()
    		except socket.error, e:
        		output = "Socket error"
        		sheet.write(row,5 ,output )
    		except paramiko.SSHException:
        		output = "Issues with SSH service"
        		sheet.write(row,5 ,output )
    		except paramiko.AuthenticationException:
        		output = "Authentication Failed"
        		sheet.write(row,5 ,output )
		except Exception as e: 
			print(e) 
        		continue
    
   
	book.close()    
	f1.close()
except:
	print "error occured"	
