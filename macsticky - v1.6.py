
######################################
# Version: 1.6
# Author:  Sami Wehbi
# Github:  https://github.com/habalpy/
######################################

import os
import sys
import re
import csv
import time
import ipaddress
import netmiko
from netmiko import ConnectHandler
        
def findMACAddress(str):
    cisco_mac_regex = "([a-fA-F0-9]{4}[\.]?)"
    p = re.compile(cisco_mac_regex)
    result = re.findall(p, str)
    result_joined = ''.join(result)
    #print (result_joined)
    add_static_mac.append(result_joined)
    return result_joined
    
def checkMACAddress(str):
    result = re.match(r"([a-fA-F0-9]{4}[\.]?)",str)
    if result == True:
        return(bool(result))
    else:
        return(bool(result))
       
def convert_list_to_string(list_object, seperator=''):
    return seperator.join(list_object)

try:
    with open('DEVICE-LIST.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print ("SKIPPING FIRST ROW")
                line_count += 1
            else:                
                config_portsec_commands = ["interface FastEthernet1/10", "switchport mode access", "switchport access vlan 10", "switchport port-security", "switchport port-security mac-address sticky"]
                add_static_mac = ["switchport port-security mac-address sticky "] 
                host = convert_list_to_string(row[1])
                device_ip = convert_list_to_string(row[2])
                svi = convert_list_to_string(row[3])                
                device = ConnectHandler(device_type='cisco_ios', ip=host, username='cisco', password='cisco', secret='cisco')
                device.enable()
                output1 = device.send_command("show mac address-table interface FastEthernet1/10")
                print (host)
                print ("##########\n")
                check_mac_value = findMACAddress(output1)
                MACCHECK = checkMACAddress(check_mac_value)
                line_count += 1
                print ("count added")
                if MACCHECK == True:
                    static_conf = ''.join(add_static_mac)
                    config_portsec_commands.append(static_conf)
                    outF = open("SwitchLog-" + host + ".txt", "a")
                    output2 = device.send_command("show run interface FastEthernet1/10")
                    outF.write("Switch " + host + " Pre Port Config Change # \n")
                    outF.write("\n")
                    outF.write(output2)
                    outF.write("\n")
                    outF.write("################\n")
                    outF.write("################\n")
                    configdev = device.send_config_set(config_portsec_commands)
                    output3 = device.send_command("show run interface FastEthernet1/10")
                    outF.write("Switch " + host + " After Port Config Change # \n")
                    outF.write("\n")
                    outF.write(output3)
                    outF.write("\n")
                    outF.write("################\n")
                    outF.write("################\n")
                    print (host + " Completed")
                    device.send_command("write memory\n")
                    device.disconnect()
                    operationLOG = open("OperationLog.txt", "a")
                    operationLOG.write("Switch " + host + " Completed \n")
                elif MACCHECK == False:
                    print ("NULL MAC ADDRESS")
                    outF = open("SwitchLog-" + host + ".txt", "a")
                    output4 = device.send_command("show run interface FastEthernet1/10")
                    outF.write("\n")
                    outF.write(output4)
                    outF.write("\n")
                    outF.write("################\n")
                    outF.write("################\n")
                    remove_vlan_interface_commands = ["no interface vlan 10"]
                    config_vlan_interface_commands = ["interface vlan 10", "no shutdown"]
                    add_svi = ["ip address "," 255.255.255.0"]                
                    add_svi.insert(1,svi)
                    oneliner = ''.join(add_svi)
                    config_vlan_interface_commands.append(oneliner)
                    print(add_svi)
                    print(oneliner)
                    print(config_vlan_interface_commands)
                    configdev = device.send_config_set(config_portsec_commands)
                    configdev2 = device.send_config_set(config_vlan_interface_commands)
                    time.sleep(2)
                    output4 = device.send_command("ping " + device_ip + " repeat 5")
                    configdev3 = device.send_config_set(remove_vlan_interface_commands)
                    output3 = device.send_command("show run interface FastEthernet1/10")
                    outF.write("Switch " + host + " After Port Config Change # \n")
                    outF.write("\n")
                    outF.write(output3)
                    outF.write("\n")
                    outF.write("################\n")
                    outF.write("################\n")
                    print (host + " Completed")
                    operationLOG = open("OperationLog.txt", "a")
                    operationLOG.write("Switch " + host + " Completed \n")
                    device.send_command("write memory\n")
                    time.sleep(2)
                    device.disconnect()
                else:
                    print("NOTHING WAS DONE to host" + host)
        print(f'Processed {line_count} lines.')
except:
    print ("\nBroken")
