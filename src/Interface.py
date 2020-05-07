# Feng Parra ID: 001183862
import datetime

from src.PrepFiles import *


# **Handle exceptions
from src.Deliver import truck1_delivery


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


def main():
    global package_table
    while True:
        print("Select an option using the number keys:")
        print("[1] Insert new package...")
        print("[2] Look up package...")
        print("[3] View all packages...")
        print("[4] Look up time...")
        print("[5] Exit...")
        response = input("> ")
        if response == str(1):
            new_package = new_package_prompt(package_table.get_size())
            package_table.insert(new_package.get_id(), new_package)
            print("New package added.\n")
        elif response == str(2):
            print(package_table.get(find_package_prompt()))
        elif response == str(3):
            for package in package_table.get_all():
                print(package)
            print()
        elif response == str(4):
            packages_found = False
            time_frame = []
            print("\n**enter numbers in 24 hour format (1 PM is 13)")
            for i in range(1, 3):
                hour = input(f"Enter hour {i}: ")
                minute = input(f"Enter minute {i}: ")
                print()
                time_frame.append(datetime.time(int(hour), int(minute)))
            for package in package_table.get_all():
                package_time = package.get_time_delivered().time()
                if time_frame[0] <= package_time <= time_frame[1]:
                    packages_found = True
                    print(package)
            if packages_found is False:
                print("No packages delivered within this time frame.")
            print()
        elif response == str(5):
            exit()
        else:
            print("Please submit a valid response.")


distance_table, package_table = init_tables('../files/distance_table.csv',
                                            open('../files/packages.csv', 'r'))
truck1_delivery(package_table, distance_table)
if __name__ == '__main__':
    main()