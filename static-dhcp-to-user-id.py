#!/usr/bin/python

from jxmlease import Parser
from lxml import etree
from jnpr.junos import Device

### Update IP, Username and password fields ###
ex_switch = 'ex_ip_address'
ex_user = 'ex_username'
ex_password = 'ex_password'

srx_firewall = 'srx_ip_address'
srx_user = 'srx_username'
srx_password = 'srx_password'

myparser = Parser()

ex = Device(host=ex_switch,user=ex_user,password=ex_password)
ex.open()
config = etree.tostring(ex.rpc.get_configuration())


srx = Device(host=srx_firewall,user=srx_user,password=srx_password)
srx.open()
users = etree.tostring(srx.rpc.get_userfw_local_auth_table_all())

#Delete all existing users
for (_, _, user_entry) in myparser(users, generator=['local-authentication-info']):
 existing_ip_address = (user_entry['ip-address']).get_cdata()
 user_del_command = "request security user-identification local-authentication-table del ip-address " + str(existing_ip_address)
 srx.cli(command=user_del_command,format='text', warning=False)

#Read static users based on configuration in EX-Series DHCP server 
for (_, _, static_entry) in myparser(config, generator=['static-binding']):
 mac = (static_entry['name']).get_cdata()
 host_name = (static_entry['host-name']).get_cdata()
 ip_address = (static_entry['fixed-address']['name']).get_cdata()
 user_add_command = "request security user-identification local-authentication-table add ip-address " + str(ip_address) + " user-name " + str(host_name)
 srx.cli(command=user_add_command,format='text', warning=False)
 
ex.close()
srx.close()


