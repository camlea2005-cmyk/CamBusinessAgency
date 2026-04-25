import customtkinter as ctk

from ui.pages.base_page import BasePage


class SalesPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "Ventes")
        ctk.CTkLabel(self, text="Module Ventes prêt pour la V2.").pack(anchor="w", padx=20, pady=10)
