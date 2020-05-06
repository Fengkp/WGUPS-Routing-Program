# Feng Parra ID: 001183862
class Package(object):

    def __init__(self, new_package):
        self.id = new_package[0]
        self.address = new_package[1]
        self.city = new_package[2]
        self.zip = new_package[4]
        self.deadline = new_package[5]
        self.weight = new_package[6]
        if new_package[7] == "\n":
            self.notes = "N/A"
        else:
            self.notes = new_package[7]
        self.status = 'Preparing for shipment'
        self.time_delivered = None

    def get_address_key(self):
        return self.address + ',' + self.zip

    def set_address(self, address):
        self.address = address

    def get_id(self):
        return self.id

    def get_address(self):
        return self.address

    def get_zip(self):
        return self.zip

    def set_zip(self, zip):
        self.zip = zip

    def get_status(self):
        return self.status

    def set_status(self, new_status):
        self.status = new_status

    def set_time_delivered(self, time):
        self.time_delivered = time

    def get_notes(self):
        return self.notes

    def __str__(self):
        package_info = f"""Package ID: {self.id}
    Current Status: {self.status}
    Delivery Address: {self.address}, {self.city}, {self.zip}
    Weight: {self.weight}
    Deliver By: {self.deadline}
    Special Notes: {self.notes}
    """
        if self.status == 'Delivered':
            package_info += "Delivered at: " + str(self.time_delivered) + '\n'
        return package_info
