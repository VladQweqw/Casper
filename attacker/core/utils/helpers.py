menu_options = [
    'Home page',
    'Network Scan',
    'ARP Spoofing',
    'Port Scanner',
    'ARP Spoofing (MITM)',
]

scan_types = {
    'Quick Scan': 'quick_scan',
    'Long Scan (Ports & OS)': 'long_scan'
}

# layout
overall_padding = 10
APP_WIDTH = 600
APP_HEIGHT = 700

# Font styles
title_font = ("Segoe UI", 16, "bold")
normal_font = ('Segoe UI', 12)
link_font = ('Segoe UI', 12, "italic")

def convert_host_tuple(items, isList=False):
    
    if isList:
        returnList = []

        for item in items:
            formatted_str = item[0]

            if item[1]:
                formatted_str += f" ({item[1]})"

            returnList.append(formatted_str)

        return returnList
    else:
        formatted_str = item[0]
            
        if item[1]:
            formatted_str += f" ({item[1]})"

        return formatted_str  
