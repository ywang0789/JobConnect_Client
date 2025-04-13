import tkinter as tk
from tkinter import messagebox

import requests

from config import BASE_API_URL


class CreateEditJobWindow(tk.Toplevel):
    """
    handles both creating and editing jobs depending on the job parameter
    if job is None, it will create a new job
    """

    def __init__(self, master, cookies, on_success, job=None):
        super().__init__(master)
        self.job = job
        self.title("Edit Job" if job else "Create New Job")
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

        if job:  # Edit mode
            self.title_entry.insert(0, job.title)
            self.location_entry.insert(0, job.location)
            self.salary_entry.insert(0, str(job.salary))
            self.description_text.insert("1.0", job.description)

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
            if self.job:  # Edit mode
                data["job_id"] = self.job.job_id  # <- Add this line
                res = requests.put(
                    f"{BASE_API_URL}/job/{self.job.job_id}",
                    json=data,
                    cookies=self.cookies,
                    verify=False,
                )
            else:  # Create mode
                res = requests.post(
                    f"{BASE_API_URL}/job",
                    json=data,
                    cookies=self.cookies,
                    verify=False,
                )

            if res.status_code in [200, 204, 201]:
                messagebox.showinfo("Success", "Job saved successfully!")
                self.destroy()
                self.on_success()
            else:
                messagebox.showerror("Error", f"Failed to save job.\n{res.text}")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
