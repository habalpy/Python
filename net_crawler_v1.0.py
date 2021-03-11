
##############################################
# Version: 1.0
# Author:  Sami Wehbi
# Github:  https://github.com/habalpy/Python/
##############################################

import os
import sys
import re
import ipaddress
import netmiko
from netmiko import ConnectHandler

      
def convert_list_to_string(list_object, seperator=''):
    return seperator.join(list_object)
    

def searchMAC(node,mac_addr_node):
    SWITCH_GET_PORT = {
        'device_type': 'cisco_ios',
        'ip': node,
        'username': 'cisco',
        'password': 'cisco',
        'port' : 22,          # optional, defaults to 22
        'secret': 'cisco',     # optional, defaults to ''
        }
        
    net_connect_switch = ConnectHandler(**SWITCH_GET_PORT)
    output1 = net_connect_switch.send_command("show mac address-table | i " + mac_addr_node )
    interface_node = re.findall(r'[A-Za-z]+[0-9]+[/]+[0-9]', output1)
    print(interface_node)
    interface = convert_list_to_string(interface_node,'')
    output2 = net_connect_switch.send_command('show cdp neighbors ' + interface + ' detail')
    print (output2)
    print ("Function Run Complete")

while True:

    try:
        node = input("INPUT Device IPv4 Address for Network Search: ")
        vrf = input("INPUT VRF for Network Search (LEAVE BLANK IF NONE): ")
        checkip = ipaddress.ip_address(str(node)) #validates either ip is ipv4 or 6
        outF = open("Search" + node + ".txt", "a")
        PE_GET_ROUTE = {
            'device_type': 'cisco_ios',
            'ip':   '192.168.233.251',
            'username': 'cisco',
            'password': 'cisco',
            'port' : 22,          # optional, defaults to 22
            'secret': 'cisco',     # optional, defaults to ''
        }
        try:
            if vrf != "":
                net_connect = ConnectHandler(**PE_GET_ROUTE)
                #output = net_connect.send_command('show ip bgp vpnv4 vrf ' + vrf + ' ' + node + ' bestpath')
                output = net_connect.send_command('show ip route vrf '+ vrf + ' ' + node)
                nexthop = output.split('from', maxsplit=1)[-1]\
                               .split(maxsplit=1)[0]
                print("NODE NEXT HOP PE = " + nexthop)
                outF.write("NODE NEXT HOP PE = " + nexthop)
            else:
                net_connect = ConnectHandler(**PE_GET_ROUTE)
                output = net_connect.send_command('show ip route ' + node)
                nexthop = output.split('from', maxsplit=1)[-1]\
                               .split(maxsplit=1)[0]
                print("NODE NEXT HOP PE (NODE FACING PE) = " + nexthop)
                outF.write("NODE NEXT HOP PE = " + nexthop)
                  
        except ValueError:  #catch error for invalid ip format
            print('Couldnt Connect'.format)
            break
            
        try:     
            checknexthop = ipaddress.ip_address(str(nexthop))
            PE_NEXTHOP_GET_MAC = {
                'device_type': 'cisco_ios',
                'ip': nexthop,
                'username': 'cisco',
                'password': 'cisco',
                'port' : 22,          # optional, defaults to 22
                'secret': 'cisco',     # optional, defaults to ''
            }

            net_connect_nh = ConnectHandler(**PE_NEXTHOP_GET_MAC)
            if vrf != "":
                output2 = net_connect_nh.send_command('show ip arp vrf ' + vrf + ' ' + node)
                re.findall(r'\S+', output2)
                s = re.findall(r'\S+', output2)
                if s != []:                
                    print ("NODE MAC ADDRESS = " + s[11])
                    outF.write("\n")
                    outF.write("NODE MAC ADDRESS = " + s[11])
                    outF.write("\n")
                    break
            else:
                output2 = net_connect_nh.send_command('show ip arp ' + node)
                re.findall(r'\S+', output2)
                s = re.findall(r'\S+', output2)
                node_mac_address = s[11]
                if s != []:
                    print ("NODE MAC ADDRESS = " + s[11])
                    outF.write("\n")
                    outF.write("NODE MAC ADDRESS = " + s[11])
                    outF.write("\n")
                    output3 = net_connect_nh.send_command('show ip cef ' + node)
                    interface_node = re.findall(r'[A-Za-z]+[0-9]+[/]+[0-9]', output3)
                    #print (interface_node)
                    interface_2 =convert_list_to_string(interface_node,'')
                    output4 = net_connect_nh.send_command('show cdp neighbors ' + interface_2 + ' detail')
                    #print (output4)
                    switch_1 = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', output4)
                    switch_ip_2 = convert_list_to_string(switch_1[0],'')
                    #print (switch_ip_2)
                    searchMAC(switch_ip_2,node_mac_address)
                else:
                     print('NO ARP ENTRY FOUND') 
                     break
        except ValueError:  #catch error for invalid ip format
            print('NEXT HOP INVALID'.format)
            break       
        
    except ValueError:  #catch error for invalid ip format
        print('invalid ip '.format(node))
        continue
