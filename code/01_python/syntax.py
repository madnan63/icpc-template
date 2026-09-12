from collections import defaultdict

# Binary string -> integer
x = int("101101", 2)

# Integer -> binary string with leading zeros
width = 8
s = format(x, f"0{width}b")

# Float formatting
value = 12.34567
print(f"{value:.2f}")

# Sort defaultdict by key
d = defaultdict(int, {3: 7, 1: 4, 2: 9})
d = defaultdict(d.default_factory, sorted(d.items()))

# Sort defaultdict by value
d = defaultdict(
    d.default_factory,
    sorted(d.items(), key=lambda item: item[1])
)
