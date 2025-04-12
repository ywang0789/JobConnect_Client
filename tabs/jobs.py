import tkinter as tk


class JobsTab(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Job Placeholder", font=("Arial", 14)).pack(pady=20)
