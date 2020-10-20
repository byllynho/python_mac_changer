#!usr/bin/env python
    
import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Specify the interface of which you want to change the MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac", help="Specify a random MAC address you would like to the interface to use.")
    (options, arguments) = parser.parse_args()
    print(options)
    if not options.interface():
        parser.error("[-] Error: interface not specified, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Error: MAC address not specified, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    regex_mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if regex_mac_search_result:
        return regex_mac_search_result.group(0)
    else:
        print("[-] Error: could not read MAC address.")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("The current MAC Address = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
	print("The MAC address successfully changed to " + current_mac)
else:
	print("Error: The MAC address did not get changed.")
