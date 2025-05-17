from hashlib import sha256
from math import log, ceil
from bitarray import bitarray
import time

class BloomFilter:
    def __init__(self, expected_items, false_positive_rate=0.01, rotation_interval=300):
        self.size = self._get_size(expected_items, false_positive_rate)
        self.hash_count = self._get_hash_count(self.size, expected_items)
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)
        self.rotation_interval = rotation_interval
        self.last_rotation_time = time.time()

    def _get_size(self, n, p):
        return ceil(-(n * log(p)) / (log(2) ** 2))

    def _get_hash_count(self, m, n):
        return ceil((m / n) * log(2))

    def _get_hashes(self, item):
        hashes = []
        item = item.encode('utf-8')
        for i in range(self.hash_count):
            digest = sha256(item + str(i).encode('utf-8')).hexdigest()
            hash_val = int(digest, 16) % self.size
            hashes.append(hash_val)
        return hashes

    def add(self, item):
        if self.should_rotate():
            self.rotate()
        for hash_val in self._get_hashes(item):
            self.bit_array[hash_val] = 1

    def __contains__(self, item):
        if self.should_rotate():
            self.rotate()
        return all(self.bit_array[hash_val] for hash_val in self._get_hashes(item))

    def should_rotate(self):
        return (time.time() - self.last_rotation_time) > self.rotation_interval

    def rotate(self):
        self.bit_array.setall(0)
        self.last_rotation_time = time.time()
