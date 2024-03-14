import customtkinter as ctk


if __name__ == "__main__":

    # ? Main window
    root = ctk.CTk()
    root.title("Neo DNS Changer With Python by Red Mage")
    # ? section 1 which is general buttons like activate or delete the selected dns or cmd commands
    section_1_frame = ctk.CTkFrame(master=root)
    section_1_frame.grid(row=0, column=0, columnspan=1, rowspan=4, padx=10, pady=10)
    btn_activate = ctk.CTkButton(master=section_1_frame, text="Activate").pack(
        padx=10, pady=10
    )
    btn_delete = ctk.CTkButton(master=section_1_frame, text="Delete").pack(
        padx=10, pady=10
    )
    # ? section 2 which is a list of dns profiles which we can use, manipulate and add new ones at will
    section_2_frame = ctk.CTkFrame(master=root)
    section_2_frame.grid(row=0, column=1, columnspan=4, rowspan=1, padx=10, pady=10)
    lb_list_info = ctk.CTkLabel(
        master=section_2_frame, text="Name \t DNS1 \t DNS2"
    ).pack(padx=10, pady=10)
    ls_dns_frame = ctk.CTkScrollableFrame(master=section_2_frame, height=300).pack(
        padx=10, pady=10
    )
    # ? main loop
    root.mainloop()
