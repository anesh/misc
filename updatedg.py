import bigsuds

className = '/E-Commerce_APP-DB_DMZ/underdevdg'

f1 = open('parkedtest.txt','r')
lines = f1.readlines()

b = bigsuds.BIGIP(hostname = '10.17.119.108',username = 'anesh.ponnarasseryke', password = 'Chakki & chakkumon',)

for line in lines:
	b.LocalLB.Class.add_string_class_member(class_members = [{'members': [line.strip()], 'name': className}])
