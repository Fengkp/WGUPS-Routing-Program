from src.Controller.PackageAllocation import *
from src.Model.Truck import Truck
import datetime

day = datetime.datetime.today().day
month = datetime.datetime.today().month
year = datetime.datetime.today().year
time_now = datetime.datetime(year, month, day, 8)

def deliver_packages(package_table, trucks):
    global time_now
    delivery_lists = prepare_list(package_table, time_now)
    first_delivery(trucks, delivery_lists[0], package_table)
    truck = trucks[0]
    index = 0
    while index < 2:
        deliver_list(delivery_lists[index], truck, trucks, package_table)
        if time_now.time() >= datetime.time(9, 5):
            delivery_lists[0] += delivery_lists[2]
            index = 0
        index += 1
    return total_distance(trucks)


def first_delivery(trucks, delivery_list, package_table):
    global time_now
    for truck in trucks:
        package = hub_package(delivery_list)
        deliver(truck, package, package.get_hub_distance(), package_table)
        update_delivery_list(package, delivery_list)


def deliver_list(delivery_list, truck, trucks, package_table):
    global time_now
    while len(delivery_list) != 0:
        if time_now.time() >= datetime.time(9, 5):
            return time_now
        if truck.get_package_count() == 16:
            go_home(truck)
            package = hub_package(delivery_list)
            if package.get_id() in ['3', '18', '36', '38']:
                truck = trucks[1]
            deliver(truck, package, package.get_hub_distance(), package_table)
        else:
            package = truck.get_deliveries()[-1]
            package, distance = next_package(package, delivery_list)
            if package.get_id() in ['3', '18', '36', '38']:
                truck = trucks[1]
            deliver(truck, package, distance, package_table)
        update_delivery_list(package, delivery_list)
        truck = switch_trucks(truck, trucks)


def deliver(truck, package, distance, package_table):
    global time_now
    add_time(distance)
    update_package(package_table, package, 'Delivered', time_now)
    truck.add_delivery(package, distance)


def add_time(miles):
    global time_now
    test = 3600 / 18 * miles
    time_now = time_now + datetime.timedelta(seconds=test)


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
    delayed_list = delayed_packages(package_table)
    priority_list = priority_packages(package_table, time_now)
    regular_list = regular_packages(package_table)
    return [priority_list, regular_list, delayed_list]


def delayed_packages(package_table):
    delayed_list = dict()
    for package_id in ['6', '25', '28', '32']:
        package = package_table.get(package_id)
        add_package(package, delayed_list, package_table)
    return delayed_list


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