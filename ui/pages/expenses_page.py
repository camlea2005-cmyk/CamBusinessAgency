import customtkinter as ctk

from ui.pages.base_page import BasePage


class ExpensesPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "Dépenses")
        ctk.CTkLabel(self, text="Module Dépenses prêt pour saisie V2.").pack(anchor="w", padx=20, pady=10)
