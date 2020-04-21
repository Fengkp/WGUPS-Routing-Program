from src.Objects.HashTable import Table
from src.PrepFiles import init_tables
from src.Objects.Truck import Truck
import datetime


# 13 not on the same truck as 15, 16, 19, 20
def deliver_packages(trucks, table):
    global package_table, current_time
    package_table = table
    priority_packages, regular_packages = determine_packages()
    delayed_packages = ['6', '25', '28', '32']
    truck_2_packages = ['3', '18', '36', '38']
    current_truck = trucks[0]
    while len(priority_packages) + len(regular_packages) + len(delayed_packages) > 0:
        # Add delayed packages to be picked up by the first truck back.
        if current_time.time() >= datetime.time(9, 5):
            add_packages(delayed_packages, priority_packages)
            delayed_packages.clear()
            add_packages(truck_2_packages, regular_packages)
            current_truck = trucks[1]
        build_delivery_list(priority_packages, regular_packages)
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
            current_time = add_time(current_time, lowest_mileage)
        # if len(priority_packages) + len(regular_packages) + len(delayed_packages) == 0:
        #     redirected_mileage = current_truck.get_deliveries()[-1][0].get_hub_distance()
        #     current_truck.adjust_mileage(-redirected_mileage)
        #     redirected_mileage = package_table.get('38').get_distance_table().get('300 State St,84103')[1]
        #     package_table.get('9').set_address(package_table.get('39').get_address())
        #     package_table.get('9').set_zip(package_table.get('39').get_zip())
        #     package_table.get('9').set_hub_distance(redirected_mileage)
        #     package_table.get('9').set_distance_table(package_table.get('38').get_distance_table)
        #     add_packages(['13'], priority_packages)
        #     build_delivery_list(priority_packages, regular_packages)
        #     current_truck.adjust_mileage(-redirected_mileage)
        #     current_truck.adjust_mileage(package_table.get('38').get_hub_distance())


def determine_packages():
    # Not 'EOD', along with packages to deliver together.
    priority_list = ['1', '6', '13', '14', '15', '16', '19', '20', '25', '29', '30', '31', '34', '37', '40']
    delayed_or_unimportant = ['6', '25', '28', '32', '3', '18', '36', '38']
    priority_table = Table(50)
    regular_table = Table(50)
    for package in package_table.get_all():
        if package.get_id() in priority_list and package.get_id() not in delayed_or_unimportant:
            priority_table.insert(package.get_id(), package)
        elif package.get_id() not in delayed_or_unimportant:
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


def build_delivery_list(priority_packages, regular_packages):
    temp_time = current_time
    current_package = find_closest_to_hub([priority_packages, regular_packages])
    temp_time = add_time(temp_time, current_package.get_hub_distance())
    update_package(current_package, current_package.get_hub_distance(), temp_time)
    while len(delivery_list) < 16:
        if len(priority_packages) + len(regular_packages) == 0:
            break
        # Split priority packages among both trucks, otherwise packages will not be delivered on time.
        if len(priority_packages) != 0 and len(delivery_list) < 10:
            current_package, distance = next_package(current_package, priority_packages)
        else:
            current_package, distance = next_package(current_package, regular_packages)
        temp_time = add_time(temp_time, distance)
        update_package(current_package, distance, temp_time)


def find_closest_to_hub(packages):
    closest_to_hub = []
    if len(packages[0]) != 0:
        package_list = packages[0]
    else:
        package_list = packages[1]
    for address in package_list.values():
        closest_to_hub += list(address.values())
    closest_to_hub.sort(key=lambda package: package.get_hub_distance())
    closest_package = closest_to_hub[0]
    update_list(closest_package, package_list)
    return closest_package


def add_time(temp_time, miles):
    elapsed_seconds = 3600 / 18 * miles
    temp_time = temp_time + datetime.timedelta(seconds=elapsed_seconds)
    return temp_time


def update_package(package, distance, temp_time):
    package_table.get(package.get_id()).set_time_delivered(temp_time)
    package_table.get(package.get_id()).set_status('Delivered')
    delivery_list.append([package, distance])


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


def add_packages(package_list, packages):
    new_packages = list()
    for package_id in package_list:
        new_packages.append(package_table.get(package_id))
    packages.update(packages_by_address(new_packages))


package_table = None
current_time = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month,
                                 datetime.datetime.today().day, 8)
delivery_list = list()