from datetime import datetime


class Project:
    def __init__(self,
                 client: str,
                 project_name: str,
                 address: str,
                 contract_date: datetime,
                 work_start_date: datetime,
                 work_completion_date: datetime):
        """

        :rtype: object
        """
        self.client = client
        self.project_name = project_name
        self.address = address
        self.contract_date = contract_date
        self.work_start_date = work_start_date
        self.work_completion_date = work_completion_date

    def __str__(self) -> str:
        return (f"{self.project_name} "
                f"for {self.client} "
                f"at {self.address.split(',')[0]}")

    def __repr__(self) -> str:
        return self.__str__()


class Vendor:
    def __init__(self,
                 name: str,
                 address: str,
                 ):
        self.name = name
        self.address = address

    def __str__(self) -> str:
        return f"{self.name} at {self.address}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return (self.name == other.name and
            self.address == other.address)

    def __cmp__(self, other) -> int:
        return self.address.__cmp__(other.address)

    def __hash__(self):
        return self.__str__().__hash__()


class Receipt:
    def __init__(self,
                 when: datetime,
                 vendor: Vendor,
                 amount: float):
        self.when = when
        self.vendor = vendor
        self.amount = amount
        self.project = None

    def set_project(self, project):
        self.project = project

    def __str__(self):
        return f"${self.amount:.2f} at {self.vendor} on {self.when}"

    def __repr__(self):
        return self.__str__()
