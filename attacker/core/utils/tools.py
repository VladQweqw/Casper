import core.utils.state as state
from core.utils.logger import log
from core.utils.helpers import scan_types

from scapy.all import *

if state.client_details['os'] == 'Windows':
    from scapy.arch.windows import get_windows_if_list

import nmap
import psutil
import ipaddress

def network_scan(network_ip, netmask='24', iface=None, scan_type='quick_scan', table_shown=False):
    """
        network_ip: x.x.x.x, is the network ip on the target iface
        netmask: /24, default, works together with network_ip
        iface: None/interface: the interface on which to make the scans
        scan_type: Scan type, scan type to operate
        table_shown: Boolean - Returns a tuple (ip, mac, ports, os) that can be shown in a table
    """

    arguments = "-sn"
    if scan_type not in scan_types.values():
        return False, f"Invalid scan type: {scan_type}"
    
    if scan_type == 'long_scan':
        arguments = "-sS -v -O"

    if iface is not None:
        arguments += " " + iface

    if network_ip is None or netmask is None:
        log(message=f"Invalid network IP or netmask: {network_ip}/{netmask}", severity='ERROR')
        return False, "Invalid Network IP or Netmask"

    complete_resp = []
    tuple_resp = []    
    nm = nmap.PortScanner()

    try:
        log(message=f"Network ({scan_type}) scan started on {network_ip}/{netmask}")

        nm.scan(hosts=f"{network_ip}/{netmask}", arguments=arguments, sudo=state.client_details['os'] == 'Linux')
        for host in nm.all_hosts():
            if nm[host]['status']['state'] == 'up':
                ports = {}
                mac = 'None'
                os = 'None'
                ipv4 ="None"
                print(nm[host])

                if 'tcp' in nm[host]:
                    for open_port, type_of_port in nm[host]['tcp'].items():
                        ports[str(open_port)] = type_of_port['name']
                
                if 'mac' in nm[host]['addresses']:
                    mac = nm[host]['addresses']['mac']

                if 'osmatch' in nm[host]:
                    os = nm[host]['osmatch'][0]['name']

                if 'ipv4' in nm[host]['addresses']:
                    ipv4 = nm[host]['addresses']['ipv4']

                if table_shown:
                    tuple_resp.append(
                        (ipv4, mac, ",".join(ports), os),
                    )
                else:
                    complete_resp.append(
                        {
                            'ipv4': ipv4,
                            'mac': mac,
                            'ports': ports,
                            'os':os
                        }
                    )

        log(message=f"Network scan ({scan_type}) completed on {network_ip}/{netmask}, {len(nm.all_hosts())} targets found")

        if table_shown:
            state.scanned_targets_tuple = tuple_resp
            return True, tuple_resp
        
        state.scanned_targets = complete_resp
        return True, complete_resp

    except nmap.PortScannerError as e:
        print(f"Nmap error: {e}")
        return False, e
    except Exception as e:
        return False, e

def port_scanner(target_ip, port_range='22-443'):
    print("Starting scanning ports...")
    nm = nmap.PortScanner()
    nm.scan(target_ip, port_range)

    target = nm[target_ip]

    # get device info
    device_hostname = target['hostnames'][0]['name'] or "No name"
    device_type = target['hostnames'][0]['type'] or "No Type"
    IPv4_address = target['addresses']['ipv4'] or "No IP"
    MAC_address = target['addresses']['mac'] or "No MAC"
    vendor = target['vendor'][MAC_address] or "No vendor"
    open_ports = target['tcp']

    # print info
    print(f"Hostname: {device_hostname}, {device_type}")
    print(f"IPv4: {IPv4_address}, MAC: {MAC_address}")
    print(f"Vendor: {vendor}")
    for port, state in open_ports.items():
        print(f"""Port: {port}, state: {state['state']}, name: {state['name']}, {state['product']}""")

def get_interfaces():
    interfaces = []
    brief_interfaces = []

    for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family.name == 'AF_INET':
                    network = ipaddress.IPv4Network(f"{addr.address}/{addr.netmask}", strict=False)

                    interface_parsed_obj = {
                        "interface": iface,
                        'interface_with_ip': f"{iface} ({addr.address})",
                        'network_ip': network.network_address,
                        'host_ip': addr.address,
                        'netmask': network.netmask,
                        'netprefix': network.prefixlen,
                        'formatted': network,
                    }
                    
                    if state.client_details['os'] == "Windows":
                        windows_iface_object = next((item for item in get_windows_if_list() if item['name'] == iface), '') 
                        interface_parsed_obj['interface'] = fr"\\Device\\NPF_{windows_iface_object['guid']}"
                    
                    print(interface_parsed_obj)

                    # create a list of interfaces
                    interfaces.append(interface_parsed_obj)
                    brief_interfaces.append(f"{iface} ({addr.address})")

    return interfaces, brief_interfaces
