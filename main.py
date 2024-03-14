import customtkinter as ctk


class main_app:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.root.title("Neo DNS Changer With Python by Red Mage")
        # ? section 1 which is general buttons like activate or delete the selected dns or cmd commands
        self.section_1_frame = ctk.CTkFrame(master=self.root)
        self.section_1_frame.grid(
            row=0, column=0, columnspan=1, rowspan=4, padx=10, pady=10
        )
        self.btn_activate = ctk.CTkButton(
            master=self.section_1_frame, text="Activate"
        ).pack(padx=10, pady=10)
        self.btn_delete = ctk.CTkButton(
            master=self.section_1_frame, text="Delete"
        ).pack(padx=10, pady=10)
        # ? section 2 which is a list of dns profiles which we can use, manipulate and add new ones at will
        self.section_2_frame = ctk.CTkFrame(master=self.root)
        self.section_2_frame.grid(
            row=0, column=1, columnspan=4, rowspan=1, padx=10, pady=10
        )
        self.lb_list_info = ctk.CTkLabel(
            master=self.section_2_frame, text="Name \t DNS1 \t DNS2"
        ).pack(padx=10, pady=10)
        self.ls_dns_frame = ctk.CTkScrollableFrame(
            master=self.section_2_frame, height=300
        ).pack(padx=10, pady=10)


if __name__ == "__main__":

    app = main_app()
    # ? main loop
    app.root.mainloop()
