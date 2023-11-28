import datetime
from distance_api import DistanceAPI
from receipt_classes import Receipt, Project, Vendor
import csv


def main():
    """
    Load the projects and receipts from their input files,
    then try to determine which project each receipt came from.

    Output the results to a new CSV file which includes all the details
    for each receipt, and adds a new column revealing which project
    the receipt is likely associated with.

    You will want to consider location and date of the transaction
    in order to make your guess.
    """
    projects = load_projects_from_csv()
    print_summary_of_projects(projects)

    receipts = load_receipts_from_csv()
    print_summary_of_receipts(receipts)

    dapi = DistanceAPI()

    #
    # YOUR CODE HERE
    #
    # 1. Which project does each receipt belong to?
    # 2. Print the results out to a CSV file.
    #


# noinspection PyTypeChecker
def load_projects_from_csv() -> list[Project]:
    """
    open the file projects.csv to find a list of projects. Each project contains
    a value for Client, Contract Start date, Work Start and End dates, and Address.
    :return: a list of Projects, filled out with all info.
    """
    projects: list[Project] = []
    with open("data/projects.csv", "r", encoding='utf-8-sig') as projectsFile:
        project_reader = csv.DictReader(projectsFile)
        for row in project_reader:
            project = Project(row["Client"],
                              row["Project Name"],
                              row["Address"],
                              datetime.datetime.strptime(row["Contract Date"],"%m/%d/%y"),
                              datetime.datetime.strptime(row["Work Start Date"], "%m/%d/%y"),
                              datetime.datetime.strptime(row["Work Completion Date"], "%m/%d/%y")
                              )
            projects.append(project)
    return projects


def load_receipts_from_csv() -> list[Receipt]:
    """

    :return:
    """
    # you should remove 'pass' and write code here.
    pass


def print_summary_of_projects(projects: list[Project]) -> None:
    print("Projects:")
    for project in projects:
        print(f"• Started on {project.work_start_date}: {project}. ")


def print_summary_of_receipts(receipts: list[Receipt]) -> None:
    vendors = set()
    total_spend = 0
    for receipt in receipts:
        vendors.add(receipt.vendor)
        total_spend += receipt.amount

    print(f"There are {len(receipts)} receipts "
          f"from {len(vendors)} unique vendors. \n"
          f"Total spend: ${total_spend:.2f}. "
          f"Average receipt amount: ${total_spend/len(receipts):.2f}")


if __name__ == "__main__":
    main()
