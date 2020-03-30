from src.Model.HashTable import Table
import csv
# Algorithm to decide which packages go on which truck
# Return packages in lists?


# For now we'll just use the address.
# In the future, the first address to be noted will be the hub address.
# This address/distance will be referenced every time a truck runs out of packages.
def determine(package_table):
    global distance_dict
    package_list = package_table.get_all()
    delivery_miles = 0.0
    delivery_list = []
    for package in package_list:
        delivery_list.append(package)
    print(len(delivery_list))
    for package in range(0, 15):
        package_1_address = delivery_list[package].get_address() + ',' + delivery_list[package].get_zip()
        package_2_address = delivery_list[package + 1].get_address() + ',' + delivery_list[package + 1].get_zip()
        delivery_miles += compare_distance(package_1_address, package_2_address)
    print(delivery_miles)


def compare_distance(package_1, package_2):
    global distance_dict
    print(float(distance_dict[package_1][package_2]))
    return float(distance_dict[package_1][package_2])


def fill_address_dict():
    with open('../../files/distance_table.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        origin_dict = dict()
        for row in reader:
            origin_dict.update({row['ORIGIN']: row})
        return origin_dict


distance_dict = fill_address_dict()