import os
import paramiko
import xlsxwriter
import socket
import re
import sys
import time
from ciscoconfparse import CiscoConfParse
import getpass
import json
from sh import Command

def get_hosts(inventory_path, group_name):
    ansible_inventory = Command('ansible-inventory')
    json_inventory = json.loads(
        ansible_inventory('-i', inventory_path, '--list').stdout)

    if group_name not in json_inventory:
        raise AssertionError('Group %r not found.' % group_name)

    hosts = []
    if 'hosts' in json_inventory[group_name]:
        return json_inventory[group_name]['hosts']
    else:
        children = json_inventory[group_name]['children']
        for child in children:
            if 'hosts' in json_inventory[child]:
                for host in json_inventory[child]['hosts']:
                    if host not in hosts:
                        hosts.append(host)
            else:
                grandchildren = json_inventory[child]['children']
                for grandchild in grandchildren:
                    if 'hosts' not in json_inventory[grandchild]:
                        raise AssertionError('Group nesting cap exceeded.')
                    for host in json_inventory[grandchild]['hosts']:
                        if host not in hosts:
                            hosts.append(host)
        return hosts

devices=get_hosts('master_inventory.ini',sys.argv[1])


username = raw_input('Enter username for device login:')
password =  getpass.getpass()


book = xlsxwriter.Workbook('benchmark.xlsx')
sheet = book.add_worksheet("report")

header_format = book.add_format({'bold':True , 'bg_color':'yellow'})
header = ["Hostname","1.1.1. Enable aaa new-model","1.1.2. Enable aaa authentication login","1.1.3. Enable aaa authentication enable default","1.1.4. Set login authentication for line con 0","1.1.5. Set login authentication for line tty","1.1.6. Set login authentication for line vty","1.1.7. Set aaa accounting to log all privileged use commands using commands15","1.1.8. Set aaa accounting connection","1.1.9. Set aaa accounting exec","1.1.10. Set aaa accounting network","1.1.11. Set aaa accounting system","1.2.1. Set privilege 1 for local users","1.2.2. Set transport input ssh for line vty connections","1.2.3. Set no exec for line aux 0","1.2.4. Create access-list for use with line vty","1.2.5. Set access-class for line vty","1.2.6. Set exec-timeout to less than or equal to 10 minutes for line aux 0","1.2.7. Set exec-timeout to less than or equal to 10 minutes line console 0","1.2.8. Set exec-timeout less than or equal to 10 minutes line tty","1.2.9. Set exec-timeout to less than or equal to 10 minutes line vty","1.2.10. Set transport input none for line aux 0","1.3.1. Set the banner-text for banner exec","1.3.2. Set the banner-text for banner login","1.3.3. Set the banner-text for banner motd","1.4.1. Set password for enable secret","1.4.2. Enable service password-encryption","1.4.3. Set username secret for all local users","1.5.1. Set no snmp-server to disable SNMP when unused","1.5.2. Unset private for snmp-server community","1.5.3. Unset public for snmp-server community","1.5.4. Do not set RW for any snmp-server community","1.5.5. Set the ACL for each snmp-server community","1.5.6. Create an access-list for use with SNMP","1.5.7. Set snmp-server host when using SNMP","1.5.8. Set snmp-server enable traps snmp","1.5.9. Set priv for each snmp-server group using SNMPv3","1.5.10. Require aes 128 as minimum for snmp-server user when using SNMPv3","2.1.1.1.1. Set the hostname","2.1.1.1.2. Set the ip domain name","2.1.1.1.3. Set modulus to greater than or equal to 2048 for crypto key generate rsa","2.1.1.1.4. Set seconds for ip ssh timeout","2.1.1.1.5. Set maximimum value for ip ssh authentication-retries","2.1.1.2. Set version 2 for ip ssh version","2.1.2. Set no cdp run","2.1.3. Set no ip bootp server","2.1.4. Set no service dhcp","2.1.5. Set no ip identd","2.1.6. Set service tcp-keepalives-in","2.1.7. Set service tcp-keepalives-out","2.1.8. Set no service pad","2.2.1. Set logging on","2.2.2. Set buffer size for logging buffered","2.2.3. Set logging console critical","2.2.4. Set IP address for logging host","2.2.5. Set logging trap informational","2.2.6. Set service timestamps debug datetime","2.2.7. Set logging source interface","2.3.1.1. Set ntp authenticate","2.3.1.2. Set ntp authentication-key","2.3.1.3. Set the ntp trusted-key","2.3.1.4. Set key for each ntp server","2.3.2. Set ip address for ntp server","2.4.1. Create a single interface loopback","2.4.2. Set AAA source-interface","2.4.3. Set ntp source to loopback interface","2.4.4. Set ip tftp source-interface to the Loopback interface","3.1.1. Set no ip source-route","3.1.2. Set no ip proxy-arp","3.1.3. Set no interface tunnel","3.1.4. Set ip verify unicast source reachable-via","3.2.1. Set ip access-list extended to Forbid Private Source Addresses from External Networks","3.2.2. Set inbound ip access-group on the External Interface ","3.3.1.1. Set key chain","3.3.1.2. Set key","3.3.1.3. Set key-string","3.3.1.4. Set address-family ipv4 autonomous-system ","3.3.1.5. Set af-interface default ","3.3.1.6. Set authentication key-chain ","3.3.1.7. Set authentication mode md5 ","3.3.1.8. Set ip authentication key-cahin eigrp ","3.3.1.9. Set ip authentication mode eigrp ","3.3.2.1. Set authentication message-digest for OSPF area","3.3.2.2. Set ip ospf message-digest-key md5","3.3.4.1. Set neighbor password"]

