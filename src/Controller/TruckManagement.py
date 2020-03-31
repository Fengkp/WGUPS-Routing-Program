from src.Controller.PackageAllocation import *


# Manage truck deliveries
class TruckManagement(object):
    def __init__(self, capacity):
        self.truck_capacity = capacity
        self.truck_count = 0
        self.truck_list = []

    def add_truck(self, truck):
        self.truck_list.append(truck)

    # Returns a list of packages that are ready to be shipped. Packages with a status of 'On route' or 'Delivered'
    # will be excluded.
    def prepare_packages(self, package_table):
        packages_to_ship = dict()
        for package in package_table.get_all():
            if package.get_status() == 'Preparing for shipment':
                address_key = package.get_address() + ',' + package.get_zip()
                if packages_to_ship.get(address_key):
                    packages_to_ship[address_key].update({package.get_id(): package})
                else:
                    packages_to_ship.update({address_key: {package.get_id(): package}})
        return packages_to_ship

# Call PackageAllocation to determine a list of packages with the most optimal route.
    def allocate_packages(self, package_table):
        total_mileage = 0.0
        while True:
            packages_to_ship = self.prepare_packages(package_table)
            if len(packages_to_ship) == 0:
                break
            delivery_list, delivery_mileage = PackageAllocation(package_table, packages_to_ship).step1(self.truck_capacity)
            total_mileage = total_mileage + delivery_mileage + delivery_list[-1].get_hub_distance()
            print("Total mileage: " + str(total_mileage))


    def deliver_packages(self):
        pass

# If a truck has 0 packages, it returns to HUB for more packages.
# This will call PackageAllocation to look at remaining packages in the PackageTable
# and determine the most optimal route based on current position.

# Change status of package to deliver.

# Make adjustments to package according to special notes.

# One of the assumptions states that a package has a wrong address.
# IF the package is delivered by 10:20 am, the closest truck, if there is available space, will have to go to
# the wrong address, update the address, then add it to the trucks package list for delivery.