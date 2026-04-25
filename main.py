import customtkinter as ctk

from config import APP_NAME, COLOR_THEME, THEME_MODE
from database.db import db
from ui.pages.clients_page import ClientsPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.debts_page import DebtsPage
from ui.pages.expenses_page import ExpensesPage
from ui.pages.reports_page import ReportsPage
from ui.pages.sales_page import SalesPage
from ui.pages.stock_page import StockPage


class CaisseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1200x740")
        self.minsize(980, 620)

        db.initialize()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="Caisse Boutique CI",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(20, 30), padx=16)

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.pages: dict[str, ctk.CTkFrame] = {}

        self.page_classes = {
            "Dashboard": DashboardPage,
            "Stock": StockPage,
            "Ventes": SalesPage,
            "Clients": ClientsPage,
            "Dettes": DebtsPage,
            "Dépenses": ExpensesPage,
            "Rapports": ReportsPage,
        }

        for name in self.page_classes:
            ctk.CTkButton(
                self.sidebar,
                text=name,
                anchor="w",
                command=lambda n=name: self.show_page(n),
            ).pack(fill="x", padx=12, pady=5)

        self.show_page("Dashboard")

    def show_page(self, page_name: str):
        current = self.pages.get(page_name)
        if current is None:
            cls = self.page_classes[page_name]
            current = cls(self.content)
            self.pages[page_name] = current
            current.grid(row=0, column=0, sticky="nsew")

        for name, page in self.pages.items():
            if name == page_name:
                page.tkraise()


if __name__ == "__main__":
    ctk.set_appearance_mode(THEME_MODE)
    ctk.set_default_color_theme(COLOR_THEME)

    app = CaisseApp()
    app.mainloop()
