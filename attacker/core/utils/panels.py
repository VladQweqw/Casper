import core.utils.helpers as helpers

import tkinter as tk
from tkinter import ttk, Scrollbar
from tkinter.scrolledtext import ScrolledText

import webbrowser

def clear_frame(content_frame):
    # destory every children
    for widget in content_frame.winfo_children():
        widget.destroy()

def default(content_frame, ttk):
    clear_frame(content_frame)
    
    # bd=0, removes border
    textbox = ScrolledText(content_frame, wrap=tk.WORD, bd=0)

    textbox.tag_config('h1', font=helpers.title_font, justify='center')
    textbox.tag_config('p', font=helpers.normal_font, foreground='#DADADA', justify='center')
    
    # Remove the scrollbar, basically remove it by None and then forget to render it ig
    textbox.config(yscrollcommand=None)
    textbox.vbar.pack_forget()

    # layout, add the tag at the end (h1 for header, p for paragrahp)
    textbox.insert("end", "Welcome to CASPER\n", "h1")
    textbox.insert("end", "This is a penetration testing tool for networks, use at your own risk.\n", "p")

    textbox.insert("end", "\nFirst steps\n", "h1")
    textbox.insert("end", "To begin, choose an attack choice, for example go for Network scan, then select the interface you want to send packets to.\n", "p")
    textbox.insert("end", "Then follow the instructions on the page and choose the target device or choose from a set of options\n", "p")

    textbox.insert("end", "\nSupport the app\n", "h1")
    textbox.insert("end", "If you want to support the ", "p")

    textbox.tag_config('link', font=helpers.link_font, underline=1)
    textbox.tag_bind('link', "<Button-1>", lambda x:webbrowser.open('https://vladpoienariu.com/'))
    textbox.insert("end", "creator", "link")
    textbox.insert("end", "\nNow you should be good, happy testing!", "p")

    # center it using nsew
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