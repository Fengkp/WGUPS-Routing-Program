from src.Controller.PackageAllocation import *
from src.Model.Truck import Truck
# Manage truck deliveries
# Account for and keep track of time of day using truck average speed. Every time the total mileage meets a number
# divisible by the truck's average speed, an hour has passed.
# Call PackageAllocation to determine a list of packages with the most optimal route.


def deliver_packages2(package_table, trucks):
    ready_packages = prepare_packages(package_table)
    # Get the first package in the table
    current_package = first_package(package_table)
    load_truck(trucks[0], current_package, current_package.get_hub_distance())
    update_package_status(package_table, current_package, 'On route')
    delivery_list = []
    truck = trucks[0]
    while len(ready_packages) != 0:
        delivery = next_package2(current_package, ready_packages)
        delivery_list.append(delivery)
        if len(delivery_list) == truck.get_capacity():
            truck = switch_trucks(truck, trucks)
    deliver_packages(package_table, trucks)



    for i in range(0, len(trucks)):
        update_package_status(package_table, current_package, 'Delivered')
        delivery_package, distance = next_package2(current_package, ready_packages)
        load_truck(trucks[i], current_package, distance)
        if trucks[i].get_package_load() == trucks[i].get_capacity():
            current_truck = switch_trucks(truck, trucks)


        if len(delivery_list) < trucks[i].get_capacity():
            break
    return total_distance_travelled(trucks)

def switch_trucks(truck, trucks):
    truck_index = trucks.index(truck) + 1
    if truck_index > len(trucks):
        truck_index = 0
    return trucks[truck_index]


def update_ready_packages(ready_packages, delivered_package):
    address_key = delivered_package.get_address() + ',' + delivered_package.get_zip()
    if len(ready_packages[address_key]) > 1:
        ready_packages[address_key].pop(delivered_package.get_id())
    else:
        del ready_packages[address_key]


def update_package_status(package_table, current_package, new_status):
    package_table.get(current_package.get_id()).set_status(new_status)


def load_truck(truck, package, distance):
    truck.add_delivery(package)
    truck.add_mileage(distance)


def deliver_packages(package_table, trucks):
    while True:
        packages_to_ship = prepare_packages(package_table)
        if len(packages_to_ship) == 0:
            break
        for i in range(0, len(trucks)):
            delivery_list, delivery_mileage = \
                PackageAllocation(package_table, packages_to_ship).deliver_packages(trucks[i].get_capacity())
            trucks[i].add_deliveries(delivery_list)
            trucks[i].add_mileage(delivery_mileage + delivery_list[-1].get_hub_distance())
            if len(delivery_list) < trucks[i].get_capacity():
                break
    return total_distance_travelled(trucks)


def total_distance_travelled(trucks):
    total_distance = 0
    for truck in trucks:
        total_distance += truck.get_miles_travelled()
    return total_distance


# Returns a list of packages that are ready to be shipped. Packages with a status of 'On route' or 'Delivered'
# will be excluded.
def prepare_packages(package_table):
    ready_packages = dict()
    for package in package_table.get_all():
        if package.get_status() == 'Preparing for shipment':
            address_key = package.get_address() + ',' + package.get_zip()
            if ready_packages.get(address_key):
                ready_packages[address_key].update({package.get_id(): package})
            else:
                ready_packages.update({address_key: {package.get_id(): package}})
    return ready_packages


def first_package(package_table):
    package = package_table[next(iter(package_table))]
    return package