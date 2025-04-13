class Account:
    """
    Class representing the user account currently logged in.
    """

    def __init__(
        self,
        Id: str,
        first_name: str,
        last_name: str,
        email: str,
        role: str,
    ):
        self.Id = Id
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.email = email


class Job:
    """
    Class representing a job
    """

    def __init__(
        self, job_id: int, title: str, description: str, salary: float, location: str
    ):
        self.job_id = job_id
        self.title = title
        self.description = description
        self.salary = salary
        self.location = location


class Application:
    """
    class representing a application
    """

    def __init__(
        self,
        application_id: int,
        job_id: int,
        account_id: str,
        content: str,
        status: str,
    ):
        self.application_id = application_id
        self.job_id = job_id
        self.account_id = account_id
        self.content = content
        self.status = status
