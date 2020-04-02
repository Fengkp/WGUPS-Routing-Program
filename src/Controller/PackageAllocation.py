# Algorithm to decide which packages go on which truck
# Return packages in lists?
# For now we'll just use the address.
# In the future, the first address to be noted will be the hub address.
# This address/distance will be referenced every time a truck runs out of packages.
class PackageAllocation(object):
    def __init__(self, package_table, packages):
        self.package_table = package_table
        self.packages_to_ship = packages
        self.delivery_mileage = 0.0
        self.current_package = self.set_first_package()
        self.delivery_list = []

    def deliver_packages(self, capacity):
        while len(self.delivery_list) < capacity:
            if len(self.packages_to_ship) == 0:
                break
            self.update_status('On route')
            self.update_packages_to_ship()
            self.load_package()
            self.update_status('Delivered')
            self.next_package()
        print("Distance travelled: " + str(self.delivery_mileage))
        return self.delivery_list, self.delivery_mileage

    def next_package(self):
        for item in self.current_package.get_distance_table().items():
            if self.packages_to_ship.get(item[0]):
                self.current_package = self.packages_to_ship[item[0]][next(iter(self.packages_to_ship[item[0]]))]
                self.delivery_mileage += item[1]
                break

    def update_packages_to_ship(self):
        address_key = self.current_package.get_address() + ',' + self.current_package.get_zip()
        if len(self.packages_to_ship[address_key]) > 1:
            self.packages_to_ship[address_key].pop(self.current_package.get_id())
        else:
            del self.packages_to_ship[address_key]

    def update_status(self, new_status):
        self.package_table.get(self.current_package.get_id()).set_status(new_status)

    def load_package(self):
        self.delivery_list.append(self.current_package)

    def set_first_package(self):
        package_list = self.packages_to_ship[next(iter(self.packages_to_ship))]
        first_package = package_list[next(iter(package_list))]
        self.delivery_mileage += first_package.get_hub_distance()
        return first_package
