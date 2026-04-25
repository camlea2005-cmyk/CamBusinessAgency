from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import customtkinter as ctk

from services.product_service import ProductService
from services.stock_service import StockService
from ui.dialogs.product_dialog import ProductDialog
from ui.pages.base_page import BasePage


class StockPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "Stock")
        self.search_var = ctk.StringVar()
        self._build_actions()
        self._build_table()
        self.refresh_table()

    def _build_actions(self) -> None:
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkButton(actions, text="Ajouter produit", command=self.add_product).pack(side="left", padx=4)
        ctk.CTkButton(actions, text="Modifier produit", command=self.edit_product).pack(side="left", padx=4)
        ctk.CTkButton(actions, text="Supprimer produit", fg_color="#d9534f", command=self.delete_product).pack(
            side="left", padx=4
        )
        ctk.CTkButton(actions, text="Entrée stock", command=lambda: self.adjust_stock("IN")).pack(side="left", padx=4)
        ctk.CTkButton(actions, text="Sortie stock", command=lambda: self.adjust_stock("OUT")).pack(side="left", padx=4)
        ctk.CTkButton(actions, text="Actualiser", command=self.refresh_table).pack(side="left", padx=4)

        search_box = ctk.CTkFrame(actions, fg_color="transparent")
        search_box.pack(side="right", padx=4)
        ctk.CTkEntry(search_box, width=220, textvariable=self.search_var, placeholder_text="Rechercher code/nom...").pack(
            side="left", padx=(0, 6)
        )
        ctk.CTkButton(search_box, text="Recherche", width=100, command=self.search_products).pack(side="left")

    def _build_table(self) -> None:
        table_container = ctk.CTkFrame(self)
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        columns = (
            "id",
            "code",
            "name",
            "category",
            "purchase_price",
            "sale_price",
            "quantity",
            "alert_threshold",
            "status",
        )

        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=18)
        headers = {
            "id": ("ID", 55),
            "code": ("Code", 95),
            "name": ("Nom", 190),
            "category": ("Catégorie", 130),
            "purchase_price": ("Prix Achat", 110),
            "sale_price": ("Prix Vente", 110),
            "quantity": ("Stock", 85),
            "alert_threshold": ("Seuil Alerte", 100),
            "status": ("État", 85),
        }
        for col in columns:
            label, width = headers[col]
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="center")

        self.tree.tag_configure("alert", background="#ffd6d6")
        self.tree.tag_configure("ok", background="#e9fce9")

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

    def search_products(self) -> None:
        self.refresh_table(self.search_var.get())

    def refresh_table(self, search: str | None = None) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in ProductService.list_products(search=search):
            is_alert = row["status"] == "ALERTE"
            self.tree.insert(
                "",
                tk.END,
                tags=("alert" if is_alert else "ok",),
                values=(
                    row["id"],
                    row["code"],
                    row["name"],
                    row["category"] or "-",
                    f"{row['purchase_price']:.2f}",
                    f"{row['sale_price']:.2f}",
                    row["quantity"],
                    row["alert_threshold"],
                    row["status"],
                ),
            )

    def _selected_product_id(self) -> int | None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Stock", "Sélectionnez un produit.")
            return None
        return int(self.tree.item(selected[0], "values")[0])

    def add_product(self) -> None:
        dialog = ProductDialog(self, title="Ajouter produit")
        self.wait_window(dialog)
        data = dialog.result
        if not data:
            return

        if not data["code"] or not data["name"]:
            messagebox.showerror("Validation", "Le code et le nom sont obligatoires.")
            return

        try:
            ProductService.create_product(**data)
            self.refresh_table(self.search_var.get())
        except Exception as exc:
            messagebox.showerror("Erreur", f"Impossible d'ajouter le produit : {exc}")

    def edit_product(self) -> None:
        product_id = self._selected_product_id()
        if not product_id:
            return

        product = ProductService.get_product(product_id)
        if not product:
            messagebox.showerror("Erreur", "Produit introuvable.")
            return

        dialog = ProductDialog(self, title="Modifier produit")
        dialog.preload(product)
        self.wait_window(dialog)
        data = dialog.result
        if not data:
            return

        try:
            ProductService.update_product(
                product_id=product_id,
                code=data["code"],
                name=data["name"],
                category=data["category"],
                purchase_price=data["purchase_price"],
                sale_price=data["sale_price"],
                alert_threshold=data["alert_threshold"],
            )
            self.refresh_table(self.search_var.get())
        except Exception as exc:
            messagebox.showerror("Erreur", f"Impossible de modifier le produit : {exc}")

    def delete_product(self) -> None:
        product_id = self._selected_product_id()
        if not product_id:
            return

        if not messagebox.askyesno("Confirmation", "Supprimer ce produit ?"):
            return

        try:
            ProductService.delete_product(product_id)
            self.refresh_table(self.search_var.get())
        except Exception as exc:
            messagebox.showerror("Erreur", f"Suppression impossible : {exc}")

    def adjust_stock(self, movement_type: str) -> None:
        product_id = self._selected_product_id()
        if not product_id:
            return

        qty = simpledialog.askinteger(
            "Mouvement de stock",
            "Quantité :",
            minvalue=1,
            parent=self,
        )
        if qty is None:
            return

        note = simpledialog.askstring("Note", "Note (optionnel) :", parent=self)
        delta = qty if movement_type == "IN" else -qty

        try:
            StockService.adjust_stock(product_id, delta, movement_type, note)
            self.refresh_table(self.search_var.get())
        except Exception as exc:
            messagebox.showerror("Erreur", str(exc))
