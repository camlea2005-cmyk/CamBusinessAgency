from datetime import datetime

import customtkinter as ctk

from services.report_service import ReportService
from ui.pages.base_page import BasePage
from utils.formatters import money


class ReportsPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "Rapports")
        now = datetime.now()
        summary = ReportService.get_monthly_summary(now.year, now.month)

        ctk.CTkLabel(self, text=f"Mois: {now:%m/%Y}").pack(anchor="w", padx=20, pady=(6, 2))
        ctk.CTkLabel(self, text=f"Ventes: {money(summary['sales'])}").pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(self, text=f"Dépenses: {money(summary['expenses'])}").pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(self, text=f"Résultat: {money(summary['profit'])}", font=ctk.CTkFont(weight="bold")).pack(
            anchor="w", padx=20, pady=(2, 10)
        )
