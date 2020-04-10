import datetime
# Algorithm to decide which packages go on which truck
# Return packages in lists?
# For now we'll just use the address.
# In the future, the first address to be noted will be the hub address.
# This address/distance will be referenced every time a truck runs out of packages.

def next_package(current_package, ready_packages):
    # Get distance table for the current package.
    potential_packages = current_package.get_distance_table().items()
    # Go through the current package distance table and see if any of those packages are
    # ready to ship; starting with the closest.
    for potential_package in potential_packages:
        # Both the packages ready to ship and distance tables are indexed by address.
        # If the distance table package exists in the ready to ship table, get ready to assign.
        if ready_packages.get(potential_package[0]):
            # Ready packages are stored in arrays because a package can have the same address.
            # This picks the first package at that address.
            first_package_key = next(iter(ready_packages[potential_package[0]]))
            current_package = ready_packages[potential_package[0]][first_package_key]
            # We return the next destination to start from, and the distance from the previous package
            # to this new one.
            return current_package, potential_package[1]


def add_package(package, package_list):
    if package.get_status() == 'Preparing for shipment':
        update_package(package, 'On route', datetime.time(0))
        if package_list.get(package.get_address_key()):
            package_list[package.get_address_key()].update({package.get_id(): package})
        else:
            package_list.update({package.get_address_key(): {package.get_id(): package}})


def add_delayed_packages(delivery_list, package_table):
    for package_id in ['6', '25', '28', '32']:
        package = package_table.get(package_id)
        add_package(package, delivery_list)
    return delivery_list


def set_priority_packages(package_table):
    time_crunch_list = time_crunch_packages()
    priority_list = dict()
    for package_id in time_crunch_list:
        package = package_table.get(package_id)
        add_package(package, priority_list)
    return priority_list


def set_regular_packages(package_table):
    regular_list = dict()
    for package in package_table.get_all():
        add_package(package, regular_list)
    return regular_list


def update_package(current_package, new_status, new_time, package_table):
    package_table.get(current_package.get_id()).set_status(new_status)
    package_table.get(current_package.get_id()).set_time_delivered(new_time)


def update_delivery_list(package, delivery_list):
    if len(delivery_list[package.get_address_key()]) > 1:
        package_list = delivery_list[package.get_address_key()]
        del package_list[package.get_id()]
    else:
        del delivery_list[package.get_address_key()]


def time_crunch_packages():
    time_crunch_list = set()
    before_9 = ['15']
    before_10_30 = ['1', '6', '13', '14', '16', '20', '25', '29', '30', '31', '34', '37', '40']
    deliver_together = ['15', '19', '13']
    delayed = ['6', '25', '28', '32']

    for package_id in before_9 + before_10_30:
        time_crunch_list.add(package_id)
    time_crunch_list.union(deliver_together)
    time_crunch_list.difference(delayed)
    return time_crunch_list
