from src.Controller.PackageAllocation import *
from src.Model.Truck import Truck
# Manage truck deliveries
# Account for and keep track of time of day using truck average speed. Every time the total mileage meets a number
# divisible by the truck's average speed, an hour has passed.
# Call PackageAllocation to determine a list of packages with the most optimal route.
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
    packages_to_ship = dict()
    for package in package_table.get_all():
        if package.get_status() == 'Preparing for shipment':
            address_key = package.get_address() + ',' + package.get_zip()
            if packages_to_ship.get(address_key):
                packages_to_ship[address_key].update({package.get_id(): package})
            else:
                packages_to_ship.update({address_key: {package.get_id(): package}})
    return packages_to_ship