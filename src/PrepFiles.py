# Feng Parra ID: 001183862
import operator
from src.Objects.HashTable import Table
from src.Objects.Package import Package
import csv


def init_tables(distance_file_name, packages_file):
    distance_table = fill_distance_table(distance_file_name)
    package_table = fill_package_table(packages_file)
    return distance_table, package_table


def fill_package_table(packages_file):
    new_table = Table(100)
    lines = packages_file.readlines()
    for line in lines:
        package = Package(line.split(','))
        new_table.insert(package.get_id(), package)
    return new_table


def fill_distance_table(distance_file_name):
    with open(distance_file_name, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        distance_dict = dict()
        for row in reader:
            distance_dict.update({row['ORIGIN']: sort_row(row)})
        return distance_dict

# This method changes and then sorts the values of a given dictionary. The method first deletes the header
# as it strictly contains a string value. Values can then be changed to type float, and then the dictionary
# is turned into a list of tuples. This list is then numerically sorted in ascending order. Finally
# this list is turned back into a dictionary, and then returned.
def sort_row(row):
    distance_dict = dict()
    del row['ORIGIN']
    for key, value in row.items():
        row[key] = float(value)
    for item in sorted(row.items(), key=operator.itemgetter(1)):
        distance_dict.update({item[0]: item[1]})
    return distance_dict