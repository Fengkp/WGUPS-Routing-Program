# Algorithm to decide which packages go on which truck
# Return packages in lists?
# For now we'll just use the address.
# In the future, the first address to be noted will be the hub address.
# This address/distance will be referenced every time a truck runs out of packages.


class PackageAllocation(object):
    def __init__(self, starting_address):
        self.packages_to_ship = dict()
        self.prepare_packages()
        self.current_package = self.packages_to_ship[starting_address][next(iter(self.packages_to_ship[starting_address]))]
        self.delivery_list = []

    def step1(self):
        while len(self.delivery_list) < 16:
            self.update_package_tables()
            self.load_package()
            self.next_package()
        return self.delivery_list

    def next_package(self):
        for item in self.current_package.get_distance_table().items():
            if self.packages_to_ship[item[0]]:
                self.current_package = self.packages_to_ship[item[0]]

    def update_package_tables(self):
        from src.View.Interface import package_table
        package_table.get(self.current_package.get_id()).set_status('On route')
        address_key = self.current_package.get_address() + ',' + self.current_package.get_zip()
        del self.packages_to_ship[address_key][self.current_package.get_id()]


        del self.packages_to_ship[self.current_package.get_id()]        # Split later as the last step

    def load_package(self):
        self.delivery_list.append(self.current_package)

    # Returns a list of packages that are ready to be shipped. Packages with a status of 'On route' or 'Delivered'
    # will be excluded.
    def prepare_packages(self):
        from src.View.Interface import package_table
        for package in package_table.get_all():
            if package.get_status() == 'Preparing for shipment':
                address_key = package.get_address() + ',' + package.get_zip()
                if self.packages_to_ship.get(address_key):
                    self.packages_to_ship[address_key].update({package.get_id(): package})
                else:
                    self.packages_to_ship.update({address_key: {package.get_id(): package}})