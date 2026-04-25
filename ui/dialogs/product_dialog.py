from __future__ import annotations

import customtkinter as ctk


class ProductDialog(ctk.CTkToplevel):
    def __init__(self, master, title: str = "Produit"):
        super().__init__(master)
        self.title(title)
        self.geometry("460x420")
        self.resizable(False, False)
        self.grab_set()

        self.result = None

        self.code_var = ctk.StringVar()
        self.name_var = ctk.StringVar()
        self.category_var = ctk.StringVar()
        self.purchase_price_var = ctk.StringVar(value="0")
        self.sale_price_var = ctk.StringVar(value="0")
        self.quantity_var = ctk.StringVar(value="0")
        self.alert_threshold_var = ctk.StringVar(value="5")

        fields = [
            ("Code", self.code_var),
            ("Nom", self.name_var),
            ("Catégorie", self.category_var),
            ("Prix achat", self.purchase_price_var),
            ("Prix vente", self.sale_price_var),
            ("Quantité initiale", self.quantity_var),
            ("Seuil alerte", self.alert_threshold_var),
        ]

        for i, (label, var) in enumerate(fields):
            ctk.CTkLabel(self, text=label).grid(row=i, column=0, padx=12, pady=8, sticky="w")
            ctk.CTkEntry(self, textvariable=var, width=280).grid(row=i, column=1, padx=12, pady=8)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

        ctk.CTkButton(button_frame, text="Annuler", fg_color="gray", command=self.destroy).pack(side="left", padx=8)
        ctk.CTkButton(button_frame, text="Valider", command=self._submit).pack(side="left", padx=8)

    def preload(self, product_row):
        self.code_var.set(product_row["code"])
        self.name_var.set(product_row["name"])
        self.category_var.set(product_row["category"] or "")
        self.purchase_price_var.set(str(float(product_row["purchase_price"])))
        self.sale_price_var.set(str(float(product_row["sale_price"])))
        self.quantity_var.set(str(int(product_row["quantity"])))
        self.alert_threshold_var.set(str(int(product_row["alert_threshold"])))

    def _submit(self):
        self.result = {
            "code": self.code_var.get().strip(),
            "name": self.name_var.get().strip(),
            "category": self.category_var.get().strip() or None,
            "purchase_price": float(self.purchase_price_var.get() or 0),
            "sale_price": float(self.sale_price_var.get() or 0),
            "quantity": int(self.quantity_var.get() or 0),
            "alert_threshold": int(self.alert_threshold_var.get() or 5),
        }
        self.destroy()
