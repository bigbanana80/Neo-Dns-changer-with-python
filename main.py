# information
""" my info !
__author__ = "Sepehr Aghajani"
__copyright__ = "Copyright 2023, Neo DNS changer with python Project"
__credits__ = ["Sepehr Aghajani"]
__license__ = "GPL"
__version__ = "1.232"
__maintainer__ = "Sepehr Aghajani"
__email__ = "sepehra90@gmail.com"
__status__ = "Finished"
"""
import customtkinter as ctk
from dataclasses import dataclass
import subprocess
import psutil
import json
import os
import sys

# ? this block of code checks if config.json and profiles dir exists, if not makes them
CONFIG = "config.json"  # ^ instead of this we use settings var to actually use the content of config.json
default_config = {"autoFlush": "True", "autoRenew": "False"}
dirname = os.path.dirname(sys.argv[0])
filename = os.path.join(dirname, "profiles\\")
if not os.path.exists(filename):
    os.mkdir(filename)
if not os.path.exists(CONFIG):
    with open(CONFIG, "w") as file:
        json.dump(default_config, file, indent=6)


# ? some startup vars including network adapter names, existing profiles in profiles dir and config.json content
addrs = [nic for nic in psutil.net_if_addrs()]  # ^ all NICs in the current pc
profiles = [
    f for f in os.listdir("profiles") if os.path.isfile(os.path.join("profiles", f))
]  # ^ all dns profiles in the profiles dir
with open(CONFIG, "r") as file:
    settings = json.loads(file.read())  # ^ loading settings in the config.json


@dataclass
class dns:
    name: str
    dns1: str = "0.0.0.0"
    dns2: str = "0.0.0.0"

    def save_json(self):
        values = {"name": self.name, "dns1": self.dns1, "dns2": self.dns2}
        with open(f"profiles/{self.name}.json", "w") as file:
            json.dump(values, file, indent=6)


