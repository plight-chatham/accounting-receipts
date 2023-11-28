import math
import random
import datetime
import csv
import re

import googlemaps
from googlemaps import Client


def main():
    # connect to google maps API
    with open('apikey.txt') as f:
        api_key = f.readline()
        f.close()
    gmaps: Client = googlemaps.Client(api_key)

    # load the data we'll need to generate a bunch of receipts for the students to work on.
    projects: list[dict] = load_projects_from_csv()
    client_name_to_hardware_nearby = fetch_hardware_nearby(gmaps, projects)

    # now generate and write the receipts to disk
    receipts = generate_receipts(client_name_to_hardware_nearby, projects)
    write_receipts(receipts, "receipts.csv")
    write_receipts(receipts, "answer-key.csv", True)

    # make it possible to determine how far a particular store is from a job site
    # if all you have are the addresses.
    all_known_addresses = map_all_addresses_to_lat_long(client_name_to_hardware_nearby, projects)
    distance_lookup_table = compute_all_distances(all_known_addresses)
    distance_lookup_rows = []
    for address1 in distance_lookup_table:
        for address2 in distance_lookup_table[address1]:
            distance_lookup_rows.append({"Address1": address1,
                                         "Address2": address2,
                                         "kmApart": distance_lookup_table[address1][address2]})
    write_distance_lookup(distance_lookup_rows)


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
        nearby_results = list(filter(is_vendor_valid, nearby_results))

        client_name_to_hardware_nearby[project["Client"]] = nearby_results
    return client_name_to_hardware_nearby


def is_vendor_valid(vendor: dict) -> bool:
    """
    Report whether a particular vendor should be used for our simulation.

    :param vendor: a single result from a gmaps.places_nearby search
    :return: true if this vendor has an address which begins with a number.
    """
    return is_address_valid(vendor["vicinity"])


# A regular expression is a way of finding specific sequences of characters in a string.
# They get "compiled" before they use them, and then you can use them many times again
# and again. This particular one would match any string which has a sequence of numeric
# digits at the beginning of it. So "123 Any Street, Anytown USA" would be a match, but
# "Never in my lifetime" would not.
begins_with_a_number = re.compile("^[0-9]+.*")


def is_address_valid(address: str) -> bool:
    """
    Identify whether a given street address appears to be valid.

    This is a much deeper topic than this code can handle; for our purposes we just
    want to report whether an address begins with a number.

    :param address: a [US] street address
    :return: true if the address begins with a number
    """
    return begins_with_a_number.match(address) is not None


def generate_receipts(client_name_to_hardware_nearby: dict[str, list[any]],
                      projects: list[dict[str, any]],
                      num_receipts=500) -> list[dict[str, any]]:
    """
    Invent the requested number of receipts which represent purchases made while working on
    a particular construction job. Each receipt will be turned in by a random worker, at a
    time which is before or during a project's calendar dates. Receipts should be for a
    dollar cost which looks somewhat realistic. Workers who are on a particular job and who
    need to get something for that project will visit one of the retailers near the job site,
    chosen at random, and get the items that they need.

    :param client_name_to_hardware_nearby: a dictionary mapping a client's name to the
      hardware stores in the area.
    :param projects: all the details about construction projects including address, client,
      and date range.
    :param num_receipts: how many receipts are desired
    :return: a list which contains num_receipts dictionaries, each one with the details
      about a particular purchase of supplies.
    """
    # generate a bunch of plausible receipts, each one associated with a particular project.
    print(f"generating {num_receipts} receipts for {len(projects)} projects.")
    receipts = []
    for i in range(num_receipts):
        project = random.choice(projects)
        receipt_date = pick_date_for_receipt(project)
        # randomly pick a vendor from the ones near this project.
        vendor = select_nearby_vendor(client_name_to_hardware_nearby, project["Client"])

        # exponential distribution with relatively many small receipt values, and a few
        # larger ones
        receipt_amount = round(random.expovariate(7) * 4500.0, 2)
        receipts.append({"Date": receipt_date,
                         "Supplier": vendor["name"],
                         "Supplier Address": vendor["vicinity"],
                         "Amount": receipt_amount,
                         "Client": project["Client"]})
    return receipts


