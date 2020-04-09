class Truck(object):
    def __init__(self, id):
        self.id = id
        self.capacity = 16      # Maximum amount of packages a truck can carry.
        self.average_speed = 18     # ...in miles per hour
        self.deliveries = []
        self.mileage = 0
        self.package_count = 0

    def reset_package_count(self):
        self.package_count = 0

    def add_delivery(self, package, mileage):
        self.package_count += 1
        self.deliveries.append(package)
        self.add_mileage(mileage)

    def get_last_package(self):
        return self.deliveries[-1]

    def get_capacity(self):
        return self.capacity

    def add_mileage(self, mileage):
        self.mileage += mileage

    def get_mileage(self):
        return self.mileage

    def get_package_count(self):
        return self.package_count

    def get_deliveries(self):
        return self.deliveries

    def get_id(self):
        return self.id
