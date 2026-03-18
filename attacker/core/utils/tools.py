from scapy.all import *
from scapy.arch.windows import get_windows_if_list

import nmap
import psutil
import ipaddress

def network_scan(network_ip, netmask='24', iface=None, table_shown=False):
    """
        iface: None/interface: the interface on which to make the scans
        parsed_return (ip, mac): returns a list of tuples for each ip and its MAC
        table_shown: Boolean - Returns a tuple that can be shown in a table
    """

    arguments = "-sS -v -O"

    if iface is not None:
        arguments += " " + iface

    if network_ip is None or netmask is None:
        return False, "Invalid Network IP or Netmask"

    resp = []
    print(f"{network_ip}/{netmask}", arguments)
    
    nm = nmap.PortScanner()

    try:
        nm.scan(hosts=f"{network_ip}/{netmask}", arguments=arguments)
        for host in nm.all_hosts():
            if nm[host]['status']['state'] == 'up':
                ports = {}
                for open_port, type_of_port in nm[host]['tcp'].items():
                    ports[str(open_port)] = type_of_port['name']

                if table_shown:
                    
                    mac = 'None'
                    if 'mac' in nm[host]['addresses']:
                        mac = nm[host]['addresses']['mac']

                    resp.append(
                        (nm[host]['addresses']['ipv4'], mac, ",".join(ports), nm[host]['osmatch'][0]['name']),
                    )
                else:
                    resp.append(
                    {
                        'addresses': nm[host]['addresses'],
                        'ports': ports,
                        'os': nm[host]['osmatch'][0]['name']
                    }
                )
    
    except nmap.PortScannerError as e:
        print(f"Nmap error: {e}")
        return False, e
    except Exception as e:
        return False, e

    return True, resp


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
    
    windows_ifaces = get_windows_if_list()

    for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family.name == 'AF_INET':
                    network = ipaddress.IPv4Network(f"{addr.address}/{addr.netmask}", strict=False)
                    windows_iface_object = next((item for item in windows_ifaces if item['name'] == iface), '') 

                    # create a list of interfaces
                    interfaces.append({
                        "interface": iface,
                        'network_ip': network.network_address,
                        'host_ip': addr.address,
                        'netmask': network.netmask,
                        'netprefix': network.prefixlen,
                        'formatted': network,
                        'windows_interface': fr"\\Device\\NPF_{windows_iface_object['guid']}"
                    })

                    brief_interfaces.append(iface)

    return interfaces, brief_interfaces