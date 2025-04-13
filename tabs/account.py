import tkinter as tk
from tkinter import messagebox

import requests

from config import BASE_API_URL
from objects import Account


class AccountTab(tk.Frame):
    """
    Tab for displaying user account information and performing account actions
    like logout and account deletion.
    """

    def __init__(self, master, cookies, user_account: Account):
        """
        Initialize the Account tab.
        :param master: The notebook parent widget
        :param cookies: Authenticated session cookies
        :param user_account: The logged-in user account data
        """
        super().__init__(master, bg="#f9f9f9")
        self.cookies = cookies
        self.user_account = user_account

        tk.Label(
            self, text="Account Information", font=("Arial", 16, "bold"), bg="#f9f9f9"
        ).pack(pady=(20, 10))

        # Display user details
        info_frame = tk.Frame(self, bg="#f9f9f9")
        info_frame.pack(pady=10)

        tk.Label(
            info_frame,
            text=f"Name: {user_account.first_name} {user_account.last_name}",
            font=("Arial", 12),
            bg="#f9f9f9",
        ).pack(anchor="w", pady=4)

        tk.Label(
            info_frame,
            text=f"Email: {user_account.email}",
            font=("Arial", 12),
            bg="#f9f9f9",
        ).pack(anchor="w", pady=4)

        tk.Label(
            info_frame,
            text=f"Role: {user_account.role.capitalize()}",
            font=("Arial", 12),
            bg="#f9f9f9",
        ).pack(anchor="w", pady=4)

        # Action buttons
        action_frame = tk.Frame(self, bg="#f9f9f9")
        action_frame.pack(pady=20)

        tk.Button(
            action_frame,
            text="Logout",
            command=self.logout,
            width=15,
            bg="#007acc",
            fg="white",
        ).pack(pady=5)

        tk.Button(
            action_frame,
            text="Delete Account",
            command=self.delete_account,
            width=15,
            bg="#c62828",
            fg="white",
        ).pack(pady=5)

    def logout(self):
        """
        Log out the current user and return to the login screen.
        """
        try:
            res = requests.post(
                f"{BASE_API_URL}/account/logout", cookies=self.cookies, verify=False
            )
            if res.status_code == 200:
                messagebox.showinfo("Logged Out", "You have been logged out.")
                self.master.master.destroy()
                from windows.login import LoginWindow

                LoginWindow().mainloop()
            else:
                messagebox.showerror("Error", "Logout failed.")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def delete_account(self):
        """
        Permanently delete the user's account after confirmation.
        """
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
                from windows.login import LoginWindow

                LoginWindow().mainloop()
            else:
                messagebox.showerror("Error", "Account deletion failed.")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
