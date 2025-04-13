import tkinter as tk
from tkinter import messagebox, ttk

import requests

from config import BASE_API_URL


class RegisterWindow(tk.Toplevel):
    """
    A popup window that allows users to register a new account.
    Includes input fields for name, email, password, and role selection.
    """

    def __init__(self, master):
        """
        registration form and attach to the given master window.
        """
        super().__init__(master)
        self.title("Register Account")
        self.geometry("360x500")
        self.configure(bg="#f9f9f9")

        tk.Label(
            self, text="Create a New Account", font=("Arial", 16, "bold"), bg="#f9f9f9"
        ).pack(pady=(30, 10))

        form_frame = tk.Frame(self, bg="#f9f9f9")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="First Name", anchor="w", bg="#f9f9f9").pack(
            fill="x", padx=20
        )
        self.first_name_entry = tk.Entry(form_frame, width=35)
        self.first_name_entry.pack(padx=20, pady=(0, 10))

        tk.Label(form_frame, text="Last Name", anchor="w", bg="#f9f9f9").pack(
            fill="x", padx=20
        )
        self.last_name_entry = tk.Entry(form_frame, width=35)
        self.last_name_entry.pack(padx=20, pady=(0, 10))

        tk.Label(form_frame, text="Email", anchor="w", bg="#f9f9f9").pack(
            fill="x", padx=20
        )
        self.email_entry = tk.Entry(form_frame, width=35)
        self.email_entry.pack(padx=20, pady=(0, 10))

        tk.Label(form_frame, text="Password", anchor="w", bg="#f9f9f9").pack(
            fill="x", padx=20
        )
        self.password_entry = tk.Entry(form_frame, show="*", width=35)
        self.password_entry.pack(padx=20, pady=(0, 10))

        tk.Label(form_frame, text="Role", anchor="w", bg="#f9f9f9").pack(
            fill="x", padx=20
        )
        self.role_combobox = ttk.Combobox(
            form_frame, values=["recruiter", "applicant"], width=32
        )
        self.role_combobox.set("applicant")
        self.role_combobox.pack(padx=20, pady=(0, 20))

        tk.Button(
            self,
            text="Register",
            command=self.register,
            width=20,
            bg="#007acc",
            fg="white",
        ).pack(pady=20)

    def register(self):
        """
        Collect form input and send a registration request to the API.
        """
        data = {
            "FirstName": self.first_name_entry.get(),
            "LastName": self.last_name_entry.get(),
            "Email": self.email_entry.get(),
            "Password": self.password_entry.get(),
            "Role": self.role_combobox.get(),
        }

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
