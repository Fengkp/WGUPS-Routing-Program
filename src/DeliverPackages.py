from src.Objects.HashTable import Table
from src.PrepFiles import init_tables
from src.Objects.Truck import Truck
import datetime


# PRETTY MUCH DONE. FIX WRONG ADDRESS PACKAGE AND UPDATE PACKAGE DELIVERY TIMES. VERIFY CONDITIONS ARE MET.
# Total mileage varies since it picks the first item in the package dictionaries, and those are "randomly" set.


def deliver_packages(trucks, table):
    global package_table
    package_table = table
    priority_packages, regular_packages = determine_packages()
    current_truck = trucks[0]
    while len(priority_packages) + len(regular_packages) > 0:
        if current_time.time() >= datetime.time(9, 5):
            delayed = ['6', '25', '28', '32']
            delayed_packages = list()
            for package_id in delayed:
                delayed_packages.append(package_table.get(package_id))
            priority_packages.update(packages_by_address(delayed_packages))
        first_package([priority_packages, regular_packages])
        current_truck.add_deliveries(delivery_list)
        delivery_list.clear()
        if current_truck.get_id() == 1:
            current_truck = trucks[1]
        else:
            lowest_mileage = trucks[0].get_prev_mileage()
            current_truck = trucks[0]
            for truck in trucks:
                if truck.get_prev_mileage() < lowest_mileage:
                    lowest_mileage = truck.get_prev_mileage()
                    current_truck = truck
            add_time(lowest_mileage)
    total = 0
    for truck in trucks:
        total += truck.get_mileage()
    print("Total mileage: " + str(total))

def first_package(packages):
    first_package = None
    for package_list in packages:
        if len(package_list) != 0:
            first_address = next(iter(package_list.values()))
            first_package = next(iter(first_address.values()))
            update_list(first_package, package_list)
            break
    delivery_list.append([first_package, first_package.get_hub_distance()])
    build_delivery_list(first_package, packages[0], packages[1])


def build_delivery_list(current_package, priority_packages, regular_packages):
    while len(delivery_list) < 16:
        if len(priority_packages) + len(regular_packages) == 0:
            break
        if len(priority_packages) != 0:
            current_package, distance = next_package(current_package, priority_packages)
        else:
            current_package, distance = next_package(current_package, regular_packages)
        delivery_list.append([current_package, distance])

def determine_packages():
    # Not 'EOD', along with packages to deliver together.
    priority_list = ['1', '6', '13', '14', '15', '16', '19', '20', '25', '29', '30', '31', '34', '37', '40']
    delayed = ['6', '25', '28', '32']
    priority_table = Table(50)
    regular_table = Table(50)
    for package in package_table.get_all():
        if package.get_id() in priority_list and package.get_id() not in delayed:
            priority_table.insert(package.get_id(), package)
        elif package.get_id() not in delayed:
            regular_table.insert(package.get_id(), package)
    priority_packages = packages_by_address(priority_table.get_all())
    regular_packages = packages_by_address(regular_table.get_all())
    return priority_packages, regular_packages


# Set initial table of packages indexed by address.
# The distance table csv uses the address as a key, not package id, so this makes it easier to navigate through
# packages when determining the distances. There will be duplicate addresses among packages, so we include them
# in a new dict w/in the address_table where now the package id is the key.
def packages_by_address(packages):
    address_table = dict()
    for package in packages:
        if address_table.get(package.get_address_key()):
            address_table[package.get_address_key()].update({package.get_id(): package})
        else:
            address_table.update({package.get_address_key(): {package.get_id(): package}})
    return address_table

# Determines the next package to be delivered and returns the distance from the previous package.
# It does so by going through each address in the current package's distance table, starting with the closest,
# then checks to see if it is in the address_table table. If it is then it determines that as the next packages.
# Also updates the address_table table so we don't include duplicates.
def next_package(package, packages):
    distance_table = package.get_distance_table().items()
    for address in distance_table:
        if packages.get(address[0]):
            package_list = packages.get(address[0])
            package = next(iter(package_list.values()))
            update_list(package, packages)
            return package, address[1]


def update_list(package, packages):
    if len(packages[package.get_address_key()]) > 1:
        package_list = packages[package.get_address_key()]
        del package_list[package.get_id()]
    else:
        del packages[package.get_address_key()]


def add_time(miles):
    global current_time
    elapsed_seconds = 3600 / 18 * miles
    current_time = current_time + datetime.timedelta(seconds=elapsed_seconds)


current_time = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month,
                                 datetime.datetime.today().day, 8)
delivery_list = list()
package_table = None
