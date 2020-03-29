from src.Model.HashTable import Table
from src.Model.Package import Package


def set_packages(packages_file):
    package_table = Table(100)
    lines = packages_file.readlines()
    row = [8]
    for line in lines:
        row = line.split(',')
        package = create_package(row)
        package_table.insert(package.get_id(), package)
    return package_table


def create_package(row):
    package = Package(row[0], row[1], row[2], row[4], row[5], row[6], row[7])
    return package


# **Handle exceptions
def new_package_prompt(package_count):
    print("\nEnter the following information, separated by a ','.")
    print("(Address, City, State, Zip Code, Deadline, Weight, Special Notes)")
    print("** Type 'None' if there are no special notes.")
    new_package = input("> ")
    new_package = str(package_count + 1) + ', ' + new_package
    return create_package(new_package.split(', '))


def find_package_prompt():
    print("\nEnter a package id.")
    return input("> ")


def interface():
    package_table = set_packages(open('../../files/packages.csv', 'r'))
    while True:
        print("Select an option using the number keys:")
        print("[1] Insert new package...")
        print("[2] Look up package...")
        print("[3] View all packages...")
        print("[4] Exit...")
        response = input("> ")
        if response == str(1):
            new_package = new_package_prompt(package_table.get_size())
            package_table.insert(new_package.get_id(), new_package)
            print("New package added.\n")
        elif response == str(2):
            print(package_table.get(find_package_prompt()))
        elif response == str(3):
            package_table.get_all()
        elif response == str(4):
            exit()
        else:
            print("Please submit a valid response.")


interface()