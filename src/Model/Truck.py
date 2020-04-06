class Truck(object):
    def __init__(self):
        self.package_load = 0
        self.capacity = 16      # Maximum amount of packages a truck can carry.
        self.average_speed = 18     # ...in miles per hour
        self.deliveries = []
        self.miles_travelled = 0

    def add_delivery(self, delivery):
        self.deliveries.append(delivery)
        if self.package_load == 16:
            self.reload_truck(delivery)
        self.package_load += 1

    def reload_truck(self, last_delivery):
        self.add_mileage(last_delivery.get_hub_distance())
        self.package_load = 0

    def get_package_load(self):
        return self.package_load

    def get_capacity(self):
        return self.capacity

    def add_mileage(self, mileage):
        self.miles_travelled += mileage

    def get_miles_travelled(self):
        return self.miles_travelled
