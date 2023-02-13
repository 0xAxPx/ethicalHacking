#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please, specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please, specify a new mac, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode("UTF-8"))

    if current_mac:
        return current_mac.group(0)
    else:
        print("MAC address was not found!")


options = get_arguments()

# get current MAC address
mac = current_mac(options.interface)
print("Current MAC address => " + str(mac))

# change MAC address
change_mac(options.interface, options.new_mac)
mac = current_mac(options.interface)

if mac == options.new_mac:
    print("[+] MAC address was changed successfully to => " + mac)
else:
    print("[-] MAC address was not changed")
