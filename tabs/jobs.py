import tkinter as tk

import requests

from config import BASE_API_URL
from objects import Account, Job
from windows.create_edit_job import CreateEditJobWindow


class JobsTab(tk.Frame):
    def __init__(self, master, cookies, user_account: Account):
        super().__init__(master, bg="#f5f5f5")
        self.master = master
        self.user_account = user_account
        self.cookies = cookies

        header = tk.Frame(self, bg="#f5f5f5")
        header.pack(fill="x", pady=(10, 0), padx=10)

        if self.user_account.role == "recruiter":
            tk.Button(
                header,
                text="Create New Job",
                command=self.create_job,
                bg="#007acc",
                fg="white",
                font=("Arial", 10, "bold"),
                padx=10,
                pady=5,
                relief="raised",
            ).pack(anchor="w")

        canvas_container = tk.Frame(self)
        canvas_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(
            canvas_container, bg="#f5f5f5", highlightthickness=0, bd=0
        )
        self.scrollbar = tk.Scrollbar(
            canvas_container, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5f5f5")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.refresh_jobs()

    def refresh_jobs(self):
        for widget in self.scrollable_frame.winfo_children():
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
                tk.Label(
                    self.scrollable_frame, text="Failed to load jobs.", bg="#f5f5f5"
                ).pack(pady=10)
        except Exception as e:
            tk.Label(self.scrollable_frame, text=f"Error: {str(e)}", bg="#f5f5f5").pack(
                pady=10
            )

    def add_job_widget(self, job: Job):
        frame = tk.Frame(
            self.scrollable_frame,
            relief="ridge",
            borderwidth=1,
            padx=10,
            pady=10,
            bg="white",
        )
        frame.pack(fill="x", padx=5, pady=8)

        tk.Label(frame, text=job.title, font=("Arial", 14, "bold"), bg="white").pack(
            anchor="w"
        )
        tk.Label(
            frame, text=f"Location: {job.location}", font=("Arial", 10), bg="white"
        ).pack(anchor="w")
        tk.Label(
            frame, text=f"Salary: ${job.salary:,.2f}", font=("Arial", 10), bg="white"
        ).pack(anchor="w")
        tk.Label(
            frame,
            text=job.description,
            font=("Arial", 10),
            wraplength=550,
            justify="left",
            bg="white",
        ).pack(anchor="w", pady=(5, 0))

        if self.user_account.role == "recruiter":
            btn_frame = tk.Frame(frame, bg="white")
            btn_frame.pack(anchor="e", pady=(10, 0))

            tk.Button(
                btn_frame, text="Edit", command=lambda j=job: self.edit_job(j), width=10
            ).pack(side="left", padx=5)
            tk.Button(
                btn_frame,
                text="Delete",
                command=lambda j=job: self.delete_job(j),
                width=10,
            ).pack(side="left", padx=5)

    def create_job(self):
        CreateEditJobWindow(self, self.cookies, self.refresh_jobs)

    def edit_job(self, job: Job):
        CreateEditJobWindow(self, self.cookies, self.refresh_jobs, job=job)

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

    def _on_mousewheel(self, event):
        """
        scrolls the canvas when the mouse wheel is used.
        """
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
