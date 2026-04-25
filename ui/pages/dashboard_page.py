import customtkinter as ctk

from services.dashboard_service import DashboardService
from ui.pages.base_page import BasePage
from utils.formatters import money


class DashboardPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "Tableau de bord")

        self.cards_frame = ctk.CTkFrame(self)
        self.cards_frame.pack(fill="x", padx=20, pady=10)

        self.labels = {}
        for idx, (key, title) in enumerate(
            [
                ("products", "Produits"),
                ("stock_value", "Valeur stock"),
                ("sales_today", "Ventes du jour"),
                ("expenses_today", "Dépenses du jour"),
            ]
        ):
            card = ctk.CTkFrame(self.cards_frame)
            card.grid(row=0, column=idx, padx=8, pady=8, sticky="nsew")
            self.cards_frame.grid_columnconfigure(idx, weight=1)
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(weight="bold")).pack(padx=20, pady=(14, 4))
            label = ctk.CTkLabel(card, text="-", font=ctk.CTkFont(size=18))
            label.pack(padx=20, pady=(0, 14))
            self.labels[key] = label

        refresh_btn = ctk.CTkButton(self, text="Rafraîchir", command=self.refresh)
        refresh_btn.pack(anchor="e", padx=20, pady=8)

        self.refresh()

    def refresh(self):
        kpis = DashboardService.get_kpis()
        self.labels["products"].configure(text=str(kpis["products"]))
        self.labels["stock_value"].configure(text=money(kpis["stock_value"]))
        self.labels["sales_today"].configure(text=money(kpis["sales_today"]))
        self.labels["expenses_today"].configure(text=money(kpis["expenses_today"]))
