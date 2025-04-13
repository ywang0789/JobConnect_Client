import tkinter as tk
from tkinter import messagebox

import requests

from config import BASE_API_URL


class CreateJobWindow(tk.Toplevel):
    def __init__(self, master, cookies, on_success):
        super().__init__(master)
        self.title("Create New Job")
        self.geometry("400x400")
        self.cookies = cookies
        self.on_success = on_success

        # Form
        tk.Label(self, text="Job Title").pack(pady=(10, 5))
        self.title_entry = tk.Entry(self, width=40)
        self.title_entry.pack()

        tk.Label(self, text="Location").pack(pady=(10, 5))
        self.location_entry = tk.Entry(self, width=40)
        self.location_entry.pack()

        tk.Label(self, text="Salary").pack(pady=(10, 5))
        self.salary_entry = tk.Entry(self, width=40)
        self.salary_entry.pack()

        tk.Label(self, text="Description").pack(pady=(10, 5))
        self.description_text = tk.Text(self, height=5, width=40)
        self.description_text.pack()

        tk.Button(self, text="Submit", command=self.submit_job).pack(pady=20)

    def submit_job(self):
        data = {
            "title": self.title_entry.get(),
            "location": self.location_entry.get(),
            "salary": float(self.salary_entry.get() or 0),
            "description": self.description_text.get("1.0", "end").strip(),
        }

        if not all(data.values()):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        try:
            res = requests.post(
                f"{BASE_API_URL}/job", json=data, cookies=self.cookies, verify=False
            )
            if res.status_code == 201:
                messagebox.showinfo("Success", "Job created successfully!")
                self.destroy()
                self.on_success()
            else:
                messagebox.showerror("Error", f"Failed to create job.\n{res.text}")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
