from random import getrandbits

MASK = (1 << 64) - 1
RANDOM = getrandbits(64)


def custom_hash(x):
    x = (x + RANDOM + 0x9e3779b97f4a7c15) & MASK
    x = ((x ^ (x >> 30)) * 0xbf58476d1ce4e5b9) & MASK
    x = ((x ^ (x >> 27)) * 0x94d049bb133111eb) & MASK
    return x ^ (x >> 31)
