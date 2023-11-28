import csv
import random


class DistanceAPI:

    def __init__(self, in_filename="data/distances.csv"):
        self.addr_to_addr_to_distances: dict[str, dict[str, float]] = {}
        self.initialize(in_filename)

    def initialize(self, in_filename) -> None:
        with open(in_filename, "r", encoding='utf-8-sig') as in_file:
            field_names = ["Address1",
                           "Address2",
                           "kmApart"]
            reader = csv.DictReader(in_file, fieldnames=field_names)
            next(reader, None)  # skip the headers in the .csv
            for row in reader:
                address1 = row["Address1"]
                address2 = row["Address2"]
                km_apart = row["kmApart"]
                if address1 not in self.addr_to_addr_to_distances:
                    self.addr_to_addr_to_distances[address1] = {}
                self.addr_to_addr_to_distances[address1][address2] = float(km_apart)

    def get_distance(self, address1: str, address2: str) -> float:
        if address1 not in self.addr_to_addr_to_distances:
            raise ValueError(f"Distance API does not recognize first address: {address1}")
        if (address2 not in self.addr_to_addr_to_distances or
                address2 not in self.addr_to_addr_to_distances[address1]):
            raise ValueError(f"Distance API does not recognize second address: {address2}")

        return self.addr_to_addr_to_distances[address1][address2]


if __name__ == "__main__":
    dapi = DistanceAPI()
    how_many = len(dapi.addr_to_addr_to_distances)

    print(f"The Distance API knows how to look up the distance "
          f"between {how_many} "
          f"different addresses in the Pittsburgh area.")

    addresses = list(dapi.addr_to_addr_to_distances.keys())
    a1 = random.choice(addresses)
    a2 = random.choice(addresses)

    distance = dapi.get_distance(a1,a2)
    print(f"\nFor example, the distance between\n• {a1}\n• {a2}\nis {distance:.1f} km.")
