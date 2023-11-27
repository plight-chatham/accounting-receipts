import random
import datetime
import csv
import re
from typing import List

import googlemaps
from googlemaps import Client

begins_with_a_number = re.compile("^[0-9]+.*")


def main():
    # connect to google maps API
    with open('apikey.txt') as f:
        api_key = f.readline()
        f.close()
    gmaps: Client = googlemaps.Client(api_key)

    # load the data we'll need to generate a bunch of receipts for the students to work on.
    projects: list[dict] = load_projects_from_csv()
    client_name_to_hardware_nearby = fetch_hardware_nearby(gmaps, projects)

    receipts = generate_receipts(client_name_to_hardware_nearby, projects)
    write_receipts(receipts)

    all_known_addresses = map_all_addresses_to_lat_long(client_name_to_hardware_nearby, projects)
    # distance_lookup_table = compute_all_distances(all_known_addresses)


# noinspection PyTypeChecker
def load_projects_from_csv() -> list[dict]:
    """
    open the file projects.csv to find a list of projects. Each project contains (at least)
    a value for Client, Contract Start date, Work Start and End dates, and Address.
    :return: a list of maps, each map representing the info about one project.
    """
    projects: list[dict] = []
    with open("projects.csv", "r", encoding='utf-8-sig') as projectsFile:
        project_reader = csv.DictReader(projectsFile)
        for row in project_reader:
            projects.append(row)
    return projects


def fetch_hardware_nearby(gmaps: Client, projects):
    """
    for each construction project in a list, determine what hardware stores
    are nearby the job site.

    :param gmaps: a Google Maps client
    :param projects: a list of dictionaries representing different projects
    :return: the hardware stores which are within a 10km (6mi) radius of each
      project. Results are returned as a map from client name to nearby locations.
    """
    client_name_to_hardware_nearby = {}
    # when = datetime.date(2022,1,1) + datetime.timedelta(float(random.randint(1,365)))
    # fetch the hardware stores near each project

    for project in projects:
        project_location = gmaps.geocode(project["Address"])[0]
        project_lat_long = project_location["geometry"]["location"]
        project["location"] = project_location
        project["lat_long"] = project_lat_long
        nearby_hardware = gmaps.places_nearby(location=project_lat_long,
                                              keyword="hardware",
                                              radius=10000)

        # there's a specific True Value retailer whose address is just "White Oak."
        # this doesn't look "right", so we are going to remove any vendors who have
        # addresses which don't contain a street number.
        nearby_results = nearby_hardware["results"]
        nearby_results = list(filter(lambda loc: begins_with_a_number.match(loc["vicinity"]) is not None,
                                     nearby_results))

        client_name_to_hardware_nearby[project["Client"]] = nearby_results
    return client_name_to_hardware_nearby


def generate_receipts(client_name_to_hardware_nearby, projects, num_receipts=350):
    # generate a bunch of plausible receipts, each one associated with a particular project.
    print(f"generating {num_receipts} receipts for {len(projects)} projects.")
    receipts = []
    for i in range(num_receipts):
        project = random.choice(projects)
        receipt_date = pick_date_for_receipt(project)
        # randomly pick a vendor from the ones near this project.
        vendor = pick_vendor_from_list(client_name_to_hardware_nearby, project["Client"])

        # exponential distribution with relatively many small receipt values, and a few
        # larger ones
        receipt_amount = round(random.expovariate(7) * 4500.0, 2)
        receipts.append({"Date": receipt_date,
                         "Employee Name": "H. Worker",
                         "Supplier": vendor["name"],
                         "Supplier Address": vendor["vicinity"],
                         "Amount": receipt_amount})
    return receipts


def pick_vendor_from_list(client_name_to_hardware_nearby, client_name):
    vendors = client_name_to_hardware_nearby[client_name]
    return random.choice(vendors)


def pick_date_for_receipt(project):
    """
    given a project, pick a suitable date for our fake receipt. we will simulate that
    most of the runs to a hardware store fall near the middle of the project time.

    :param project: a map containing project details, including contract start date,
      and work completion date. We want to pick a date which is somewhere between those
      times, with a gaussian distribution.
    :return: a date which (roughly) falls between contract date and end of work date.
      the dates will follow a gaussian distribution between the start and end dates.
    """
    # figure out how many days between contract start date and work completion date
    project_start = parse_date(project["Contract Date"])
    project_end = parse_date(project["Work Completion Date"])
    days_between = (project_end - project_start).days
    # generate a date during the project
    # 1. pick a number with a gaussian distribution centered at 0.5
    random_gauss = random.gauss(0.5, 0.2)
    # 2. how many days into this project will this receipt fall on?
    receipt_days_in = round(days_between * random_gauss, 0)
    # 3. what day on the calendar is this?
    receipt_date = (project_start + datetime.timedelta(receipt_days_in)).date()
    return receipt_date


def write_receipts(receipts):
    # output
    print(f"writing {len(receipts)} receipts")
    with open('receipts.csv', 'w', encoding='utf-8-sig') as receipt_file:
        field_names = ["Date",
                       "Employee Name",
                       "Supplier",
                       "Supplier Address",
                       "Amount"]
        writer = csv.DictWriter(receipt_file, fieldnames=field_names)
        writer.writeheader()
        for receipt in receipts:
            writer.writerow(receipt)


def map_all_addresses_to_lat_long(client_name_to_hardware_nearby: dict, projects: list[dict]) -> dict:
    result = {}

    # first, map all the project addresses to their lat/longs
    for project in projects:
        result[project["Address"]] = project["lat_long"]

    # now, do the same for all vendors
    for client_name in client_name_to_hardware_nearby:
        for vendor in client_name_to_hardware_nearby[client_name]:
            result[vendor["vicinity"]] = vendor["geometry"]["location"]
            pass
            # result[vendor["Address"]]

    return result


def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%m/%d/%y")


if __name__ == "__main__":
    main()
