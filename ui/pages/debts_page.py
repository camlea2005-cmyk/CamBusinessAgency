import customtkinter as ctk

from services.debt_service import DebtService
from ui.pages.base_page import BasePage


class DebtsPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "Dettes")
        debts = DebtService.list_debts()
        ctk.CTkLabel(self, text=f"Dettes enregistrées: {len(debts)}").pack(anchor="w", padx=20, pady=10)
