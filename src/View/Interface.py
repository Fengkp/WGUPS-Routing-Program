from src.Model.HashTable import Table
from src.Model.Package import Package


def set_packages(packages_file):
    new_table = Table(100)
    lines = packages_file.readlines()
    for line in lines:
        package = Package(line.split(','))
        new_table.insert(package.get_id(), package)
    return new_table


# **Handle exceptions
def new_package_prompt(package_count):
    print("\nEnter the following information, separated by a ','.")
    print("(Address, City, State, Zip Code, Deadline, Weight, Special Notes)")
    print("** Type 'None' if there are no special notes.")
    new_package = input("> ")
    new_package = str(package_count + 1) + ', ' + new_package
    return new_package.split(', ')


def find_package_prompt():
    print("\nEnter a package id.")
    return input("> ")


def package_interface():
    while True:
        print("Select an option using the number keys:")
        print("[1] Insert new package...")
        print("[2] Look up package...")
        print("[3] View all packages...")
        print("[4] Return...")
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
            main_interface()
        else:
            print("Please submit a valid response.")


def main_interface():
    while True:
        print("[1] Manage Packages...")
        print("[2] Start Deliveries...")
        print("[3] Exit...")
        response = input("> ")
        if response == str(1):
            package_interface()
        elif response == str(2):
            # Start TruckManagement
            pass
        elif response == str(3):
            exit()
        else:
            print("Please submit a valid response.")


package_table = set_packages(open('../../files/packages.csv', 'r'))
main_interface()