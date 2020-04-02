class Truck(object):
    def __init__(self):
        self.capacity = 16      # Maximum amount of packages a truck can carry.
        self.average_speed = 18     # ...in miles per hour
        self.delivery_lists = []
        self.miles_travelled = 0

    def add_deliveries(self, deliveries):
        self.delivery_lists.append(deliveries)

    def get_capacity(self):
        return self.capacity

    def add_mileage(self, mileage):
        self.miles_travelled += mileage

    def get_miles_travelled(self):
        return self.miles_travelled