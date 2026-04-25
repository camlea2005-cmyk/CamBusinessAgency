import customtkinter as ctk


class BasePage(ctk.CTkFrame):
    def __init__(self, master, title: str):
        super().__init__(master)
        self.title_label = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(anchor="w", padx=20, pady=(20, 10))
