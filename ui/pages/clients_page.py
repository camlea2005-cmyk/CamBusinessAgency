import customtkinter as ctk

from services.client_service import ClientService
from ui.pages.base_page import BasePage


class ClientsPage(BasePage):
    def __init__(self, master):
        super().__init__(master, "Clients")
        clients = ClientService.list_clients()
        ctk.CTkLabel(self, text=f"Nombre de clients: {len(clients)}").pack(anchor="w", padx=20, pady=10)
