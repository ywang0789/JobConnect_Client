import tkinter as tk
from tkinter import messagebox

import requests

from config import BASE_API_URL
from objects import Account
from windows.dashboard import MainDashboardWindow
from windows.register import RegisterWindow


class LoginWindow(tk.Tk):
    """
    A window for users to log in to JobConnect
    """

    def __init__(self):
        """
        Initialize the LoginWindow with input fields and control buttons.
        """
        super().__init__()
        self.title("JobConnect - Login")
        self.geometry("360x500")
        self.configure(bg="#f9f9f9")

        tk.Label(
            self, text="Login to JobConnect", font=("Arial", 16, "bold"), bg="#f9f9f9"
        ).pack(pady=(30, 10))

        form_frame = tk.Frame(self, bg="#f9f9f9")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Email", anchor="w", bg="#f9f9f9").pack(
            fill="x", padx=20
        )
        self.email_entry = tk.Entry(form_frame, width=35)
        self.email_entry.pack(padx=20, pady=(0, 10))

        tk.Label(form_frame, text="Password", anchor="w", bg="#f9f9f9").pack(
            fill="x", padx=20
        )
        self.password_entry = tk.Entry(form_frame, show="*", width=35)
        self.password_entry.pack(padx=20, pady=(0, 20))

        action_frame = tk.Frame(self, bg="#f9f9f9")
        action_frame.pack(pady=5)

        tk.Button(
            action_frame,
            text="Login",
            command=self.login,
            width=15,
            bg="#007acc",
            fg="white",
        ).pack(pady=5)
        tk.Button(
            action_frame, text="Register", command=self.open_register_window, width=15
        ).pack(pady=5)

        autofill_frame = tk.LabelFrame(
            self, text="Testing Shortcuts", padx=10, pady=10, bg="#f9f9f9"
        )
        autofill_frame.pack(pady=20)

        tk.Button(
            autofill_frame, text="Fill Recruiter", command=self.fill_recruiter, width=20
        ).pack(pady=5)
        tk.Button(
            autofill_frame, text="Fill Applicant", command=self.fill_applicant, width=20
        ).pack()

    def login(self):
        """
        Attempt to log in the user using the API with provided email and password.
        On success, fetch user details and open the dashboard window.
        """
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            res = requests.post(
                f"{BASE_API_URL}/account/login",
                json={"email": email, "password": password},
                verify=False,
            )
            if res.status_code == 200:
                me = requests.get(
                    f"{BASE_API_URL}/account/me", cookies=res.cookies, verify=False
                )
                if me.status_code == 200:
                    user_account = Account(
                        me.json()["id"],
                        me.json()["first_name"],
                        me.json()["last_name"],
                        me.json()["email"],
                        me.json()["role"],
                    )
                    self.destroy()
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
        """
        Open a separate window for user registration.
        """
        RegisterWindow(self)

    def fill_recruiter(self):
        """
        Autofill recruiter credentials for testing purposes.
        """
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, "recruiter@test.com")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "Recruiter123!")

    def fill_applicant(self):
        """
        Autofill applicant credentials for testing purposes.
        """
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, "applicant@test.com")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "Applicant123!")
