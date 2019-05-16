import requests
requests.packages.urllib3.disable_warnings()
from f5.bigip import ManagementRoot

b = ManagementRoot('192.168.190.130', 'admin', 'password', token=True)

'''
###pools example
pools=b.tm.ltm.pools.get_collection()
for pool in pools:
    print pool.name
    for member in pool.members_s.get_collection():
         print member.name'''



'''
#get profiles on virtual
virtual = b.tm.ltm.virtuals.virtual.load(partition='Common', name='ubuntu_apache_8443')
for profile in virtual.profiles_s.get_collection():
	print profile.name
