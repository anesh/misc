import bigsuds

className = '/E-Commerce_APP-DB_DMZ/redirectdg'

f1 = open('redirecttest.txt','r')
lines = f1.readlines()

b = bigsuds.BIGIP(hostname = '10.17.119.108',username = 'anesh.ponnarasseryke', password = 'Chakki & chakkumon',)

for line in lines:
	column = line.split()
	value=column[1]
	b.LocalLB.Class.add_string_class_member(class_members = [{'members': [column[0]], 'name': className}])
 	b.LocalLB.Class.set_string_class_member_data_value(class_members = [{'members': [column[0]] , 'name': className}], values=[[value]] )
