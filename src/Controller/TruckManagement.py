from src.Controller.PackageAllocation import *
from src.Model.Truck import Truck
# Manage truck deliveries
# Account for and keep track of time of day using truck average speed. Every time the total mileage meets a number
# divisible by the truck's average speed, an hour has passed.
# Call PackageAllocation to determine a list of packages with the most optimal route.
def deliver_packages(package_table, trucks):
    capacity = 16
    ready_packages = prepare_packages(package_table)
    init_trucks(trucks, ready_packages)
    truck = trucks[0]
    while len(ready_packages) != 0:
        if truck.get_package_count() == capacity:
            go_home(truck)
            package = hub_package(ready_packages)
            truck.add_delivery(package, package.get_hub_distance())
        else:
            package = truck.get_deliveries()[-1]
            package, distance = next_package(package, ready_packages)
            truck.add_delivery(package, distance)
        update_ready_packages(package, ready_packages)
        truck = switch_trucks(truck, trucks)
    return total_distance(trucks)


def total_distance(trucks):
    distance = 0
    for truck in trucks:
        go_home(truck)
        distance += truck.get_mileage()
    return distance


def init_trucks(trucks, ready_packages):
    for truck in trucks:
        package = hub_package(ready_packages)
        truck.add_delivery(package, package.get_hub_distance())
        update_ready_packages(package, ready_packages)


def go_home(truck):
    truck.add_mileage(truck.get_deliveries()[-1].get_hub_distance())
    truck.reset_package_count()


def hub_package(ready_packages):
    package_list = ready_packages[next(iter(ready_packages))]
    package = package_list[next(iter(package_list))]
    return package


def update_ready_packages(package, ready_packages):
    if len(ready_packages[package.get_address_key()]) > 1:
        package_list = ready_packages[package.get_address_key()]
        del package_list[package.get_id()]
    else:
        del ready_packages[package.get_address_key()]


def switch_trucks(truck, trucks):
    new_truck_index = trucks.index(truck) + 1
    if new_truck_index == len(trucks):
        new_truck_index = 0
    return trucks[new_truck_index]


def update_package_status(package_table, current_package, new_status):
    package_table.get(current_package.get_id()).set_status(new_status)


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


