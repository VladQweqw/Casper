import tkinter as tk
from tkinter import ttk, Scrollbar

from tkinter.scrolledtext import ScrolledText

import core.utils.helpers as helpers


def clear_frame(content_frame):
    # destory every children
    for widget in content_frame.winfo_children():
        widget.destroy()

def default(content_frame, ttk):
    clear_frame(content_frame)
    
    textbox = ScrolledText(content_frame, wrap=tk.WORD)

    textbox.tag_config('h1', font=helpers.title_font, justify='center')
    textbox.tag_config('p', font=helpers.normal_font, justify='center')
    textbox.config(yscrollcommand=None)
    textbox.vbar.pack_forget()

    # layout
    textbox.insert("end", "Welcome to CASPER", "h1")
    textbox.grid(row=0, column=0, sticky='nsew')

    textbox.config(state='disabled')

def network_scan(content_frame, ttk):
    # res = tools.network_scan(network_ip=current_interface_object['network_ip'], iface=current_interface_object['windows_interface'], output=True, verbose=True)
    clear_frame(content_frame)

    ttk.Label(content_frame, text="network scan").grid(row=3, column=1, sticky='w')

def port_scan(content_frame, ttk):
    clear_frame(content_frame)
    ttk.Label(content_frame, text="port_scan").grid(row=1, column=1, sticky='w')

def arp_spoofing(content_frame, ttk):
    clear_frame(content_frame)
    ttk.Label(content_frame, text="arp spoofing").grid(row=1, column=1, sticky='w')

def dns_poison(content_frame, ttk):
    clear_frame(content_frame)
    ttk.Label(content_frame, text="dns poison").grid(row=1, column=1, sticky='w')