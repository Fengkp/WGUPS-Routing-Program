from src.Controller.PackageAllocation import *
from src.Model.Truck import Truck
import datetime


def deliver_packages(package_table, trucks):
    day = datetime.datetime.today().day
    month = datetime.datetime.today().month
    year = datetime.datetime.today().year
    time_now = datetime.datetime(year, month, day, 8)
    delivery_lists = prepare_list(package_table, time_now)
    first_delivery(trucks, delivery_lists[0], time_now, package_table)
    truck = trucks[0]
    for delivery_list in delivery_lists:
        deliver_list(delivery_list, truck, trucks, time_now, package_table)
    return total_distance(trucks)


def first_delivery(trucks, delivery_list, time_now, package_table):
    for truck in trucks:
        package = hub_package(delivery_list)
        deliver(truck, package, package.get_hub_distance(), time_now, package_table)
        update_delivery_list(package, delivery_list)


def deliver_list(delivery_list, truck, trucks, time_now, package_table):
    while len(delivery_list) != 0:
        if truck.get_package_count() == 16:
            go_home(truck)
            package = hub_package(delivery_list)
            deliver(truck, package, package.get_hub_distance(), time_now, package_table)
        else:
            package = truck.get_deliveries()[-1]
            package, distance = next_package(package, delivery_list)
            deliver(truck, package, package.get_hub_distance(), time_now, package_table)
        update_delivery_list(package, delivery_list)
        truck = switch_trucks(truck, trucks)


def deliver(truck, package, distance, time_now, package_table):
    time_delivered = add_time(distance, time_now)
    update_package(package_table, package, 'Delivered', time_delivered)
    truck.add_delivery(package, distance)


def add_time(miles, time_now):
    test = 3600 / 18 * miles
    time_now = time_now + datetime.timedelta(seconds=test)
    return time_now


def total_distance(trucks):
    distance = 0
    for truck in trucks:
        go_home(truck)
        distance += truck.get_mileage()
    return distance


def go_home(truck):
    truck.add_mileage(truck.get_deliveries()[-1].get_hub_distance())
    truck.reset_package_count()


def hub_package(delivery_list):
    package_list = delivery_list[next(iter(delivery_list))]
    package = package_list[next(iter(package_list))]
    return package


def update_delivery_list(package, delivery_list):
    if len(delivery_list[package.get_address_key()]) > 1:
        package_list = delivery_list[package.get_address_key()]
        del package_list[package.get_id()]
    else:
        del delivery_list[package.get_address_key()]


def switch_trucks(truck, trucks):
    new_truck_index = trucks.index(truck) + 1
    if new_truck_index == len(trucks):
        new_truck_index = 0
    return trucks[new_truck_index]


def update_package(package_table, current_package, new_status, time_now):
    package_table.get(current_package.get_id()).set_status(new_status)
    package_table.get(current_package.get_id()).set_time_delivered(time_now)


def prepare_list(package_table, time_now):
    priority_list = priority_packages(package_table, time_now)
    regular_list = regular_packages(package_table)
    return [priority_list, regular_list]


def priority_packages(package_table, time):
    time_crunch_list = time_crunch_packages(time)
    priority_list = dict()
    for package_id in time_crunch_list:
        package = package_table.get(package_id)
        add_package(package, priority_list, package_table)
    return priority_list


def time_crunch_packages(time_now):
    before_9 = ['15']
    before_10_30 = ['1', '6', '13', '14', '16', '20', '25', '29', '30', '31', '34', '37', '40']
    deliver_together = ['15', '19', '13']
    delayed = ['6', '25', '28', '32']
    if time_now.time() < datetime.time(9):
        time_crunch_list = set(before_9 + before_10_30)
        time_crunch_list.union(set(deliver_together))
    if time_now.time() < datetime.time(9, 5):
        for package_id in delayed:
            if time_crunch_list.__contains__(package_id):
                time_crunch_list.remove(package_id)
    return time_crunch_list


def regular_packages(package_table):
    regular_list = dict()
    for package in package_table.get_all():
         add_package(package, regular_list, package_table)
    return regular_list


def add_package(package, package_list, package_table):
    if package.get_status() == 'Preparing for shipment':
        update_package(package_table, package, 'On route', datetime.time(0))
        if package_list.get(package.get_address_key()):
            package_list[package.get_address_key()].update({package.get_id(): package})
        else:
            package_list.update({package.get_address_key(): {package.get_id(): package}})