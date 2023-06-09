import customtkinter as ctk

from packages.gui.settings.tab_view import TabView
from setup import Setup

config = Setup


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Settings")
        self.resizable(False, False)
        self.iconbitmap(config.ICON)

        self.tab_view = TabView(self)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10)