for col, text in enumerate(header):
	sheet.write(0, col, text, header_format)



ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
config =[]
row=0
rwcount=0

def checkmatch(rvalue):
	if not rvalue:
		return "NO"
        else:
                return "YES"


for device in devices:
    row=row+1
    #column = device.split()
    #ip=column[1]
    print device
    sheet.write(row, 0,device )
    try:
	ssh.connect(device, username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
	stdin,stdout,stderr = ssh.exec_command('show version ')
	version=stdout.read()
	if not re.search('Cisco Nexus Operating System \(NX-OS\) Software', version):
		ssh.connect(device, username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
		stdin,stdout,stderr = ssh.exec_command('show running-config all')
		config = stdout.readlines()
		parse = CiscoConfParse(config)
		match1=parse.find_objects("^aaa new-model")
		r1=checkmatch(match1)
	        sheet.write(row, 1,r1 )	
                match2=parse.find_objects("^aaa authentication login")
		r2=checkmatch(match2)
                sheet.write(row, 2,r2 )
		match3=parse.find_objects("^aaa authentication enable default")
		r3=checkmatch(match3)
                sheet.write(row, 3,r3 )
		match4= parse.find_objects_w_child(parentspec=r"^line con 0", childspec=r"login authentication")
		r4=checkmatch(match4)
                sheet.write(row, 4,r4 )
		match5=parse.find_objects_w_child(parentspec=r"^line tty", childspec=r"login authentication")
		r5=checkmatch(match5)
		sheet.write(row, 5,r5 )
		match6=parse.find_objects_w_child(parentspec=r"^line vty", childspec=r"login authentication")
		r6=checkmatch(match6)
		sheet.write(row, 6,r6 )
		match46 =parse.find_objects("^aaa accounting commands")
		r46=checkmatch(match46)
		sheet.write(row, 7,r46 )
		match7=parse.find_objects("^aaa accounting connection")
		r7=checkmatch(match7)
		sheet.write(row, 8,r7 )
		match8=parse.find_objects("^aaa accounting exec")
		r8=checkmatch(match8)
		sheet.write(row, 9,r8 )
		match9=parse.find_objects("^aaa accounting network")
		r9=checkmatch(match9)
		sheet.write(row, 10,r9 )
		match10=parse.find_objects("^aaa accounting system")
		r10=checkmatch(match10)
		sheet.write(row, 11,r10) 
		rule121 ="N/A"
		sheet.write(row, 12,rule121)
		match11=parse.find_objects_w_child(parentspec=r"^line vty", childspec=r"transport input ssh")
		r11=checkmatch(match11)
		sheet.write(row, 13,r11)
		match12=parse.find_objects_w_child(parentspec=r"^line aux 0", childspec=r"no exec")
		r12=checkmatch(match12)
		sheet.write(row, 14,r12)
		match13=parse.find_objects_w_child(parentspec=r"^line vty", childspec=r"access-list")
		r13=checkmatch(match13)
		sheet.write(row, 15,r13)
		match14=parse.find_objects_w_child(parentspec=r"^line vty", childspec=r"access-class")
		r14=checkmatch(match14)
		sheet.write(row, 16,r14)
		match85=parse.find_objects_w_child(parentspec=r"^line aux", childspec=r"exec-timeout")
		if match85:
			for objchild in match85:
                                for obj in objchild.children:
                                        timeout=re.findall(r'(?<=exec-timeout)(.\d*)',obj.text)
                                        if timeout:
                                                timeoutcheck= timeout[0]
                                if timeoutcheck <= 10:
					sheet.write(row, 17,"YES")
                                else:
					sheet.write(row, 17,"NO")
                else:
			sheet.write(row,17,"N/A")

		match86=parse.find_objects_w_child(parentspec=r"^line con 0", childspec=r"exec-timeout")
		if match86:
			for objchild in match86:
				for obj in objchild.children:
					timeout=re.findall(r'(?<=exec-timeout)(.\d*)',obj.text)
					if timeout:
						timeoutcheck= timeout[0]
                        	if timeoutcheck <= 10:
					sheet.write(row, 18,"YES")
                        	else:
					sheet.write(row, 18,"NO")
                else:
			sheet.write(row, 18,"N/A")

		match87=parse.find_objects_w_child(parentspec=r"^line tty", childspec=r"exec-timeout")
		if match87:
                        for objchild in match87:
                                for obj in objchild.children:
                                        timeout=re.findall(r'(?<=exec-timeout)(.\d*)',obj.text)
                                        if timeout:
                                                timeoutcheck= timeout[0]
                                if timeoutcheck <= 10:
					sheet.write(row, 19,"YES")
                                else:
					sheet.write(row, 19,"NO")
                else:
			sheet.write(row, 19,"N/A")
                match88=parse.find_objects_w_child(parentspec=r"^line vty", childspec=r"exec-timeout")
		if match88:
			for objchild in match88:
                                for obj in objchild.children:
                                        timeout=re.findall(r'(?<=exec-timeout)(.\d*)',obj.text)
                                        if timeout:
                                                timeoutcheck= timeout[0]
                                if timeoutcheck <= 10:
					sheet.write(row, 20,"YES")
                                else:
					sheet.write(row, 20,"NO")
                else:
			sheet.write(row, 20,"N/A")
   
		match15=parse.find_objects_w_child(parentspec=r"^line aux 0", childspec=r"transport input none")
		r15=checkmatch(match15)
		sheet.write(row, 21,r15)
		
		match52=parse.find_objects("^banner exec")
		r52=checkmatch(match52)
	        sheet.write(row, 22,r52)
		match53=parse.find_objects("^banner login")
                r53=checkmatch(match53)
                sheet.write(row, 23,r53)
		match54=parse.find_objects("^banner motd")
                r54=checkmatch(match54)
                sheet.write(row,24,r54)

		match16=parse.find_objects("^enable secret")
		r16=checkmatch(match16)
		sheet.write(row,25,r16)
		match17=parse.find_objects("^service password-encryption")
		r17=checkmatch(match17)
		sheet.write(row,26,r17)
		
		match55= parse.find_objects("^username")
		for issecret in match55:
			valsec=re.findall(r'secret',issecret.text)
			if not valsec:
				sheet.write(row,27,"NO")
			else:
				sheet.write(row,27,"YES")
		match56 ="N/A"
		sheet.write(row,28,match56)
		match57=parse.find_objects_w_child(parentspec=r"^snmp-server community", childspec=r"private")
                if not match57:
			sheet.write(row,29,"YES")
                else:
			sheet.write(row,29,"NO")
		match58=parse.find_objects_w_child(parentspec=r"^snmp-server community", childspec=r"public")
		if not match58:
			sheet.write(row,30,"YES")
		else:
			sheet.write(row,30,"NO")
		match18= parse.find_objects("^snmp-server community")
		for obj in match18:
                	rw= re.findall(r'RW',obj.text)
                	if not rw:
				pass
			else:
				rwcount=rwcount+1
		if rwcount > 0:
			sheet.write(row,31,"NO")
		else:
			sheet.write(row,31,"YES")
		match59="covered by 1.5.4"
		sheet.write(row,32,match59)
		aclcount = 0
		match60a=parse.find_objects("^access-list 11")
		for acl11 in match60a:
        		if "SNMP" in acl11.text:
                		aclcount= aclcount+1

		match60b=parse.find_objects("^access-list 12")
		for acl12 in match60b:
        		if "SNMP" in acl12.text:
                		aclcount=aclcount+1
		match60c=parse.find_objects("^access-list 13")
		for acl13 in match60c:
        		if "SNMP" in acl13.text:
                		aclcount=aclcount+1
		match60d=parse.find_objects("^access-list 14")
		for acl14 in match60d:
        		if "SNMP" in acl14.text:
                		aclcount=aclcount+1
		match60e=parse.find_objects("^access-list 15")
		for acl15 in match60e:
        		if "SNMP" in acl15.text:
                		aclcount=aclcount+1

		if aclcount == 8:
        		match60="YES"
		else:
			match60="NO"

		sheet.write(row,33,match60)
		match19= parse.find_objects("^snmp-server host")
		r19=checkmatch(match19)
		sheet.write(row,34,r19)
		match20= parse.find_objects("^snmp-server enable traps snmp")
		r20=checkmatch(match20)
		sheet.write(row,35,r20)
		match61="N/A"
		sheet.write(row,36,match61)
		match62="N/A"
		sheet.write(row,37,match62)
		match21=parse.find_objects("^hostname")
		r21=checkmatch(match21)
		sheet.write(row,38,r21)
		match22=parse.find_objects("^ip domain name")
		r22=checkmatch(match22)
		sheet.write(row,39,r22)
		match63="N/A"
		sheet.write(row,40,match63)
		ssh.connect(device, username=username, password=password,timeout=5,allow_agent=False,look_for_keys=False)
		stdin,stdout,stderr = ssh.exec_command('sh ip ssh')
		match64=stdout.readlines()
		sshparse = CiscoConfParse(match64)
		sshparams=sshparse.find_objects("^Authentication timeout")
		sshversionfind=sshparse.find_objects("^SSH Enabled")
		for version in sshversionfind:
        		sshversion=re.search(r'(?<=SSH\sEnabled\s-\sversion)(.*)',version.text)
        		if float(sshversion.group(0)) == 2.0:
				sheet.write(row,43,"YES")
        		else:
                		sheet.write(row,43,"NO")

		for sshvalues in sshparams:
        		timeout=re.search(r'(?<=^Authentication\stimeout:\s)(\d*)',sshvalues.text)
        		retries=re.search(r'(?<=Authentication\sretries:\s)(\d*)',sshvalues.text)
        		if int(timeout.group(0)) == 60:
				sheet.write(row,41,"YES")
        		else:
                		sheet.write(row,41,"NO")
        		if int(retries.group(0)) == 3:
				sheet.write(row,42,"YES")
        		else:
				sheet.write(row,42,"YES")

		
		match24=parse.find_objects("^no cdp run")
		r24=checkmatch(match24)
		sheet.write(row,44,r24)
		match25=parse.find_objects("^no ip bootp server")
		r25=checkmatch(match25)
		sheet.write(row,45,r25)
		match26=parse.find_objects("^no service dhcp")
		r26=checkmatch(match26)
		sheet.write(row,46,r26)
		match27=parse.find_objects("^no ip identd")
		r27=checkmatch(match27)
		sheet.write(row,47,r27)
		match28=parse.find_objects("^service tcp-keepalives-in")
		r28=checkmatch(match28)
		sheet.write(row,48,r28)
		match29=parse.find_objects("^service tcp-keepalives-out")
		r29=checkmatch(match29)
		sheet.write(row,49,r29)
		match30=parse.find_objects("^no service pad")
		r30=checkmatch(match30)
		sheet.write(row,50,r30)
		match31=parse.find_objects("^logging on")
		r31=checkmatch(match31)
		sheet.write(row,51,r31)
		match32=parse.find_objects("^logging buffered")
		r32=checkmatch(match32)
		sheet.write(row,52,r32)
		match33=parse.find_objects("^logging console critical")
		r33=checkmatch(match33)
		sheet.write(row,53,r33)
		match34=parse.find_objects("^logging host")
		r34=checkmatch(match34)
		sheet.write(row,54,r34)
		match35=parse.find_objects("^logging trap informational")
		r35=checkmatch(match35)
		sheet.write(row,55,r35)
		match36=parse.find_objects("^service timestamps debug datetime")
		r36=checkmatch(match36)
		sheet.write(row,56,r36)
		match37=parse.find_objects("^logging source interface")
		r37=checkmatch(match37)
		sheet.write(row,57,r37)
		#match38=parse.find_objects("^ntp authenticate")
		#r38=checkmatch(match38)
		sheet.write(row,58,"N/A")
		#match39=parse.find_objects("^ntp authentication-key")
		#r39=checkmatch(match39)
		sheet.write(row,59,"N/A")
		#match40=parse.find_objects("^ntp trusted-key")
		#r40=checkmatch(match40)
		sheet.write(row,60,"N/A")
		sheet.write(row,61,"N/A")
		match42=parse.find_objects("^ntp server")
		r42=checkmatch(match42)
		sheet.write(row,62,r42)
		match66="N/A"
		sheet.write(row,63,match66)
		match67="N/A"
		sheet.write(row,64,match67)
		match68="N/A"
		sheet.write(row,65,match68)
		match69="N/A"
		sheet.write(row,66,match69)
		
		match43=parse.find_objects("^no ip source-route")
		r43=checkmatch(match43)
		sheet.write(row,67,r43)
		#match44=parse.find_objects("^no ip proxy-arp")
		#r44=checkmatch(match44)
		sheet.write(row,68,"N/A")
		#match45=parse.find_objects("^no interface tunnel")
		#r45=checkmatch(match45)
		sheet.write(row,69,"N/A")
		match70="N/A"
		sheet.write(row,70,match70)
		match71="N/A"
		sheet.write(row,71,match71)
		match72="N/A"
		sheet.write(row,72,match72)
		match73="N/A"
		sheet.write(row,73,match73)
		match74="N/A"
		sheet.write(row,74,match74)
		match75="N/A"
		sheet.write(row,75,match75)
		match76="N/A"
		sheet.write(row,76,match76)
		match77="N/A"
		sheet.write(row,77,match77)
		match78="N/A"
		sheet.write(row,78,match78)
		match79="N/A"
		sheet.write(row,79,match79)
		match80="N/A"
		sheet.write(row,80,match80)
		match81="N/A"
		sheet.write(row,81,match81)
		match82="N/A"
		sheet.write(row,82,match82)
		match83= "N/A"
		sheet.write(row,83,match83)
		match84="N/A"
		sheet.write(row,84,match84)

    except socket.error, e:
        output = "Socket error"
	sheet.write(row,5,output)
    except paramiko.SSHException:
        output = "Issues with SSH service"
	sheet.write(row,5,output)
    except paramiko.AuthenticationException:
        output = "Authentication Failed"
	sheet.write(row,5,output)
    except Exception as e: print(e)		 
        

    
book.close()    
