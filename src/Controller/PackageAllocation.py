# Algorithm to decide which packages go on which truck
# Return packages in lists?


# For now we'll just use the address.
# In the future, the first address to be noted will be the hub address.
# This address/distance will be referenced every time a truck runs out of packages.
def determine():
    from src.View.Interface import package_table
    package_list = prepare_packages(package_table)
    delivery_list = []
    current_package = package_list[str(1)]
    print(current_package.get_id())
    del package_list[current_package.get_id()]
    for item in current_package.get_distance_table().items():
        if package_list.__contains__(item[0]):
            pass


# def reorder_package_list(package_list):
#     packagelist


# Returns a list of packages that are ready to be shipped. Packages with a status of 'On route' or 'Delivered'
# will be excluded.
def prepare_packages(package_table):
    package_list = dict()
    for package in package_table.get_all():
        if package.get_status() == 'Preparing for shipment':
            package_list.update({package.get_id(): package})
    return package_list


# Compare the distances between two packages, and a distance to not be exceed. If the distance between the two
# packages is greater than a max_distance, then it'll return the distance in between the two packages, and 'True'
# to signify that the distance is too far. Otherwise the method will return the distance in between, along with
# 'False' to signify that the distance in between meets the preset criteria.
def compare_distance(package_1, package_2, max_distance):
    from src.View.Interface import distance_table
    distance_in_between = float(distance_table[package_1][package_2])
    if distance_in_between > 3.5:
        return distance_in_between, True
    return distance_in_between, False