class main_app:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.title("Neo DNS Changer With Python by Red Mage")
        self.root.grid_rowconfigure(0, weight=1, pad=10)
        self.root.grid_columnconfigure(0, weight=1, pad=10)
        self.root.grid_rowconfigure(1, weight=1, pad=10)
        self.root.grid_columnconfigure(1, weight=1, pad=10)
        # ? section 1 which is general buttons like activate or delete the selected dns or cmd commands
        self.section_1_frame = ctk.CTkFrame(master=self.root)
        self.section_1_frame.grid(
            row=0, column=0, columnspan=1, rowspan=1, sticky="NSEW"
        )
        self.section_1_frame.grid_rowconfigure(0, weight=1)
        self.section_1_frame.grid_columnconfigure(0, weight=1)
        self.section_1_frame.grid_rowconfigure(1, weight=1)
        self.section_1_frame.grid_columnconfigure(1, weight=1)
        self.section_1_frame.grid_rowconfigure(2, weight=1)
        self.section_1_frame.grid_columnconfigure(2, weight=1)
        self.section_1_frame.grid_rowconfigure(3, weight=1)
        self.section_1_frame.grid_columnconfigure(3, weight=1)
        self.section_1_frame.grid_rowconfigure(4, weight=1)
        self.section_1_frame.grid_columnconfigure(4, weight=1)

        self.btn_activate = ctk.CTkButton(master=self.section_1_frame, text="Activate")
        self.btn_activate.grid(
            row=0, column=0, columnspan=1, rowspan=1, padx=10, pady=10
        )
        self.btn_delete = ctk.CTkButton(master=self.section_1_frame, text="Delete")
        self.btn_delete.grid(row=0, column=1, columnspan=1, rowspan=1, padx=10, pady=10)

        self.btn_renew = ctk.CTkButton(
            master=self.section_1_frame,
            text="Renew IP(auto release)",
            command=self.renew_command,
        )
        self.btn_renew.grid(row=1, column=0, columnspan=1, rowspan=1, padx=10, pady=10)
        self.btn_flush = ctk.CTkButton(
            master=self.section_1_frame, text="Flush Dns", command=self.flush_command
        )
        self.btn_flush.grid(row=1, column=1, columnspan=1, rowspan=1, padx=10, pady=10)

        self.auto_renew_checkbox_var = ctk.StringVar(master=self.section_1_frame)
        self.auto_renew_checkbox_var.set("off")
        self.auto_flush_checkbox_var = ctk.StringVar(master=self.section_1_frame)
        self.auto_flush_checkbox_var.set("off")
        self.auto_renew_checkbox = ctk.CTkCheckBox(
            master=self.section_1_frame,
            text="Auto Renew ip",
            variable=self.auto_renew_checkbox_var,
            onvalue="on",
            offvalue="off",
            command=self.auto_renew_checkbox_event,
        ).grid(row=2, column=0, columnspan=1, rowspan=1, padx=10, pady=10)
        self.auto_flush_checkbox = ctk.CTkCheckBox(
            master=self.section_1_frame,
            text="Auto flush",
            variable=self.auto_flush_checkbox_var,
            onvalue="on",
            offvalue="off",
            command=self.auto_flush_checkbox_event,
        ).grid(row=2, column=1, columnspan=1, rowspan=1, padx=10, pady=10)

        self.btn_dhcp_dns = ctk.CTkButton(master=self.section_1_frame, text="DHCP Dns")
        self.btn_dhcp_dns.grid(
            row=3, column=0, columnspan=1, rowspan=1, padx=10, pady=10
        )

        self.btn_ping_dns = ctk.CTkButton(
            master=self.section_1_frame, text="Ping selected DNS"
        )
        self.btn_ping_dns.grid(
            row=3, column=1, columnspan=1, rowspan=1, padx=10, pady=10
        )

        self.s1_logs = ctk.CTkTextbox(
            master=self.section_1_frame, width=250, wrap="word"
        )
        self.s1_logs.insert(
            "0.0",
            "The log of the last action you take appear here including the errors with solutions.",
        )
        self.s1_logs.configure(state=ctk.DISABLED)
        self.s1_logs.grid(row=4, column=0, columnspan=2, rowspan=4, padx=10, pady=10)

        # ? section 2 which is a list of dns profiles which we can use, manipulate and add new ones at will
        self.section_2_frame = ctk.CTkFrame(master=self.root)
        self.section_2_frame.grid(
            row=0, column=1, columnspan=1, rowspan=1, sticky="NSEW"
        )
        self.section_2_frame.grid_rowconfigure(0, weight=1)
        self.section_2_frame.grid_columnconfigure(0, weight=1)
        self.lb_s2_list_info = ctk.CTkLabel(
            master=self.section_2_frame, text="Name \t DNS1 \t DNS2"
        ).grid(row=0, column=0, padx=10, pady=10)
        self.ls_s2_dns_frame = ctk.CTkScrollableFrame(
            master=self.section_2_frame, height=327
        ).grid(row=1, column=0, padx=10, pady=10)

        # ? section 3  which is a for adding new dns profiles and editing existing ones
        self.section_3_frame = ctk.CTkFrame(master=self.root)
        self.section_3_frame.grid(
            row=1, column=0, columnspan=1, rowspan=1, sticky="NSEW"
        )
        self.section_3_frame.grid_rowconfigure(0, weight=1)
        self.section_3_frame.grid_columnconfigure(0, weight=1)
        self.section_3_frame.grid_rowconfigure(1, weight=1)
        self.section_3_frame.grid_columnconfigure(1, weight=1)
        self.section_3_frame.grid_rowconfigure(2, weight=1)
        self.section_3_frame.grid_columnconfigure(2, weight=1)
        self.section_3_frame.grid_rowconfigure(3, weight=1)
        self.section_3_frame.grid_columnconfigure(3, weight=1)

        self.lb_s3_name = ctk.CTkLabel(master=self.section_3_frame, text="Name:").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.s3_name_entry = ctk.CTkEntry(
            master=self.section_3_frame, placeholder_text="name"
        )
        self.s3_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.lb_s3_dns1 = ctk.CTkLabel(
            master=self.section_3_frame, text="Preferred DNS:"
        ).grid(row=1, column=0, padx=10, pady=10)
        self.s3_dns1_entry = ctk.CTkEntry(
            master=self.section_3_frame, placeholder_text="Valid DNS like 1.1.1.1"
        )
        self.s3_dns1_entry.grid(row=1, column=1, padx=10, pady=10)

        self.lb_s3_dns2 = ctk.CTkLabel(
            master=self.section_3_frame, text="Alternative DNS:"
        ).grid(row=2, column=0, padx=10, pady=10)
        self.s3_dns2_entry = ctk.CTkEntry(
            master=self.section_3_frame, placeholder_text="Valid DNS like 1.0.0.1"
        )
        self.s3_dns2_entry.grid(row=2, column=1, padx=10, pady=10)

        self.btn_add = ctk.CTkButton(
            master=self.section_3_frame, text="ADD", command=self.add_dns
        ).grid(row=3, column=0, padx=10, pady=10)
        self.btn_edit = ctk.CTkButton(
            master=self.section_3_frame, text="EDIT", command=self.edit_dns
        ).grid(row=3, column=1, padx=10, pady=10)
        # ? section 4 which just shows current DNS config that is active by the host pc and
        # ? also the section where you can choose the Network adapter which by defualt is Wi-fi
        self.section_4_frame = ctk.CTkFrame(master=self.root)
        self.section_4_frame.grid(
            row=1, column=1, columnspan=1, rowspan=1, sticky="NSEW", ipadx=30
        )
        self.section_4_frame.grid_rowconfigure(0, weight=1)
        self.section_4_frame.grid_columnconfigure(0, weight=1)
        self.section_4_frame.grid_rowconfigure(1, weight=1)
        self.section_4_frame.grid_columnconfigure(1, weight=1)
        self.section_4_frame.grid_rowconfigure(2, weight=1)
        self.section_4_frame.grid_columnconfigure(2, weight=1)
        self.section_4_frame.grid_rowconfigure(3, weight=1)
        self.section_4_frame.grid_columnconfigure(3, weight=1)

        self.adapter_selector = ctk.CTkOptionMenu(
            master=self.section_4_frame, values=addrs
        )
        self.adapter_selector.set("Wi-Fi")
        self.adapter_selector.grid(row=0, column=0, padx=10, pady=10)
        self.lb_s4_current_1st_dns = ctk.CTkLabel(
            master=self.section_4_frame, text="Current Preferred DNS: . . . ."
        )
        self.lb_s4_current_1st_dns.grid(row=1, column=0, padx=10, pady=10)
        self.lb_s4_current_2st_dns = ctk.CTkLabel(
            master=self.section_4_frame, text="Current Alternative DNS: . . . ."
        )
        self.lb_s4_current_2st_dns.grid(row=2, column=0, padx=10, pady=10)
        self.lb_s4_current_local_ip = ctk.CTkLabel(
            master=self.section_4_frame, text="Current Local ip: . . . ."
        )
        self.lb_s4_current_local_ip.grid(row=3, column=0, padx=10, pady=10)

    def auto_renew_checkbox_event(self):
        print(self.auto_renew_checkbox_var.get())

    def auto_flush_checkbox_event(self):
        print(self.auto_flush_checkbox_var.get())

    def add_dns(self):
        name = self.s3_name_entry.get()
        dns1 = self.s3_dns1_entry.get()
        dns2 = self.s3_dns2_entry.get()
        if name + ".json" in profiles:
            self.update_app_log(
                "Warning :\nFile already exist, use edit instead of Add"
            )
            return
        if name == "" or dns1 == "" or dns2 == "":
            self.update_app_log(
                "Empty entry error:\n\nAdd or edit buttons are clicked when one of the entries is empty."
                + "Please complete the entries with valid values. good example :\n\nGoogle\n8.8.8.8\n8.8.4.4",
            )
            return
        values = dns(name, dns1, dns2)
        values.save_json()
        self.clear_entries()

    def edit_dns(self):
        name = self.s3_name_entry.get()
        dns1 = self.s3_dns1_entry.get()
        dns2 = self.s3_dns2_entry.get()
        if name + ".json" not in profiles:
            self.update_app_log(
                "Warning:\nFile does not exist, use Add to make a new profile with the chosen name."
            )
            return
        if name == "" or dns1 == "" or dns2 == "":
            self.update_app_log(
                "Empty entry error:\n\nAdd or edit buttons are clicked when one of the entries is empty."
                + "Please complete the entries with valid values. good example :\n\nGoogle\n8.8.8.8\n8.8.4.4",
            )
            return
        values = dns(name, dns1, dns2)
        values.save_json()
        self.clear_entries()

    def clear_entries(self):
        self.s3_name_entry.delete(0, ctk.END)
        self.s3_dns1_entry.delete(0, ctk.END)
        self.s3_dns2_entry.delete(0, ctk.END)

    def update_app_log(self, value: str):
        self.s1_logs.configure(state="normal")
        self.s1_logs.delete("0.0", "end")
        self.s1_logs.insert("0.0", value)
        self.s1_logs.configure(state="disabled")

    def flush_command(self):
        try:
            subprocess.call("ipconfig /flushdns")
            self.update_app_log("Successfully flushed the DNS Resolver Cache.")
        except:
            self.update_app_log(
                "Unknown Error :\npossible fix is running the app as admin however report the"
                + "error to developer at Github."
            )

    def renew_command(self):
        try:
            subprocess.call("ipconfig /release")
            subprocess.call("ipconfig /renew")
            self.update_app_log("Successfully flushed the DNS Resolver Cache.")
        except:
            self.update_app_log(
                "Unknown Error :\npossible fix is running the app as admin however report the"
                + "error to developer at Github."
            )


if __name__ == "__main__":

    app = main_app()
    # ? main loop
    app.root.mainloop()
