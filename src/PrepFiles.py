# Feng Parra ID: 001183862
import operator
from src.Objects.HashTable import Table
from src.Objects.Package import Package
import csv


def init_tables(distance_file_name, packages_file):
    distance_table = fill_distance_table(distance_file_name)
    package_table = fill_package_table(packages_file)
    return distance_table, package_table

# Reads the packages.csv, and for each line creates a package object that is then added to our hash table.
# Time Complexity: O(n)
def fill_package_table(packages_file):
    new_table = Table(100)
    lines = packages_file.readlines()
    # Time Complexity: O(n)
    for line in lines:
        package = Package(line.split(','))
        new_table.insert(package.get_id(), package)
    return new_table

# Creates the weighted graph by reading the data from the csv file as a dictionary entry.
# Using dictionaries allows a weight to be found by simply using the the addresses of two packages
# and then getting the associated weight/distance between the two.
# Time Complexity: O(n) * O(n) = O(n^2)
def fill_distance_table(distance_file_name):
    with open(distance_file_name, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        distance_dict = dict()
        # Time Complexity: O(n)
        for row in reader:
            # Time Complexity: O(n) --> sort_row()
            distance_dict.update({row['ORIGIN']: sort_row(row)})
        return distance_dict

# This method changes and then sorts the values of a given dictionary. The method first deletes the header
# as it strictly contains a string value. Values can then be changed to type float, and then the dictionary
# is turned into a list of tuples. This list is then numerically sorted in ascending order. Finally
# this list is turned back into a dictionary, and then returned.
# Time Complexity: O(n) + O(n) = O(2n) = O(n)
def sort_row(row):
    distance_dict = dict()
    del row['ORIGIN']
    # Time Complexity: O(n)
    for key, value in row.items():
        row[key] = float(value)
    # Time Complexity: O(n)
    for item in sorted(row.items(), key=operator.itemgetter(1)):
        distance_dict.update({item[0]: item[1]})
    return distance_dict