import core.utils.attacks as attacks
import core.utils.tools as tools

from core.utils.helpers import menu_options
import core.utils.panels as panels

import psutil
import ipaddress
import ctypes

import tkinter as tk
from tkinter import ttk
from tkinter import font
import sv_ttk

# variables
current_attack_option = ''
current_interface_option = ''
current_interface_object = {}

root = tk.Tk()
sv_ttk.set_theme('dark')
root.geometry('600x700')
root.minsize(600, 700)
root.maxsize(600, 700)

# App title / icon
root.title("Casper - Peneration testing tool")
root.iconbitmap("public/images/logo.ico")

# font
default_font = font.nametofont("TkDefaultFont")
default_font.config(family='Segoe UI', size=12)

# grid layout
# 2 columns, 1fr 1fr
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# 3 rows
root.rowconfigure(0, weight=0, minsize=75)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

header_frame = ttk.Frame(root, padding=10)
attackComboFrame = ttk.Frame(root, padding=10)
interfaceComboFrame = ttk.Frame(root, padding=10)

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
attacksLabel.pack(side='top')

attacksText = tk.StringVar(value=menu_options[0])
attackCombo = ttk.Combobox(
    attackComboFrame, 
    textvariable=attacksText,
    values=menu_options,
    state='readonly',
    width=30
)
attackCombo.place(anchor='center', relx=0.5, rely=0.2)
current_attack_option = menu_options[0]

# Interface dropdown
interfacesLabel = tk.Label(
    interfaceComboFrame,
    text="Choose interface")
interfacesLabel.pack(side='top')

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
interfacesCombo.place(anchor='center', relx=0.5, rely=0.2)
current_interface_option = brief_interfaces[0]
current_interface_object = next((item for item in interfaces if item['interface'] == current_interface_option), None)

# get combobox state
def get_current_interface(event):
    global current_attack_option, current_interface_object
    current_interface_option = interfacesCombo.get()
    current_interface_object = next((item for item in interfaces if item['interface'] == current_interface_option), None)

interfacesCombo.bind("<<ComboboxSelected>>", get_current_interface)

# main panel
content_frame = ttk.Frame(root, padding=10)
content_frame.grid(row=2, column=0, columnspan=3)

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
    current_attack_option = attackCombo.get()
    menu_options(current_attack_option)

attackCombo.bind("<<ComboboxSelected>>", get_current_attack)

def menu_options(option):
    if option == "Network Scan":  
        res = tools.network_scan(network_ip=current_interface_object['network_ip'], iface=current_interface_object['windows_interface'], output=True, verbose=True)

        for send, received in res:
            print(send, received)

        panels.network_scan(content_frame, ttk)
    elif option == "Port Scanner": 
        panels.port_scan(content_frame, ttk)
    elif option == "ARP Spoofing":
        panels.arp_spoofing(content_frame, ttk)
    elif option == "ARP Spoofing (MITM)":
        panels.dns_poison(content_frame, ttk)

# last line
root.mainloop()
