import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

from services.sales_service import SalesService
from ui.dialogs.sale_dialog import SaleDialog
from ui.pages.base_page import BasePage


class SalesPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "Ventes")
        self.search_var = ctk.StringVar()

        self._build_actions()
        self._build_table()
        self.refresh_table()

    def _build_actions(self):
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkButton(actions, text="Nouvelle vente", command=self.new_sale).pack(side="left", padx=4)
        ctk.CTkButton(actions, text="Supprimer vente", fg_color="#d9534f", command=self.delete_sale).pack(
            side="left", padx=4
        )
        ctk.CTkButton(actions, text="Actualiser", command=self.refresh_table).pack(side="left", padx=4)

        search_box = ctk.CTkFrame(actions, fg_color="transparent")
        search_box.pack(side="right")
        ctk.CTkEntry(search_box, textvariable=self.search_var, width=220, placeholder_text="Rechercher...").pack(
            side="left", padx=(0, 6)
        )
        ctk.CTkButton(search_box, text="Recherche", width=100, command=self.search_sales).pack(side="left")

    def _build_table(self):
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        columns = ("id", "date", "product", "quantity", "unit_price", "total", "client", "payment")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=18)

        headers = {
            "id": ("ID", 60),
            "date": ("Date", 150),
            "product": ("Produit", 180),
            "quantity": ("Quantité", 80),
            "unit_price": ("Prix Unitaire", 110),
            "total": ("Total", 100),
            "client": ("Client", 170),
            "payment": ("Paiement", 120),
        }

        for col in columns:
            label, width = headers[col]
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="center")

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def refresh_table(self, search: str | None = None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in SalesService.list_sales(search):
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row["id"],
                    row["created_at"],
                    row["product_name"],
                    row["quantity"],
                    f"{row['unit_price']:.2f}",
                    f"{row['line_total']:.2f}",
                    row["client_name"],
                    row["payment_mode"],
                ),
            )

    def search_sales(self):
        self.refresh_table(self.search_var.get())

    def new_sale(self):
        dialog = SaleDialog(self)
        self.wait_window(dialog)
        data = dialog.result
        if not data:
            return

        try:
            SalesService.create_sale(**data)
            self.refresh_table(self.search_var.get())
        except Exception as exc:
            messagebox.showerror("Ventes", str(exc))

    def delete_sale(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ventes", "Sélectionnez une vente.")
            return

        sale_id = int(self.tree.item(selected[0], "values")[0])
        if not messagebox.askyesno("Confirmation", "Supprimer cette vente ?"):
            return

        try:
            SalesService.delete_sale(sale_id)
            self.refresh_table(self.search_var.get())
        except Exception as exc:
            messagebox.showerror("Ventes", str(exc))
