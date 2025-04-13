import tkinter as tk
from tkinter import ttk

from objects import Account
from tabs.account import AccountTab
from tabs.jobs import JobsTab


class MainDashboardWindow(tk.Tk):
    """
    Main dashboard window for JobConnect after successful login - has tabs to things
    """

    def __init__(self, cookies, user_account: Account):
        """
        :param cookies: Session cookies for API requests fro auth
        :param user_account: Logged-in user's account info
        """
        super().__init__()
        self.title("JobConnect - Dashboard")
        self.geometry("700x600")
        self.configure(bg="#f0f0f0")
        self.cookies = cookies
        self.user_account = user_account

        # Header
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill="x", pady=(15, 5))

        tk.Label(
            header_frame,
            text=f"Welcome, {self.user_account.first_name}!",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
        ).pack()

        # Notebook tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabs
        notebook.add(
            AccountTab(notebook, self.cookies, self.user_account), text="Account"
        )
        notebook.add(JobsTab(notebook, self.cookies, self.user_account), text="Jobs")
