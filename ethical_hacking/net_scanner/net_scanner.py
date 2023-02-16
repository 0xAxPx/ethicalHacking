#!/usr/bin/env python3

import scapy.all as scapy
import argparse as arg

#Parse entering arguments
def get_arguments():
    parser = arg.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range")
    options = parser.parse_args()
    return options

#Search all clients machine by IP in the network
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    arp_request.show()
    #broadcast MAC address of destination
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    #Client IP and MAC list
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------------------")
    for client in results_list:
        print(client['ip'] + "\t\t" + client['mac'])

options = get_arguments()
print_result(scan(options.target))

