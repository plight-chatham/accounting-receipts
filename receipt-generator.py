import random
import datetime
import csv
import googlemaps


def pick_vendor_from_list(client_name_to_hardware_nearby, client_name):
    vendors = client_name_to_hardware_nearby[client_name]
    return random.choice(vendors)


def main():

    # connect to google maps API
    with open('apikey.txt') as f:
        api_key = f.readline()
        f.close()
    gmaps = googlemaps.Client(api_key)

    # load the data we'll need to generate a bunch of receipts for the students to work on.
    projects = load_projects_from_csv()
    client_name_to_hardware_nearby = fetch_hardware_nearby(gmaps, projects)

    # generate a bunch of plausible receipts, each one associated with a particular project.
    receipts = []
    for i in range(350):
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

    # output
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


def fetch_hardware_nearby(gmaps, projects):
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
        nearby_hardware = gmaps.places_nearby(location=project_lat_long,
                                              keyword="hardware",
                                              radius=10000)

        client_name_to_hardware_nearby[project["Client"]] = nearby_hardware["results"]
    return client_name_to_hardware_nearby


def load_projects_from_csv():
    """
    open the file projects.csv to find a list of projects. Each project contains (at least)
    a value for Client, Contract Start date, Work Start and End dates, and Address.
    :return: a list of maps, each map representing the info about one project.
    """
    projects = []
    with open("projects.csv", "r", encoding='utf-8-sig') as projectsFile:
        project_reader = csv.DictReader(projectsFile)
        for row in project_reader:
            projects.append(row)
    return projects


def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%m/%d/%y")


if __name__ == "__main__":
    main()
