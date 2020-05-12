# Feng Parra ID: 001183862
# Delivery algorithm presented within truck1_delivery.
import datetime

# Creates delivery list for truck 1 using various stipulations to ensure packages are delivered on time and correctly.
# The next package to be considered for delivery is determined using a greedy algorithm.
# The algorithm uses the last delivered package, and finds the lowest weight and its associated address.
# It checks if the package has already been delivered, if it isn't, it is added to the list, and the process repeats.
# As packages are being considered, the stipulations are handled manually through the use of several if statements.
# Truck 1 starts delivering at 8 AM, while truck 2 waits until the delayed packages arrive.
# The Truck 2 delivery list will be created within a separate function similar to this one.

# ------------------------------------------------  PSEUDO CODE
# function truck1_delivery(package table, distance table)
#   initialize unshipped packages by creating a new table based on package table, but is instead indexed by address
#   initialize truck list
#   initialize time using todays date
#   initialize current package with package 15, this will be the starting point and what determines the total mileage
#   add current package to truck list
#   initialize total weight using distance from HUB to package 15
#   set time based on distance from origin point, in this case the origin point is HUB
#   set current package status
#   initialize package count to 1, this will determine when the truck has to return to HUB
#   iterate through unshipped packages n times until there are none left
#       iterate through distance table n times until closest address from current package is found in unshipped packages
#           if package is excluded from delivery
#               set package to current package
#           else if current package is package 12
#               change current package to package 13 to assure that package 13 restrictions are met
#               add distance from current package address to package 13 address, to total weight
#               set time based on package 13 distance and not 12
#           else if package count is 0
#               add distance from HUB to current package, to total weight
#               set time based on distance from HUB
#           else
#               add distance from current package address to new address, to total weight
#               set time based on current package distance to new address
#           if package package count is 16
#               add distance from current package address to HUB, to total weight
#               set time based on distance from HUB
#               set package count to 0
#           if time is greater than or equal to 9:05 am
#               create truck 2 list with excluded packages
#           add current package to delivery list
#   reroute package 9 by:
#   add distance from last delivered package address to current package 9 address, to total weight
#   add distance from last delivered package address to new package 9 address, to total weight
#   set time based on total distance travelled to reroute package 9
#   return total weight with addition of distance back to HUB from new package 9 address and truck 2 list weight
# ------------------------------------------------  END

# Time Complexity: O(n^2) + O(n) + O(n^3) = O(n^3)
def truck1_delivery(pack_table, dis_table):
    # Initialize the variables to be used throughout the algorithm.
    global package_table, distance_table, unshipped_packages, package_count, truck2_packages
    package_table = pack_table
    distance_table = dis_table
    # Time Complexity: O(n^2) --> package_table.get_all()
    # Time Complexity: O(n) --> get_packages()
    unshipped_packages = get_packages(package_table.get_all())
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
    # Time Complexity: O(1) -- add_time()
    current_time = add_time(current_time, total_weight)
    # Adds the current package being delivered to the current truck. In this case, truck 1.
    # Time Complexity: O(1) --> add_delivery()
    add_delivery(current_package, truck1_list, current_time)
    # package_count keeps tracks of when  the truck has to go back to the HUB to reload.
    package_count = 1

    # The trucks will continue to be loaded until there are no packages left to deliver.
    # Every time a package is added to a list, it is removed from the unshipped_packages.
    # Time Complexity: O(n) * O(n^2) + O(n^2) = O(n^3)
    while len(unshipped_packages) > 0:
        # Takes the last delivered package, and finds the lowest weight and its associated address.
        # Time Complexity: O(n)
        for address, weight in distance_table[current_package.get_address_key()].items():
            # Checks if a non-delivered package matches the current closest address.
            # If not, we move on to the next weight lowest weight and the address associated with it.
            if unshipped_packages.get(address):
                # Packages can have the same address, so we navigate through the table to find the first available.
                # Time Complexity: O(n)
                for package_id, package in unshipped_packages[address].items():
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
                        # Time Complexity: O(1) -- add_time()
                        current_time = add_time(current_time, new_weight)
                        # same_truck_packages makes sure that package 12 is only exchanged once.
                        same_truck_packages = True
                    # Currently at the HUB if package_count is 0, add weight based on the HUB and the current address.
                    elif package_count == 0:
                        total_weight += distance_table[current_package.get_address_key()]['HUB']
                        # Time Complexity: O(1) -- add_time()
                        current_time = add_time(current_time, distance_table[current_package.get_address_key()]['HUB'])
                    # Add weight as normal since the current load has not finished being delivered.
                    else:
                        total_weight += weight
                        # Time Complexity: O(1) -- add_time()
                        current_time = add_time(current_time, weight)
                    # Once 16 packages have been delivered, add the weight to get back to the HUB and reset the count.
                    if package_count == 16:
                        total_weight += distance_table[current_package.get_address_key()]['HUB']
                        package_count = 0
                        # Time Complexity: O(1) -- add_time()
                        current_time = add_time(current_time, distance_table[current_package.get_address_key()]['HUB'])
                    # Start the deliveries for truck 2 at 9:05.
                    if current_time.time() >= datetime.time(9, 5) and truck2_packages_delivered is False:
                        # Time Complexity: O(n^2) --> truck2_delivery()
                        total_weight2, truck2_list = truck2_delivery(current_time)
                        # Make sure truck 2 only goes out once.
                        truck2_packages_delivered = True
                    # Time Complexity: O(1) --> add_delivery()
                    add_delivery(current_package, truck1_list, current_time)
                    # Reset to find eligble packages.
                    package_eligible = False
                    break

    # Reroute package 9 manually since it has no special conditions other than an incorrect address
    current_package = package_table.get('9')
    # Weight/distance it takes to pick up the package from the incorrect address, then to the correct address.
    reroute_weight = distance_table[truck1_list[-1].get_address_key()][current_package.get_address_key()] + \
                     distance_table[current_package.get_address_key()]["410 S State St,84111"]
    # Time Complexity: O(1) -- add_time()
    current_time = add_time(current_time, reroute_weight)
    # Update the new package information accordingly.
    current_package.set_address("410 S State St")
    current_package.set_zip("84111")
    current_package.set_time_delivered(current_time)
    print("All packages delivered on time. See all packages status.")
    # Add truck 1 total, truck 2 total, the distance for truck 1 to get back to the HUB, and the detour weight for 9.
    return total_weight + distance_table["410 S State St,84111"]['HUB'] + reroute_weight, total_weight2

