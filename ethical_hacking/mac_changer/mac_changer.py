#!/usr/bin/env python3

import subprocess
import optparse


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
    subprocess.call("ifconfig eth0 down", shell=True)
    subprocess.call("ifconfig eth0 hw ether 00:11:33:44:55:22", shell=True)
    subprocess.call("ifconfig eth0 up", shell=True)


options = get_arguments()
# change_mac(options.interface, options.new_mac)

ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
print(ifconfig_result)
