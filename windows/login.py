import tkinter as tk
from tkinter import messagebox

import requests

from config import BASE_API_URL
from objects import Account
from windows.dashboard import MainDashboardWindow
from windows.register import RegisterWindow


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JobConnect - Login")
        self.geometry("300x300")

        tk.Label(self, text="Email").pack(pady=(20, 5))
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.pack()

        tk.Label(self, text="Password").pack(pady=(20, 5))
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=20)
        tk.Button(self, text="Register", command=self.open_register_window).pack()

        # autofill for testing
        tk.Button(self, text="Fill Recruiter", command=self.fill_recruiter).pack(pady=5)
        tk.Button(self, text="Fill Applicant", command=self.fill_applicant).pack(pady=5)

    def login(self):
        """uses entry fields to login to the API"""

        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            res = requests.post(
                f"{BASE_API_URL}/account/login",
                json={"email": email, "password": password},
                verify=False,
            )
            if res.status_code == 200:
                # get accouint info
                me = requests.get(
                    f"{BASE_API_URL}/account/me", cookies=res.cookies, verify=False
                )
                if me.status_code == 200:
                    # print(me.json())
                    user_account = Account(
                        me.json()["id"],
                        me.json()["first_name"],
                        me.json()["last_name"],
                        me.json()["email"],
                        me.json()["role"],
                    )
                    self.destroy()
                    # open dashboard window
                    MainDashboardWindow(res.cookies, user_account).mainloop()
                else:
                    messagebox.showerror("Error", "Failed to fetch user data.")
            else:
                messagebox.showerror(
                    "Login Failed", res.json().get("message", "Invalid credentials")
                )
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def open_register_window(self):
        RegisterWindow(self)

    def fill_recruiter(self):
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "Recruiter123!")
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, "recruiter@test.com")

    def fill_applicant(self):
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "Applicant123!")
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, "Applicant@test.com")
