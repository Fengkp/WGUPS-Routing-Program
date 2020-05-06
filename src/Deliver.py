# Feng Parra ID: 001183862
# Delivery algorithm presented within truck1_delivery.
import datetime

# Creates delivery lists for truck 1 and 2.
# Truck 1 starts delivering at 8 AM, while truck 2 waits until the delayed packages arrive.
def truck1_delivery(table, table2):
    # Initialize the variables to be used throughout the algorithm.
    global package_table, distance_table, available_packages, package_count, truck2_packages
    package_table = table
    distance_table = table2
    available_packages = get_packages(package_table.get_all())
    truck1_list = list()
    # This time is associated with this function, as the delivery times will be different between truck 1 and truck 2.
    current_time = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month,
                                     datetime.datetime.today().day, 8)
    # A check to begin truck 2 deliveries only once.
    truck2_packages_delivered = False
    # A check to see if a package can only be delivered by truck 2.
    package_eligible = False
    # A check to make sure that certain packages are loaded on the same truck during a delivery trip.
    same_truck_packages = False

    # We need a starting package. We use '15' because it's the package with the earliest delivery deadline.
    current_package = package_table.get('15')
    # total_weight keeps track of the overall distance travelled as packages are delivered.
    total_weight = distance_table[current_package.get_address_key()]['HUB']
    # Updates the current time.
    current_time = add_time(current_time, total_weight)
    # Adds the current package being delivered to the current truck. In this case, truck 1.
    add_delivery(current_package, truck1_list, current_time)
    # package_count keeps tracks of when  the truck has to go back to the HUB to reload.
    package_count = 1

    # The trucks will continue to be loaded until there are no packages left to deliver.
    # Every time a package is added to a list, it is removed from the available_packages.
    while len(available_packages) > 0:
        # Takes the last delivered package, and finds the lowest weight and its associated address.
        for address, weight in distance_table[current_package.get_address_key()].items():
            # Checks if a non-delivered package matches the current closest address.
            # If not, we move on to the next weight lowest weight and the address associated with it.
            if available_packages.get(address):
                # Packages can have the same address, so we navigate through the table to find the first available.
                for package_id, package in available_packages[address].items():
                    # Sets the current package as eligible to be delivered next.
                    if package_id not in truck2_packages:
                        current_package = package
                        package_eligible = True
                        break
                # Delivers the current package, update the time, and adjust weight based on package count conditions.
                if package_eligible:
                    # Package 13 has to be delivered on the same load as several other packages.
                    # But using a greedy algorithm always delivers this package on the next load.
                    # We force the delivery of 13 here when package 12 is to be delivered, by exchanging the two.
                    if current_package.get_id() == '12' and same_truck_packages is False:
                        current_package = package_table.get('13')
                        # Add the correct weight to the total, and adjust the time accordingly.
                        new_weight = distance_table[truck1_list[-1].get_address_key()][current_package.get_address_key()]
                        total_weight += new_weight
                        current_time = add_time(current_time, new_weight)
                        # same_truck_packages makes sure that package 12 is only exchanged once.
                        same_truck_packages = True
                    # Currently at the HUB if package_count is 0, add weight based on the HUB and the current address.
                    elif package_count == 0:
                        total_weight += distance_table[current_package.get_address_key()]['HUB']
                        current_time = add_time(current_time, distance_table[current_package.get_address_key()]['HUB'])
                    # Add weight as normal since the current load has not finished being delivered.
                    else:
                        total_weight += weight
                        current_time = add_time(current_time, weight)
                    # Once 16 packages have been delivered, add the weight to get back to the HUB and reset the count.
                    if package_count == 16:
                        total_weight += distance_table[current_package.get_address_key()]['HUB']
                        package_count = 0
                        current_time = add_time(current_time, distance_table[current_package.get_address_key()]['HUB'])
                    # Start the deliveries for truck 2 at 9:05.
                    if current_time.time() >= datetime.time(9, 5) and truck2_packages_delivered is False:
                        total_weight2, truck2_list = truck2_delivery(current_time)
                        # Make sure truck 2 only goes out once.
                        truck2_packages_delivered = True
                    add_delivery(current_package, truck1_list, current_time)
                    # Reset to find eligble packages.
                    package_eligible = False
                    break

    # Reroute package 9 manually since it has no special conditions other than an incorrect address
    current_package = package_table.get('9')
    # Weight/distance it takes to pick up the package from the incorrect address, then to the correct address.
    reroute_weight = distance_table[truck1_list[-1].get_address_key()][current_package.get_address_key()] + \
                     distance_table[current_package.get_address_key()]["410 S State St,84111"]
    current_time = add_time(current_time, reroute_weight)
    # Update the new package information accordingly.
    current_package.set_address("410 S State St")
    current_package.set_zip("84111")
    current_package.set_time_delivered(current_time)
    # Add truck 1 total, truck 2 total, the distance for truck 1 to get back to the HUB, and the detour weight for 9.
    return total_weight + total_weight2 + distance_table["410 S State St,84111"]['HUB'] + reroute_weight

# Essentially the same as truck1_delivery, with less stipulations as truck 2 only loads once.
def truck2_delivery(current_time):
    delivery_list = list()
    package_eligible = False
    # Manually start with package 25 as it yields the lowest mileage using our greedy algorithm.
    current_package = package_table.get('25')
    total_weight = distance_table[current_package.get_address_key()]['HUB']
    current_time = add_time(current_time, total_weight)
    add_delivery(current_package, delivery_list, current_time)
    while len(delivery_list) < 9:
        for address, weight in distance_table[current_package.get_address_key()].items():
            if available_packages.get(address):
                for package_id, package in available_packages[address].items():
                    if package_id in truck2_packages:
                        current_package = package
                        package_eligible = True
                        break
                if package_eligible:
                    total_weight += weight
                    current_time = add_time(current_time, weight)
                    add_delivery(current_package, delivery_list, current_time)
                    package_eligible = False
                    break
    return total_weight + distance_table[delivery_list[-1].get_address_key()]['HUB'], delivery_list

# Removes the package availability, adds the package to the current truck list, and updates said package.
def add_delivery(package, delivery_list, current_time):
    update_list(package)
    package_table.get(package.get_id()).set_status('Delivered')
    package_table.get(package.get_id()).set_time_delivered(current_time)
    delivery_list.append(package)

# Removes package from being available.
def update_list(package):
    if len(available_packages[package.get_address_key()]) > 1:
        package_list = available_packages[package.get_address_key()]
        del package_list[package.get_id()]
    else:
        del available_packages[package.get_address_key()]

# Adjusts the time given based on miles travelled.
def add_time(current_time, miles):
    elapsed_seconds = 3600 / 18 * miles
    current_time = current_time + datetime.timedelta(seconds=elapsed_seconds)
    return current_time

# Creates a package table filled with packages available to be delivered.
def get_packages(package_list):
    address_table = dict()
    for package in package_list:
        if address_table.get(package.get_address_key()):
            address_table[package.get_address_key()].update({package.get_id(): package})
        else:
            address_table.update({package.get_address_key(): {package.get_id(): package}})
    return address_table


# Globalized variables frequently used by our functions to reduce extra parameters.
package_table = None
distance_table = None
available_packages = None
package_count = 0
# Packages that are delayed and have strict conditions will be delivered on truck 2 starting at 9:05.
truck2_packages = ['6', '25', '28', '32', '31', '3', '18', '36', '38']