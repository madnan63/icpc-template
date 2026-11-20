from random import getrandbits
from collections import defaultdict


class Hashed_dict:
    MASK = (1 << 64) - 1

    def __init__(self, factory):
        self.d = defaultdict(factory)
        self.RANDOM = getrandbits(64)

    def custom_hash(self, x):
        h = (x + self.RANDOM + 0x9e3779b97f4a7c15) & self.MASK
        h = ((h ^ (h >> 30)) * 0xbf58476d1ce4e5b9) & self.MASK
        h = ((h ^ (h >> 27)) * 0x94d049bb133111eb) & self.MASK
        return (h ^ (h >> 31), x)

    def __getitem__(self, key):
        return self.d[self.custom_hash(key)]

    def __setitem__(self, key, value):
        self.d[self.custom_hash(key)] = value

    def __contains__(self, key):
        return self.custom_hash(key) in self.d

    def __delitem__(self, key):
        del self.d[self.custom_hash(key)]

    def __len__(self):
        return len(self.d)

    def get(self, key, default=None):
        return self.d.get(self.custom_hash(key), default)

    def keys(self):
        return (k[1] for k in self.d)

    def values(self):
        return self.d.values()

    def items(self):
        return ((k[1], v) for k, v in self.d.items())

    def __iter__(self):
        return self.keys()
