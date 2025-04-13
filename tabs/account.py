import tkinter as tk
from tkinter import messagebox

import requests

from config import BASE_API_URL
from objects import Account


class AccountTab(tk.Frame):
    def __init__(self, master, cookies, user_account: Account):
        super().__init__(master)
        self.cookies = cookies
        self.user_account = user_account

        tk.Label(self, text="Account Info", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(
            self, text=f"Name: {user_account.first_name} {user_account.last_name}"
        ).pack(pady=2)
        tk.Label(self, text=f"Email: {user_account.email}").pack(pady=2)
        tk.Label(self, text=f"Role: {user_account.role}").pack(pady=2)

        # Buttons
        tk.Button(self, text="Logout", command=self.logout, bg="lightblue").pack(
            pady=10
        )
        tk.Button(
            self,
            text="Delete Account",
            command=self.delete_account,
            bg="red",
            fg="white",
        ).pack(pady=5)

    def logout(self):
        try:
            res = requests.post(
                f"{BASE_API_URL}/account/logout", cookies=self.cookies, verify=False
            )
            if res.status_code == 200:
                messagebox.showinfo("Logged Out", "You have been logged out.")
                self.master.master.destroy()
            else:
                messagebox.showerror("Error", "Logout failed.")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def delete_account(self):
        confirm = messagebox.askyesno(
            "Delete Account", "Are you sure you want to delete your account?"
        )
        if not confirm:
            return

        try:
            res = requests.delete(
                f"{BASE_API_URL}/account/delete", cookies=self.cookies, verify=False
            )
            if res.status_code == 200:
                messagebox.showinfo("Deleted", "Your account has been deleted.")
                self.master.master.destroy()
            else:
                messagebox.showerror("Error", "Account deletion failed.")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