# Essentially the same as truck1_delivery, with less stipulations as truck 2 only loads once.
# Time Complexity: O(n^2)
def truck2_delivery(current_time):
    delivery_list = list()
    package_eligible = False
    # Manually start with package 25 as it yields the lowest mileage using our greedy algorithm.
    current_package = package_table.get('25')
    total_weight = distance_table[current_package.get_address_key()]['HUB']
    # Time Complexity: O(1) -- add_time()
    current_time = add_time(current_time, total_weight)
    # Time Complexity: O(1) --> add_delivery()
    add_delivery(current_package, delivery_list, current_time)
    # 9 is just the amount of special packages, i.e. truck2_packages
    # Time Complexity: O(1) * O(n^2) = O(n^2)
    while len(delivery_list) < 9:
        # Time Complexity: O(n)
        for address, weight in distance_table[current_package.get_address_key()].items():
            if unshipped_packages.get(address):
                # Time Complexity: O(n)
                for package_id, package in unshipped_packages[address].items():
                    if package_id in truck2_packages:
                        current_package = package
                        package_eligible = True
                        break
                if package_eligible:
                    total_weight += weight
                    # Time Complexity: O(1) -- add_time()
                    current_time = add_time(current_time, weight)
                    # Time Complexity: O(1) --> add_delivery()
                    add_delivery(current_package, delivery_list, current_time)
                    package_eligible = False
                    break
    return total_weight + distance_table[delivery_list[-1].get_address_key()]['HUB'], delivery_list

# Removes the package availability, adds the package to the current truck list, and updates said package.
# Time Complexity: O(1)
def add_delivery(package, delivery_list, current_time):
    # Time Complexity: O(1) --> update_list()
    update_list(package)
    package_table.get(package.get_id()).set_status('Delivered')
    package_table.get(package.get_id()).set_time_delivered(current_time)
    delivery_list.append(package)

# Removes package from being available.
# Time Complexity: O(1)
def update_list(package):
    if len(unshipped_packages[package.get_address_key()]) > 1:
        package_list = unshipped_packages[package.get_address_key()]
        del package_list[package.get_id()]
    else:
        del unshipped_packages[package.get_address_key()]

# Adjusts the time given based on miles travelled.
# Time Complexity: O(1)
def add_time(current_time, miles):
    # 18 is the average speed of the trucks.
    elapsed_seconds = 3600 / 18 * miles
    current_time = current_time + datetime.timedelta(seconds=elapsed_seconds)
    return current_time

# Creates a new package table filled with packages available to be delivered.
# Since the original hash table containing our packages is keyed by package ID, and the weight table is keyed by
# address, then it makes it difficult to locate the next package. Creating a new table with the address as a key makes
# it easier to check a package and subsequently, add it to our delivery list.
# Time Complexity: O(n)
def get_packages(package_list):
    address_table = dict()
    # Time Complexity: O(n)
    for package in package_list:
        # Because there are multiple packages with the same address, we need to make sure they don't collide.
        if address_table.get(package.get_address_key()):
            address_table[package.get_address_key()].update({package.get_id(): package})
        else:
            address_table.update({package.get_address_key(): {package.get_id(): package}})
    return address_table


# Globalized variables frequently used by our functions to reduce extra parameters.
package_table = None
distance_table = None
unshipped_packages = None
package_count = 0
# Packages that are delayed and have strict conditions will be delivered on truck 2 starting at 9:05.
truck2_packages = ['6', '25', '28', '32', '31', '3', '18', '36', '38']