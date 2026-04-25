import customtkinter as ctk


def section_title(parent: ctk.CTkFrame, text: str) -> ctk.CTkLabel:
    label = ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=20, weight="bold"))
    label.pack(anchor="w", padx=20, pady=(15, 8))
    return label
