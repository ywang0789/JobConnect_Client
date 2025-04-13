import tkinter as tk
from tkinter import messagebox

import requests

from config import BASE_API_URL


class CreateEditJobWindow(tk.Toplevel):
    """
    A window for creating a new job or editing an existing one.
    The same interface adapts based on whether a job object is passed in.
    """

    def __init__(self, master, cookies, on_success, job=None):
        """
        :param master: Parent window
        :param cookies: Authenticated session cookies
        :param on_success: Callback function to call after successful submission
        :param job: (Optional) Job object to edit if no job is passed, its new job mode
        """
        super().__init__(master)
        self.job = job
        self.title("Edit Job" if job else "Create New Job")
        self.geometry("400x450")
        self.configure(bg="#f9f9f9")
        self.cookies = cookies
        self.on_success = on_success

        # Title Label
        tk.Label(
            self,
            text="Edit Job Details" if job else "Create New Job",
            font=("Arial", 14, "bold"),
            bg="#f9f9f9",
        ).pack(pady=20)

        # Form frame
        form_frame = tk.Frame(self, bg="#f9f9f9")
        form_frame.pack(padx=20, pady=10, fill="x")

        # Title
        tk.Label(form_frame, text="Job Title", anchor="w", bg="#f9f9f9").pack(fill="x")
        self.title_entry = tk.Entry(form_frame, width=40)
        self.title_entry.pack(pady=(0, 10))

        # Location
        tk.Label(form_frame, text="Location", anchor="w", bg="#f9f9f9").pack(fill="x")
        self.location_entry = tk.Entry(form_frame, width=40)
        self.location_entry.pack(pady=(0, 10))

        # Salary
        tk.Label(form_frame, text="Salary", anchor="w", bg="#f9f9f9").pack(fill="x")
        self.salary_entry = tk.Entry(form_frame, width=40)
        self.salary_entry.pack(pady=(0, 10))

        # Description
        tk.Label(form_frame, text="Description", anchor="w", bg="#f9f9f9").pack(
            fill="x"
        )
        self.description_text = tk.Text(form_frame, height=5, width=40)
        self.description_text.pack(pady=(0, 10))

        # Prefill if editing
        if job:
            self.title_entry.insert(0, job.title)
            self.location_entry.insert(0, job.location)
            self.salary_entry.insert(0, str(job.salary))
            self.description_text.insert("1.0", job.description)

        # Submit button
        tk.Button(
            self,
            text="Submit",
            command=self.submit_job,
            width=20,
            bg="#007acc",
            fg="white",
        ).pack(pady=20)

    def submit_job(self):
        """
        Validate input and send API request to create or update a job.
        """
        data = {
            "title": self.title_entry.get().strip(),
            "location": self.location_entry.get().strip(),
            "description": self.description_text.get("1.0", "end").strip(),
        }

        # Validate salary
        try:
            data["salary"] = float(self.salary_entry.get().strip())
        except ValueError:
            messagebox.showerror("Validation Error", "Salary must be a valid number.")
            return

        # Check all fields
        if not all(data.values()):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        try:
            if self.job:
                data["job_id"] = self.job.job_id
                res = requests.put(
                    f"{BASE_API_URL}/job/{self.job.job_id}",
                    json=data,
                    cookies=self.cookies,
                    verify=False,
                )
            else:
                res = requests.post(
                    f"{BASE_API_URL}/job",
                    json=data,
                    cookies=self.cookies,
                    verify=False,
                )

            if res.status_code in [200, 201, 204]:
                messagebox.showinfo("Success", "Job saved successfully!")
                self.destroy()
                self.on_success()
            else:
                messagebox.showerror("Error", f"Failed to save job.\n{res.text}")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
