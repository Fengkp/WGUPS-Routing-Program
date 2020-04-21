class Truck(object):
    def __init__(self, id):
        self.id = id
        self.capacity = 16      # Maximum amount of packages a truck can carry.
        self.average_speed = 18     # ...in miles per hour
        self.deliveries = []
        self.mileage = 0
        self.prev_mileage = 0

    def add_deliveries(self, packages):
        self.deliveries += packages
        self.prev_mileage = 0
        for package, distance in packages:
            self.prev_mileage += distance
        self.prev_mileage += packages[-1][0].get_hub_distance()
        self.add_mileage(self.prev_mileage)

    def add_delivery(self, package, mileage):
        self.package_count += 1
        self.deliveries.append(package)
        self.add_mileage(mileage)

    def get_deliveries(self):
        return self.deliveries

    def add_mileage(self, mileage):
        self.mileage += mileage

    def get_mileage(self):
        return self.mileage

    def adjust_mileage(self, amount):
        self.mileage += amount

    def get_prev_mileage(self):
        return self.prev_mileage

    def get_id(self):
        return self.id
