from src.Controller.PackageAllocation import *
from src.Model.Truck import Truck
import datetime

class TruckManagement(object):

    def __init__(self, package_table, trucks):
        self.package_table = package_table
        self.trucks = trucks
        self.current_truck = trucks[0]
        self.current_time = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month,
                                              datetime.datetime.today().day, 8)
        self.priority_list = set_priority_packages(package_table)
        self.find_closest_to_hub(self.priority_list)
        self.regular_list = set_regular_packages(package_table)
        self.delayed_packages_arrived = False
        self.deliver_packages()

    def deliver_packages(self):
        update_delayed_packages(self.package_table)
        if len(self.priority_list) != 0:
            self.first_delivery(self.priority_list)
        else:
            self.first_delivery(self.regular_list)
        self.current_truck = self.trucks[0]
        while len(self.priority_list) != 0 or len(self.regular_list) != 0:
            if len(self.priority_list) != 0:
                self.deliver_list(self.priority_list)
            else:
                self.deliver_list(self.regular_list)
        print(self.total_distance())

    def deliver_list(self, delivery_list):
        while len(delivery_list) != 0:
            if self.current_time.time() >= datetime.time(9, 5) and self.delayed_packages_arrived is False:
                self.delayed_packages_arrived = True
                add_delayed_packages(self.priority_list, self.package_table)
                return
            if self.current_truck.get_package_count() == 16:
                self.go_home()
                package = self.find_closest_to_hub(delivery_list)
                if package.get_id() in ['3', '18', '36', '38']:
                    self.current_truck = self.trucks[1]
                self.deliver(package, package.get_hub_distance())
            else:
                package = self.current_truck.get_deliveries()[-1]
                package, distance = next_package(package, delivery_list)
                if package.get_id() in ['3', '18', '36', '38']:
                    self.current_truck = self.trucks[1]
                self.deliver(package, distance)
            update_delivery_list(package, delivery_list)
            self.switch_trucks()

    def first_delivery(self, delivery_list):
        for truck in self.trucks:
            self.current_truck = truck
            package = self.find_closest_to_hub(delivery_list)
            self.deliver(package, package.get_hub_distance())
            update_delivery_list(package, delivery_list)

    def find_closest_to_hub(self, delivery_list):
        cloest_to_hub = []
        for address in delivery_list.values():
            cloest_to_hub += list(address.values())
        cloest_to_hub.sort(key=lambda package: package.get_hub_distance())
        return cloest_to_hub[0]

    def switch_trucks(self):
        new_truck_index = self.trucks.index(self.current_truck) + 1
        if new_truck_index == len(self.trucks):
            new_truck_index = 0
        self.current_truck = self.trucks[new_truck_index]

    def deliver(self, package, distance):
        self.add_time(distance)
        update_package(package, 'Delivered', self.current_time, self.package_table)
        self.current_truck.add_delivery(package, distance)

    def add_time(self, miles):
        elapsed_seconds = 3600 / 18 * miles
        self.current_time = self.current_time + datetime.timedelta(seconds=elapsed_seconds)

    def total_distance(self):
        distance = 0
        for truck in self.trucks:
            self.current_truck = truck
            self.go_home()
            distance += self.current_truck.get_mileage()
        return distance

    def go_home(self):
        self.current_truck.add_mileage(self.current_truck.get_deliveries()[-1].get_hub_distance())
        self.current_truck.reset_package_count()