import customtkinter as ctk
import subprocess


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
        self.section_1_frame.grid(row=0, column=0, columnspan=1, rowspan=1, sticky="nw")

        self.btn_activate = ctk.CTkButton(
            master=self.section_1_frame, text="Activate"
        ).grid(row=0, column=0, columnspan=1, rowspan=1, padx=10, pady=10)
        self.btn_delete = ctk.CTkButton(
            master=self.section_1_frame, text="Delete"
        ).grid(row=0, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.btn_renew = ctk.CTkButton(
            master=self.section_1_frame, text="Renew IP(auto release)"
        ).grid(row=1, column=0, columnspan=1, rowspan=1, padx=10, pady=10)
        self.btn_flush = ctk.CTkButton(
            master=self.section_1_frame, text="Flush Dns"
        ).grid(row=1, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.auto_renew_checkbox = ctk.CTkCheckBox(
            master=self.section_1_frame, text="Auto Renew ip"
        ).grid(row=2, column=0, columnspan=1, rowspan=1, padx=10, pady=10)
        self.auto_flush_checkbox = ctk.CTkCheckBox(
            master=self.section_1_frame, text="Auto flush"
        ).grid(row=2, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.btn_dhcp_dns = ctk.CTkButton(
            master=self.section_1_frame, text="DHCP Dns"
        ).grid(row=3, column=0, columnspan=1, rowspan=1, padx=10, pady=10)
        self.btn_ping_dns = ctk.CTkButton(
            master=self.section_1_frame, text="Ping selected DNS"
        ).grid(row=3, column=1, columnspan=1, rowspan=1, padx=10, pady=10)
        self.s1_logs = ctk.CTkTextbox(
            master=self.section_1_frame, width=250, state=ctk.DISABLED
        ).grid(row=4, column=0, columnspan=2, rowspan=4, padx=10, pady=10)
        # ? section 2 which is a list of dns profiles which we can use, manipulate and add new ones at will
        self.section_2_frame = ctk.CTkFrame(master=self.root)
        self.section_2_frame.grid(row=0, column=1, columnspan=1, rowspan=1, sticky="ne")
        self.lb_s2_list_info = ctk.CTkLabel(
            master=self.section_2_frame, text="Name \t DNS1 \t DNS2"
        ).pack(padx=10, pady=10)
        self.ls_s2_dns_frame = ctk.CTkScrollableFrame(
            master=self.section_2_frame, height=327
        ).pack(padx=10, pady=10)
        # ? section 3  which is a for adding new dns profiles and editing existing ones
        self.section_3_frame = ctk.CTkFrame(master=self.root)
        self.section_3_frame.grid(row=1, column=0, columnspan=1, rowspan=1, sticky="sw")
        self.lb_s3_name = ctk.CTkLabel(master=self.section_3_frame, text="Name:").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.s3_name_entry = ctk.CTkEntry(
            master=self.section_3_frame, placeholder_text="name"
        ).grid(row=0, column=1, padx=10, pady=10)
        self.lb_s3_dns1 = ctk.CTkLabel(
            master=self.section_3_frame, text="Preferred DNS:"
        ).grid(row=1, column=0, padx=10, pady=10)
        self.s3_dns1_entry = ctk.CTkEntry(
            master=self.section_3_frame, placeholder_text="Valid DNS like 1.1.1.1"
        ).grid(row=1, column=1, padx=10, pady=10)
        self.lb_s3_dns2 = ctk.CTkLabel(
            master=self.section_3_frame, text="Alternative DNS:"
        ).grid(row=2, column=0, padx=10, pady=10)
        self.s3_dns2_entry = ctk.CTkEntry(
            master=self.section_3_frame, placeholder_text="Valid DNS like 1.0.0.1"
        ).grid(row=2, column=1, padx=10, pady=10)
        self.btn_add = ctk.CTkButton(master=self.section_3_frame, text="ADD").grid(
            row=3, column=0, padx=10, pady=10
        )
        self.btn_edit = ctk.CTkButton(master=self.section_3_frame, text="EDIT").grid(
            row=3, column=1, padx=10, pady=10
        )
        # ? section 4 which just shows current DNS config that is active by the host pc and
        # ? also the section where you can choose the Network adapter which by defualt is Wi-fi
        self.section_4_frame = ctk.CTkFrame(master=self.root)
        self.section_4_frame.grid(
            row=1, column=1, columnspan=1, rowspan=1, sticky="se", ipadx=30
        )

        self.adapter_selector = ctk.CTkOptionMenu(master=self.section_4_frame).pack(
            padx=10, pady=10
        )
        self.lb_s4_current_1st_dns = ctk.CTkLabel(
            master=self.section_4_frame, text="Current Preferred DNS: . . . ."
        ).pack(padx=10, pady=10)
        self.lb_s4_current_2st_dns = ctk.CTkLabel(
            master=self.section_4_frame, text="Current Alternative DNS: . . . ."
        ).pack(padx=10, pady=10)
        self.lb_s4_current_local_ip = ctk.CTkLabel(
            master=self.section_4_frame, text="Current Local ip: . . . ."
        ).pack(padx=10, pady=10)


if __name__ == "__main__":

    app = main_app()
    # ? main loop
    app.root.mainloop()
