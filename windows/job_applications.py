import tkinter as tk
from tkinter import messagebox

import requests

from config import BASE_API_URL
from objects import Account, Application, Job


class JobApplicationsWindow(tk.Toplevel):
    """
    A window to view and manage applications for a specific job.
    recruiters (can manage status) and applicants (can apply or withdraw).
    """

    def __init__(self, master, cookies, user_account: Account, job: Job):
        """
        :param master: Parent window
        :param cookies: Session cookies for authenticated API access
        :param user_account: The current logged-in user
        :param job: The job for which applications are shown
        """
        super().__init__(master)
        self.cookies = cookies
        self.user_account = user_account
        self.job = job

        self.title(f"Applications - {job.title}")
        self.geometry("700x550")
        self.configure(bg="#f9f9f9")

        # Title header
        tk.Label(
            self,
            text=f"Applications for: {job.title}",
            font=("Arial", 16, "bold"),
            bg="#f9f9f9",
        ).pack(pady=(20, 10))

        # "New Application" for applicants
        if self.user_account.role == "applicant":
            tk.Button(
                self,
                text="New Application",
                command=self.open_new_application_window,
                bg="green",
                fg="white",
                font=("Arial", 10, "bold"),
                width=20,
                height=1,
            ).pack(pady=(0, 15))

        # Scrollable container
        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(container, highlightthickness=0, bg="#f9f9f9")
        self.scrollbar = tk.Scrollbar(
            container, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f9f9f9")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.refresh_applications()

    def refresh_applications(self):
        """
        Fetch and display applications for the current job.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            res = requests.get(
                f"{BASE_API_URL}/application/job/{self.job.job_id}",
                cookies=self.cookies,
                verify=False,
            )
            if res.status_code == 200:
                applications = res.json()
                if not applications:
                    tk.Label(
                        self.scrollable_frame,
                        text="No applications found.",
                        bg="#f9f9f9",
                    ).pack(pady=10)
                    return

                for app_data in applications:
                    self.render_application(app_data)
            else:
                messagebox.showerror(
                    "Error", f"Failed to fetch applications.\n{res.text}"
                )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def render_application(self, data):
        """
        Render a single application in the scrollable frame with status and buttons.
        """
        app = Application(
            application_id=data["application_id"],
            job_id=data["job_id"],
            account_id=data["account_id"],
            content=data["content"],
            status=data["status"],
        )

        frame = tk.Frame(
            self.scrollable_frame,
            relief="ridge",
            borderwidth=2,
            padx=15,
            pady=12,
            bg="white",
        )
        frame.pack(fill="x", padx=15, pady=10)

        # Application content
        tk.Label(
            frame,
            text=f"Content:\n{app.content}",
            anchor="w",
            justify="left",
            wraplength=550,
            font=("Arial", 11),
            bg="white",
        ).pack(fill="x", pady=(0, 6))

        # Status label with color
        status_colors = {
            "pending": "#f57c00",  # Orange
            "accepted": "#2e7d32",  # Green
            "rejected": "#c62828",  # Red
        }
        status_color = status_colors.get(app.status.lower(), "black")

        tk.Label(
            frame,
            text=f"Status: {app.status.capitalize()}",
            fg=status_color,
            font=("Arial", 10, "bold"),
            bg="white",
        ).pack(anchor="w", pady=(0, 10))

        # Recruiter controls with color-coded buttons
        if self.user_account.role == "recruiter":
            status_frame = tk.Frame(frame, bg="white")
            status_frame.pack(anchor="w", pady=5)

            for status, color in {
                "pending": "#f57c00",
                "accepted": "#2e7d32",
                "rejected": "#c62828",
            }.items():
                tk.Button(
                    status_frame,
                    text=f"Mark {status}",
                    command=lambda s=status, a=app: self.update_status(a, s),
                    width=12,
                    font=("Arial", 9),
                    bg=color,
                    fg="white",
                    activebackground=color,
                ).pack(side="left", padx=5)

        # Applicant controls
        elif self.user_account.role == "applicant":
            tk.Button(
                frame,
                text="Withdraw Application",
                command=lambda a=app: self.withdraw_application(a),
                bg="red",
                fg="white",
                padx=10,
                pady=5,
                font=("Arial", 10, "bold"),
            ).pack(pady=(5, 0))

    def update_status(self, app: Application, new_status: str):
        """
        Recruiter can update the status of an application.
        """
        try:
            res = requests.put(
                f"{BASE_API_URL}/application/{app.application_id}",
                json={
                    "application_id": app.application_id,
                    "job_id": app.job_id,
                    "account_id": app.account_id,
                    "content": app.content,
                    "status": new_status,
                },
                cookies=self.cookies,
                verify=False,
            )
            if res.status_code == 204:
                self.refresh_applications()
            else:
                messagebox.showerror("Error", f"Failed to update status.\n{res.text}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def withdraw_application(self, app: Application):
        """
        Applicants can delete their own applications.
        """
        confirm = messagebox.askyesno(
            "Withdraw", "Are you sure you want to withdraw this application?"
        )
        if not confirm:
            return

        try:
            res = requests.delete(
                f"{BASE_API_URL}/application/{app.application_id}",
                cookies=self.cookies,
                verify=False,
            )
            if res.status_code == 204:
                self.refresh_applications()
            else:
                messagebox.showerror(
                    "Error", f"Failed to delete application.\n{res.text}"
                )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_new_application_window(self):
        """
        Show a popup for applicants to submit a new application.
        """
        window = tk.Toplevel(self)
        window.title("New Application")
        window.geometry("400x300")
        window.configure(bg="#f9f9f9")

        tk.Label(window, text="Application Content:", bg="#f9f9f9").pack(pady=10)
        content_text = tk.Text(window, height=8, width=40)
        content_text.pack(pady=5)

        def submit_application():
            content = content_text.get("1.0", "end").strip()
            if not content:
                messagebox.showwarning("Validation", "Content cannot be empty.")
                return

            try:
                res = requests.post(
                    f"{BASE_API_URL}/application/job/{self.job.job_id}",
                    json={"content": content},
                    cookies=self.cookies,
                    verify=False,
                )
                if res.status_code in [200, 201]:
                    messagebox.showinfo("Success", "Application submitted.")
                    window.destroy()
                    self.refresh_applications()
                else:
                    messagebox.showerror("Error", f"Submission failed.\n{res.text}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            window,
            text="Submit",
            command=submit_application,
            bg="#007acc",
            fg="white",
            width=15,
        ).pack(pady=15)

    def _on_mousewheel(self, event):
        """
        Scroll the canvas using mouse wheel input.
        """
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
