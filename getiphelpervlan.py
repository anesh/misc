import os
import paramiko
import xlsxwriter
import re
import sys
import time
import getpass
import socket

username = raw_input('Enter username for device login:')
password =  getpass.getpass()

f1 = open('device.txt','r')
vlans=""
version=""
vlan=""
row=0

try:
	book = xlsxwriter.Workbook('iphelper.xlsx')
	sheet = book.add_worksheet("report")

	header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
	header = ["DeviceIP","Hostname","VLANID","SVI","IPHelper address","Comments"]
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
        		remote_conn.send("show ip int brief | i Vlan")
        		remote_conn.send("\n")
			while (not_done):
				time.sleep(1)
				if remote_conn.recv_ready():
        				vlan = remote_conn.recv(65535)
				else:
					not_done = False

			matchlist=re.findall(r'(^Vlan\d*)',vlan,re.MULTILINE)        
			for match in matchlist:
				row=row+1
				not_done = True
				print match
				sheet.write(row,2 ,match )
				remote_conn.send('show ip int '+str(match))
				remote_conn.send("\n")
				while (not_done):
                			time.sleep(1)
                			if remote_conn.recv_ready():
                        			vlans = remote_conn.recv(65535)
						svi=re.findall(r'(?<=Internet address is)(.*)',vlans)
						iphelper=re.findall(r'(?<=Helper addresses are )(.*)(?=Directed broadcast)',vlans,re.DOTALL)
						for match1 in svi:
                                        		print match1
                                        		sheet.write(row,3 ,match1 )
                                		for match2 in iphelper:
                                        		print match2
                                        		sheet.write(row,4 ,match2 )

                			else:
                        			not_done = False

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
		except: 
			print "error occured"	
        		continue
    
   
	book.close()    
	f1.close()
except:
	print "error occured"	
