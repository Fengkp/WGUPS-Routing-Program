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
        self.status = "Not Delivered."

    def get_id(self):
        return self.id

    def __str__(self):
        return f"""Package ID: {self.id}
    Current Status: {self.status}
    Delivery Address: {self.address}, {self.city}, {self.zip}
    Weight: {self.weight}
    Deliver By: {self.deadline}
    Special Notes: {self.notes}
    """