def select_nearby_vendor(client_name_to_hardware_nearby: dict[str, list[dict[str, any]]],
                         client_name: str):
    """
    For the indicated client project, return the name of a single hardware vendor
    near the job site

    :param client_name_to_hardware_nearby: a dictionary which provides a list of
      vendor options for any client name
    :param client_name: a single client that we should select a vendor for.
    :return: a vendor listing (which is a dictionary with all details.)
    """
    vendors = client_name_to_hardware_nearby[client_name]
    return random.choice(vendors)


def pick_date_for_receipt(project):
    """
    given a project, pick a suitable date for our fake receipt. we will simulate that
    most of the runs to a hardware store fall near the middle of the project time.

    :param project: a dict containing project details, including contract start date,
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


def write_receipts(receipts, out_file_name, include_clients=False):
    # output
    print(f"writing {len(receipts)} receipts {include_clients}")
    with open(out_file_name, 'w', encoding='utf-8-sig') as receipt_file:
        field_names = ["Date",
                       "Supplier",
                       "Supplier Address",
                       "Amount"]
        if include_clients:
            field_names.append("Client")
        writer = csv.DictWriter(receipt_file, fieldnames=field_names)
        writer.writeheader()
        for receipt in receipts:
            write_me = {"Date": receipt["Date"],
                        "Supplier": receipt["Supplier"],
                        "Supplier Address": receipt["Supplier Address"],
                        "Amount": receipt["Amount"]}
            if include_clients:
                write_me["Client"] = receipt["Client"]

            writer.writerow(write_me)


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


def compute_all_distances(all_known_addresses: dict[dict]) -> dict[dict[float]]:
    result = {}
    for address1 in all_known_addresses:
        lat_long_1 = all_known_addresses[address1]
        distances = {}
        result[address1] = distances

        for address2 in all_known_addresses:
            lat_long_2 = all_known_addresses[address2]
            distances[address2] = pythagorean_distance(lat_long_1, lat_long_2)
    return result


def pythagorean_distance(lat_long_1, lat_long_2):
    """
    This function computes a very crude distance approximation between
    two latitude/longitude pairs. It takes the lat/long and computes the
    pythagorean distance between those points, then multiplies that number
    by 111.1, because that's the distance in km of 1 degree of latitude.

    That is pretty bogus cartographically, but it's a reasonable approximation
    of how far apart the two points are.

    :param lat_long_1: a dictionary which maps "lat" and "lng" to a float value
    :param lat_long_2: a dictionary which maps "lat" and "lng" to a float value
    :return: the approximate distance (in km) between these two points on the earth.
    """
    lat_distance = abs(lat_long_2["lat"] - lat_long_1["lat"])
    lng_distance = abs(lat_long_2["lng"] - lat_long_1["lng"])
    dist_in_degrees = math.sqrt(lat_distance ** 2 + lng_distance ** 2)
    return dist_in_degrees * 111.1


def write_distance_lookup(distance_lookup_rows: list[dict]) -> None:
    print(f"writing {len(distance_lookup_rows)} distance mappings")
    with open('distances.csv', 'w', encoding='utf-8-sig') as receipt_file:
        field_names = ["Address1",
                       "Address2",
                       "kmApart"]
        writer = csv.DictWriter(receipt_file, fieldnames=field_names)
        writer.writeheader()
        for lookup in distance_lookup_rows:
            writer.writerow(lookup)


def parse_date(date_str: str) -> datetime.datetime:
    """
    Accepts a string which contains a date in the form MM/DD/YYYY and
    return that datetime.

    :param date_str: a string containing a single date.
    :return: a datetime object representing the corresponding date.
    """
    return datetime.datetime.strptime(date_str, "%m/%d/%y")


if __name__ == "__main__":
    main()
