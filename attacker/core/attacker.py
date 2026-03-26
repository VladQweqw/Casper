import core.utils.attacks as attacks
import core.utils.tools as tools

from core.utils.helpers import menu_options, overall_padding, APP_WIDTH, APP_HEIGHT
import core.utils.panels as panels
import core.utils.state as state

import platform
import psutil
import ipaddress
import ctypes

import tkinter as tk
from tkinter import ttk
from tkinter import font

import sv_ttk

root = tk.Tk()
sv_ttk.set_theme('dark')

root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
root.minsize(APP_WIDTH, APP_HEIGHT)
root.maxsize(APP_WIDTH, APP_HEIGHT)

# App title / icon
root.title("Casper - Pentesting tool")
# root.iconbitmap("public/images/logo.ico")s

# font
default_font = font.nametofont("TkDefaultFont")
default_font.config(family='Segoe UI', size=12)

# get client OS
state.client_details['os'] = platform.uname()[0]
state.client_details['system_name'] = platform.uname()[1]
state.client_details['release'] = platform.uname()[2]
state.client_details['release'] = platform.uname()[4]

# grid layout
# 2 columns, 1fr 1fr
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# 3 rows
root.rowconfigure(0, weight=0, minsize=75)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=1)

header_frame = ttk.Frame(root, padding=overall_padding)
attackComboFrame = ttk.Frame(root, padding=overall_padding)
interfaceComboFrame = ttk.Frame(root, padding=overall_padding)

header_frame.grid(row=0, column=0, sticky='nsew', columnspan=2)
attackComboFrame.grid(row=1, column=0, sticky='nsew')
interfaceComboFrame.grid(row=1, column=1, sticky='nsew')

# app title
image = tk.PhotoImage(file='public/images/hero_logo.png')
appTitle = ttk.Label(header_frame, image=image)
appTitle.place(relx=0.5, rely=.5, anchor="center")

# Attack dropdown
attacksLabel = tk.Label(
    attackComboFrame,
    text="Choose attack type")
attacksLabel.grid(row=0, column=0, sticky='nswe', pady=(0, 5))

attacksText = tk.StringVar(value=menu_options[0])
attackCombo = ttk.Combobox(
    attackComboFrame, 
    textvariable=attacksText,
    values=menu_options,
    state='readonly',
    width=30
)
attackCombo.grid(row=1, column=0, sticky='ew')
state.current_attack_option = menu_options[0]

# Interface dropdown
interfacesLabel = tk.Label(
    interfaceComboFrame,
    text="Choose interface")
interfacesLabel.grid(row=0, column=0, sticky='nwse', pady=(0, 5))

# get interfaces
interfaces, brief_interfaces = tools.get_interfaces()
interfacesText = tk.StringVar(value=brief_interfaces[0])
interfacesCombo = ttk.Combobox(
    interfaceComboFrame, 
    textvariable=interfacesText,
    values=brief_interfaces,
    state='readonly',
    width=30
)
interfacesCombo.grid(row=1, column=0, sticky='we')
state.current_interface_option = brief_interfaces[0]
state.current_interface_object = next((item for item in interfaces if item['interface_with_ip'] == state.current_attack_option), None)

print(interfaces)
print(brief_interfaces)

# get combobox state
def get_current_interface(event):
    state.current_interface_option = interfacesCombo.get()
    state.current_interface_object = next((item for item in interfaces if item['interface_with_ip'] == state.current_interface_option), None)

# initial to set default iface
get_current_interface(None)

interfacesCombo.bind("<<ComboboxSelected>>", get_current_interface)

# content frame grid layout
content_frame = ttk.Frame(root, padding=overall_padding)
content_frame.grid(row=2, column=0, columnspan=3, rowspan=3)

# panel cols
content_frame.columnconfigure(0, weight=1)
content_frame.columnconfigure(1, weight=1)
content_frame.columnconfigure(2, weight=1)

# panel rows
content_frame.rowconfigure(0, weight=1)
content_frame.rowconfigure(1, weight=1)
content_frame.rowconfigure(2, weight=1)

# panels config
panels.clear_frame(content_frame)

# add attack combobox listener
def get_current_attack(event):
    state.current_attack_option = attackCombo.get()
    change_panel(state.current_attack_option)

attackCombo.bind("<<ComboboxSelected>>", get_current_attack)

def change_panel(option):
    if option == "Network Scan":
        panels.network_scan(content_frame, ttk)
    elif option == "Port Scanner":
        panels.port_scan(content_frame, ttk)
    elif option == "ARP Spoofing":
        panels.arp_spoofing(content_frame, ttk)
    elif option == "ARP Spoofing (MITM)":
        panels.dns_poison(content_frame, ttk)
    else:
        panels.default(content_frame, ttk)

# display the default page initial
change_panel('default')

# last line
root.mainloop()
