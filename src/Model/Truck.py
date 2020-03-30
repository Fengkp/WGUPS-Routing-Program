class Truck(object):
    def __init__(self, id):
        self.truck_id = id
        self.max_packages = 16      # Maximum amount of packages a truck can carry.
        self.average_speed = 18     # ...in miles per hour
        self.current_package_list = []

    def add_package(self, package):
        self.current_package_list.append(package)
