class Package(object):
    def __init__(self, id, address, city, zip, deadline, weight, notes):
        self.id = id
        self.address = address
        self.city = city
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        if notes == "\n":
            self.notes = "N/A"
        else:
            self.notes = notes
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
