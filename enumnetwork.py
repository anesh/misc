import os
import paramiko
import socket
import re
import sys
import time
import getpass
from netaddr import *

ipsubnet = raw_input('Provide ip Subnet:')


username = raw_input('Enter username for device login:')
password =  getpass.getpass()





ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ip = IPNetwork(ipsubnet)
ip_list = list(ip)
for ip in ip_list:
	try:
		print "connecting to", ip
        	ssh.connect(ip, username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
        	stdin,stdout,stderr = ssh.exec_command('show version ')
        	version=stdout.read()
		print version
    	except socket.error, e:
        	output = "Socket error"
    	except paramiko.SSHException:
        	output = "Issues with SSH service"
   	except paramiko.AuthenticationException:
        	output = "Authentication Failed"
    	except: 
        	print "error occured"   
        	continue

