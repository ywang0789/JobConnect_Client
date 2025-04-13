import tkinter as tk

import requests

from config import BASE_API_URL
from objects import Account, Job
from windows.create_job import CreateJobWindow


class JobsTab(tk.Frame):
    def __init__(self, master, cookies, user_account: Account):
        super().__init__(master)
        self.master = master
        self.user_account = user_account
        self.cookies = cookies

        # Recruiter-only "Create Job" button
        if self.user_account.role == "recruiter":
            tk.Button(self, text="Create New Job", command=self.create_job).pack(
                pady=(10, 0), anchor="e", padx=10
            )

        self.jobs_frame = tk.Frame(self)
        self.jobs_frame.pack(fill="both", expand=True)

        self.refresh_jobs()

    def refresh_jobs(self):
        for widget in self.jobs_frame.winfo_children():
            widget.destroy()

        try:
            res = requests.get(
                f"{BASE_API_URL}/job", cookies=self.cookies, verify=False
            )
            if res.status_code == 200:
                job_list = res.json()
                for job_data in job_list:
                    job = Job(**job_data)
                    self.add_job_widget(job)
            else:
                tk.Label(self.jobs_frame, text="Failed to load jobs.").pack(pady=10)
        except Exception as e:
            tk.Label(self.jobs_frame, text=f"Error: {str(e)}").pack(pady=10)

    def add_job_widget(self, job: Job):
        frame = tk.Frame(
            self.jobs_frame, relief="groove", borderwidth=2, padx=10, pady=10
        )
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text=job.title, font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(frame, text=f"Location: {job.location}").pack(anchor="w")
        tk.Label(frame, text=f"Salary: ${job.salary:,.2f}").pack(anchor="w")
        tk.Label(frame, text=job.description).pack(anchor="w")

        if self.user_account.role == "recruiter":
            btn_frame = tk.Frame(frame)
            btn_frame.pack(anchor="e", pady=(5, 0))

            tk.Button(
                btn_frame, text="Edit", command=lambda j=job: self.edit_job(j)
            ).pack(side="left", padx=5)
            tk.Button(
                btn_frame, text="Delete", command=lambda j=job: self.delete_job(j)
            ).pack(side="left", padx=5)

    def create_job(self):
        CreateJobWindow(self, self.cookies, self.refresh_jobs)

    def edit_job(self, job: Job):
        print(f"Edit job {job.job_id} clicked.")
        # You can implement a popup or switch to a job editing window here

    def delete_job(self, job: Job):
        try:
            res = requests.delete(
                f"{BASE_API_URL}/job/{job.job_id}", cookies=self.cookies, verify=False
            )
            if res.status_code == 204:
                tk.messagebox.showinfo("Success", "Job deleted successfully.")
                self.refresh_jobs()
            else:
                tk.messagebox.showerror("Error", "Failed to delete job.")
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
