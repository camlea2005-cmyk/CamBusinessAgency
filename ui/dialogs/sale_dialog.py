from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox

from services.product_service import ProductService


class SaleDialog(ctk.CTkToplevel):
    PAYMENT_OPTIONS = ["comptant", "mobile money", "dette"]

    def __init__(self, master):
        super().__init__(master)
        self.title("Nouvelle vente")
        self.geometry("520x420")
        self.resizable(False, False)
        self.grab_set()

        self.result = None
        self.products = list(ProductService.list_products())
        if not self.products:
            ctk.CTkLabel(self, text="Aucun produit en stock disponible.", font=ctk.CTkFont(weight="bold")).pack(
                pady=40
            )
            ctk.CTkButton(self, text="Fermer", command=self.destroy).pack(pady=10)
            return

        self.product_label_to_id = {f"{p['code']} - {p['name']}": int(p["id"]) for p in self.products}

        self.product_var = ctk.StringVar(value=list(self.product_label_to_id.keys())[0])
        self.qty_var = ctk.StringVar(value="1")
        self.price_var = ctk.StringVar(value="0")
        self.total_var = ctk.StringVar(value="0")
        self.client_var = ctk.StringVar()
        self.payment_var = ctk.StringVar(value=self.PAYMENT_OPTIONS[0])
        self.note_var = ctk.StringVar()

        self._build_form()
        self._bind_events()
        self._update_price_and_total()

    def _build_form(self):
        form = ctk.CTkFrame(self)
        form.pack(fill="both", expand=True, padx=16, pady=16)

        self._add_row(form, 0, "Produit", ctk.CTkOptionMenu(form, values=list(self.product_label_to_id.keys()), variable=self.product_var))
        self._add_row(form, 1, "Quantité", ctk.CTkEntry(form, textvariable=self.qty_var))
        self._add_row(form, 2, "Prix unitaire", ctk.CTkEntry(form, textvariable=self.price_var, state="readonly"))
        self._add_row(form, 3, "Total", ctk.CTkEntry(form, textvariable=self.total_var, state="readonly"))
        self._add_row(form, 4, "Client (optionnel)", ctk.CTkEntry(form, textvariable=self.client_var))
        self._add_row(
            form,
            5,
            "Paiement",
            ctk.CTkOptionMenu(form, values=self.PAYMENT_OPTIONS, variable=self.payment_var),
        )
        self._add_row(form, 6, "Note", ctk.CTkEntry(form, textvariable=self.note_var))

        button_frame = ctk.CTkFrame(form, fg_color="transparent")
        button_frame.grid(row=7, column=0, columnspan=2, pady=(18, 4))
        ctk.CTkButton(button_frame, text="Annuler", fg_color="gray", command=self.destroy).pack(side="left", padx=8)
        ctk.CTkButton(button_frame, text="Valider", command=self._submit).pack(side="left", padx=8)

    @staticmethod
    def _add_row(frame, row, label, widget):
        ctk.CTkLabel(frame, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=8)
        widget.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
        frame.grid_columnconfigure(1, weight=1)

    def _bind_events(self):
        self.qty_var.trace_add("write", lambda *_: self._update_price_and_total())
        self.product_var.trace_add("write", lambda *_: self._update_price_and_total())

    def _update_price_and_total(self):
        product = self._selected_product()
        if not product:
            self.price_var.set("0")
            self.total_var.set("0")
            return

        price = float(product["sale_price"])
        try:
            qty = max(1, int(self.qty_var.get() or "1"))
        except ValueError:
            qty = 1

        self.price_var.set(f"{price:.2f}")
        self.total_var.set(f"{(price * qty):.2f}")

    def _selected_product(self):
        selected = self.product_var.get()
        product_id = self.product_label_to_id.get(selected)
        for p in self.products:
            if int(p["id"]) == product_id:
                return p
        return None

    def _submit(self):
        product = self._selected_product()
        if not product:
            self.destroy()
            return

        try:
            qty = int(self.qty_var.get() or "0")
        except ValueError:
            messagebox.showerror("Validation", "Quantité invalide")
            return

        if qty <= 0:
            messagebox.showerror("Validation", "Quantité invalide")
            return

        self.result = {
            "product_id": int(product["id"]),
            "quantity": qty,
            "unit_price": float(product["sale_price"]),
            "client_name": self.client_var.get().strip() or None,
            "payment_mode": self.payment_var.get(),
            "note": self.note_var.get().strip() or None,
        }
        self.destroy()
