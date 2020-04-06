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
