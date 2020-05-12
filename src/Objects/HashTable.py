# Feng Parra ID: 001183862
class Table:
    # Initialize an empty list to serve as our map. Then fill the empty list with several lists, or "buckets".
    # Time Complexity: O(n)
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = []
        # Time Complexity: O(n)
        for i in range(capacity):       # Initializing the map with empty lists/buckets.
            self.table.append([])

    # This method will create and return a unique hash key based off of given key. This will determine the position
    # in our table where the value will be contained.
    # Time Complexity: O(1)
    def get_hash(self, key):
        # Turn given key into a hash key, in attempt to get a unique position.
        hash_key = hash(key) % self.capacity
        return hash_key

    # This method will determine a bucket to place our value in, using a unique hash key. The value will then be
    # inserted into the bucket corresponding to the hash key.
    # Time Complexity: O(1)
    def insert(self, key, value):
        bucket = self.get_hash(key)
        self.table[bucket].append([key, value])
        self.size += 1

    # Time Complexity: O(n)
    def get(self, key):
        bucket = self.get_hash(key)
        if self.table[bucket] is not None:
            bucket_list = self.table[bucket]
            # Time Complexity: O(n)
            for index, value in bucket_list:
                if index == key:
                    return value
        else:
            print("Not found.")
            return None

    # Time Complexity: O(n^2)
    def get_all(self):
        package_list = []
        # Time Complexity: O(n)
        for bucket in self.table:
            # Time Complexity: O(n)
            for item in bucket:
                package_list.append(item[1])
        return package_list

    # Time Complexity: O(1)
    def get_size(self):
        return self.size