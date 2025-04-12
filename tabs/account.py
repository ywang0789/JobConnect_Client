import tkinter as tk


class AccountTab(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Account Placeholder", font=("Arial", 14)).pack(pady=20)
