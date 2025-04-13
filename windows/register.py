import tkinter as tk
from tkinter import messagebox, ttk  # Added ttk for Combobox

import requests

from config import BASE_API_URL


class RegisterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Register Account")
        self.geometry("300x500")

        # Form fields
        tk.Label(self, text="First Name").pack(pady=(20, 5))
        self.first_name_entry = tk.Entry(self, width=30)
        self.first_name_entry.pack()

        tk.Label(self, text="Last Name").pack(pady=(20, 5))
        self.last_name_entry = tk.Entry(self, width=30)
        self.last_name_entry.pack()

        tk.Label(self, text="Email").pack(pady=(20, 5))
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.pack()

        tk.Label(self, text="Password").pack(pady=(20, 5))
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack()

        tk.Label(self, text="Role").pack(pady=(20, 5))
        self.role_combobox = ttk.Combobox(self, values=["recruiter", "applicant"])
        self.role_combobox.set("applicant")
        self.role_combobox.pack()

        tk.Button(self, text="Register", command=self.register).pack(pady=20)

    def register(self):
        data = {
            "FirstName": self.first_name_entry.get(),
            "LastName": self.last_name_entry.get(),
            "Email": self.email_entry.get(),
            "Password": self.password_entry.get(),
            "Role": self.role_combobox.get(),
        }

        # print(data)

        if not all(data.values()):
            messagebox.showerror("Missing Info", "Please fill in all fields.")
            return

        try:
            res = requests.post(
                f"{BASE_API_URL}/account/register", json=data, verify=False
            )

            if res.status_code == 200:
                messagebox.showinfo("Success", "Account registered successfully!")
                self.destroy()
            else:
                try:
                    error_response = res.json()
                    if isinstance(error_response, dict):
                        message = error_response.get("message", str(error_response))
                    elif isinstance(error_response, list):
                        message = "\n".join(str(item) for item in error_response)
                    else:
                        message = str(error_response)
                except Exception as parse_err:
                    message = res.text or str(parse_err)

                messagebox.showerror("Register Failed", message)

        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
