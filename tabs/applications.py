import tkinter as tk


class ApplicationsTab(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Applications Placeholder", font=("Arial", 14)).pack(
            pady=20
        )
