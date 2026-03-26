import core.utils.helpers as helpers
import core.utils.tools as tools
import core.utils.state as state
from core.utils.logger import log

import tkinter as tk
from tkinter import ttk, Scrollbar
from tkinter.scrolledtext import ScrolledText

import threading
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
    # initially clear the frame
    clear_frame(content_frame)

    # define layout
    content_frame.columnconfigure(2, weight=1)

    # variables
    isScanLoading = {"value": False}
    optionsBox = None
    scanned_hosts = state.scanned_targets or []
    targetComboHosts = []
    selected_target = state.selected_target or {}
    selected_target_index = state.selected_target_index or 0

    def get_current_target(event):
        global selected_target, scanned_hosts

        # get the value from scanned_host using selected index
        selected_target_index = targetBox.current()
        selected_target = scanned_hosts[selected_target_index]

        # set the value as a global variable
        state.selected_target_index = selected_target_index
        state.selected_target = selected_target

        log(message=f"State changed: selected_target_index is now {selected_target_index}", severity="INFO")
        log(message=f"State changed: selected_target is now {selected_target}", severity="INFO")

    targetBox = ttk.Combobox(
        content_frame, 
        values=tuple(targetComboHosts),
        state='readonly',
    )
    targetBox.bind("<<ComboboxSelected>>", get_current_target)

    optionsBox = ttk.Combobox(
        content_frame, 
        values=tuple(helpers.scan_types.keys()),
        state='readonly',
        width=int(helpers.APP_WIDTH/2) - helpers.overall_padding
    )
    optionsBox.current(0)

    scan_btn = ttk.Button(
        content_frame,
        text="Scan",
        command=lambda: threading.Thread(target=scan_handler).start(),
        width=int(helpers.APP_WIDTH/2) - helpers.overall_padding
    )
    
    loading_label = ttk.Label(content_frame, text="")

    # upate table with new rows
    def update_table(rows):
        log(message=f"Netowork scan table is being updated with {rows}", severity="INFO")

        tree.delete(*tree.get_children())
        for host_row in rows:
            tree.insert("", "end", values=host_row)

    def update_target_combo(rows):
        log(message=f"Netowork scan target dropdown is being updated with {rows}", severity="INFO")

        # clear the box
        targetComboHosts.clear()
        targetBox['values'] = ()
        targetBox.set("")

        # format display string for combo box
        for host in rows:
            ip = host[0] if host[0] is not None else ""
            mac = host[1] if host[1] is not None else ""
            os = host[2] if host[2] is not None else ""

            formatted_str = f"{ip} {mac}" if helpers.scan_types[optionsBox.get()] == 'quick_scan' else f"{ip} {mac} {os}"
            targetComboHosts.append(formatted_str)
        
        # add targets to the targets combo box
        targetBox['values'] = targetComboHosts
        # use the cached index or 0
        targetBox.current(state.selected_target_index)

    def scan_handler():
        global scanned_hosts

        try:
            content_frame.after(0, start_loading)

            rc, scanned_hosts = tools.network_scan(
                network_ip=state.current_interface_object['network_ip'],
                iface=state.current_interface_object['interface'],
                scan_type=helpers.scan_types[optionsBox.get()],
                table_shown=True
            )

        except Exception as e:
            # In case of error, we want to stop the loading state
            content_frame.after(0, lambda: log(message=f"Network scan failed ({helpers.scan_types[optionsBox.get()]}), iface: {state.current_interface_option}\nError: {e}", severity="ERROR"))
            content_frame.after(0, stop_loading)

            scan_btn.config(text="Error", state="enabled")
        
        # cache scanned hosts value
        state.scanned_targets = scanned_hosts

        # add values to combobox
        update_target_combo(scanned_hosts)

        # update the table
        content_frame.after(0, lambda: update_table(scanned_hosts))
        content_frame.after(0, stop_loading)

    def start_loading():
        isScanLoading["value"] = True
        scan_btn.config(text="Scanning...", state="disabled")

    def stop_loading():
        isScanLoading["value"] = False
        scan_btn.config(text="Scan", state="normal")

    # define table header
    columns = ('IPv4 Address', "MAC address", "Open ports", "OS")
    columns_widths = (110, 130, 170, 170)

    # dynamically add table content
    tree = ttk.Treeview(content_frame, columns=columns, show='headings')
    for idx in range(len(columns)):
        tree.heading(columns[idx], text=columns[idx])
        tree.column(columns[idx], width=columns_widths[idx], anchor='w')
    
    # grid layout
    scan_btn.grid(row=1, column=1, sticky="we", pady=helpers.overall_padding, padx=helpers.overall_padding / 2)
    targetBox.grid(row=2, column=0, columnspan=2, sticky='we', pady=helpers.overall_padding)
    tree.grid(row=4, column=0, columnspan=2, sticky='nswe')
    loading_label.grid(row=3, column=1, sticky='n')
    optionsBox.grid(row=1, column=0, sticky='we', pady=helpers.overall_padding, padx=helpers.overall_padding / 2)

    # if the values are cached, use them
    if state.scanned_targets:
        update_table(state.scanned_targets)
        log(message=f"Loaded from cache, scanned_targets: {state.scanned_targets}", severity="INFO")


    if state.selected_target:
        update_target_combo(state.scanned_targets)
        log(message=f"Loaded from cache, selected_target: {state.selected_target}", severity="INFO")


def port_scan(content_frame, ttk):
    clear_frame(content_frame)
    ttk.Label(content_frame, text="port_scan").grid(row=1, column=1, sticky='w')

def arp_spoofing(content_frame, ttk):
    clear_frame(content_frame)
    ttk.Label(content_frame, text="arp spoofing").grid(row=1, column=1, sticky='w')

def dns_poison(content_frame, ttk):
    clear_frame(content_frame)
    ttk.Label(content_frame, text="dns poison").grid(row=1, column=1, sticky='w')