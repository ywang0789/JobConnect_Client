import tkinter as tk
from tkinter import ttk

from objects import Account
from tabs.account import AccountTab
from tabs.applications import ApplicationsTab
from tabs.jobs import JobsTab


class MainDashboardWindow(tk.Tk):
    def __init__(self, cookies, user_account: Account):
        super().__init__()
        self.title("JobConnect - Dashboard")
        self.geometry("600x400")
        self.cookies = cookies
        self.user_account = user_account

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        notebook.add(AccountTab(notebook), text="Account")
        notebook.add(JobsTab(notebook), text="Jobs")
        notebook.add(ApplicationsTab(notebook), text="Applications")
