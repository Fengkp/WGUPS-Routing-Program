# Combine lists to return based on special circumstances
# Use union combine? as to not get duplicates
# Use these lists to remove packages from ready_packages
# Deliver 1 at a time as we have it
def before_9(package_table):
    before_9 = get_delivery_list(['15'], package_table)
    before_10_30 = get_delivery_list(['1', '6', '13', '14', '16', '20', '25', '29', '30', '31', '34', '37', '40'],
                                     package_table)
    only_truck2 = get_delivery_list(['3', '18', '36', '38'], package_table)
    deliver_together = get_delivery_list(['15', '19', '13'], package_table)
    delayed = get_delivery_list(['6', '25', '28', '32'], package_table)
    wrong_address = get_delivery_list(['9'], package_table)


def get_delivery_list(special_packages, package_table):
    delivery_list = []
    for package in special_packages:
        delivery_list.append(package_table[package])
    return delivery_list