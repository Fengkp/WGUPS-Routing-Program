from src.Controller.PackageAllocation import *


# Manage truck deliveries
class TruckManagement(object):
    def __init__(self, limit):
        self.truck_limit = limit
        self.truck_count = 0
        self.truck_list = []

    def add_truck(self, truck):
        self.truck_list.append(truck)

# Call PackageAllocation to determine a list of packages with the most optimal route.
    def allocate_packages(self):
        list_1 = PackageAllocation('195 W Oakland Ave,84115').step1()




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