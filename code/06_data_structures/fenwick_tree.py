
# ==================================================
# FENWICK TREE / BINARY INDEXED TREE
# ==================================================
#
# Indexing: 1-based
# Build: O(N)
# Update / Query: O(log N)
# Space: O(N)
#
# SUPPORTED OPERATIONS:
#
# build(values)         -> Build BIT from an array
# update(i, val)        -> Add val at index i
# query(i)              -> Prefix sum [1, i]
# range_query(l, r)     -> Range sum [l, r]
# set_value(i, val)     -> Replace value at index i
# kth(k)                -> First index with prefix sum >= k
#
# IMPORTANT:
# - Valid indices are 1 to N.
# - update() ADDS, it does not replace.
# - Never call update(0, val).
# - kth() requires non-negative stored values.
# - kth() returns -1 if k is invalid.


N = 200005

bit = [0] * (N + 1)
arr = [0] * (N + 1)


# --------------------------------------------------
# BUILD FENWICK TREE - O(N)
# --------------------------------------------------
# Builds BIT from a normal 0-indexed Python list.
# Internally, BIT uses 1-based indexing.
#
# Example:
# values = [2, 4, 1, 5, 3]
# build(values)
#
# Completely resets the previous BIT.
# Do NOT call update() again for the same
# initial values, or they will be added twice.

def build(values):
    n = len(values)

    if n > N:
        raise ValueError("Array exceeds BIT capacity")

    bit[:] = [0] * (N + 1)
    arr[:] = [0] * (N + 1)

    for i, x in enumerate(values, 1):
        arr[i] = x
        bit[i] = x

    # Propagate sums to parent BIT indices.
    # Process all N positions, including zero padding.
    for i in range(1, N + 1):
        j = i + (i & -i)

        if j <= N:
            bit[j] += bit[i]


# --------------------------------------------------
# POINT UPDATE - O(log N)
# --------------------------------------------------
# Adds val to index i (does NOT replace).
#
# update(3, 5)  -> Add 5 at index 3
# update(3, -2) -> Subtract 2 from index 3
#
# When storing frequencies:
# update(x, 1)  -> Insert one occurrence of x
# update(x, -1) -> Delete one occurrence of x
#
# Valid index: 1 <= i <= N

def update(i, val):
    arr[i] += val

    while i <= N:
        bit[i] += val
        i += i & -i


# --------------------------------------------------
# PREFIX QUERY - O(log N)
# --------------------------------------------------
# Returns sum of indices [1, i].
#
# Normal array:
# query(4) -> arr[1] + arr[2] + arr[3] + arr[4]
#
# Frequency array:
# query(5) -> Count of numbers <= 5

def query(i):
    ans = 0

    while i > 0:
        ans += bit[i]
        i -= i & -i

    return ans


# --------------------------------------------------
# RANGE QUERY - O(log N)
# --------------------------------------------------
# Returns sum of indices [l, r] (inclusive).
#
# Normal array:
# range_query(2, 5) -> Sum of positions 2 to 5
#
# Frequency array:
# range_query(2, 5) -> Count values in [2, 5]

def range_query(l, r):
    return query(r) - query(l - 1)


# --------------------------------------------------
# POINT ASSIGNMENT - O(log N)
# --------------------------------------------------
# Replaces arr[i] with val.
#
# Example:
# If arr[3] = 5:
# set_value(3, 10) -> arr[3] becomes 10
#
# Uses the difference between new and old values.
# Do not modify arr[] directly after building BIT.

def set_value(i, val):
    update(i, val - arr[i])


# --------------------------------------------------
# K-TH ELEMENT / PREFIX LOWER BOUND - O(log N)
# --------------------------------------------------
# Returns the smallest index i where query(i) >= k.
#
# Uses binary lifting on the Fenwick Tree.
#
# USE CASE 1: K-th smallest number
# Store the frequency of each number.
# kth(k) returns the k-th smallest value.
#
# USE CASE 2: K-th remaining element
# Store 1 for active positions, 0 for removed.
# kth(k) returns the k-th remaining position.
#
# REQUIREMENTS:
# - All stored values must be non-negative.
# - k must be between 1 and total frequency.
# - Returns -1 if k is invalid.

def kth(k):
    if k <= 0 or k > query(N):
        return -1

    i = 0
    step = 1 << (N.bit_length() - 1)

    while step:
        nxt = i + step

        if nxt <= N and bit[nxt] < k:
            k -= bit[nxt]
            i = nxt

        step >>= 1

    return i + 1


# ==================================================
# CUSTOMIZATION: SUM -> XOR
# ==================================================
#
# To customize this template for RANGE XOR:
#
# 1. Inside build():
#    bit[j] += bit[i]   -> bit[j] ^= bit[i]
#
# 2. Inside update():
#    arr[i] += val      -> arr[i] ^= val
#    bit[i] += val      -> bit[i] ^= val
#
# 3. Inside query():
#    ans += bit[i]      -> ans ^= bit[i]
#
# 4. Inside range_query():
#    query(r) - query(l - 1)
#                ->
#    query(r) ^ query(l - 1)
#
# 5. Inside set_value():
#    update(i, val - arr[i])
#                ->
#    update(i, val ^ arr[i])
#
# NOTES:
# - update(i, x) XORs element i with x.
# - set_value(i, x) replaces element i with x.
# - kth() is NOT supported for XOR.


# ==================================================
# APPLICATIONS / PROBLEM PATTERNS
# ==================================================
#
# Each example assumes a fresh Fenwick Tree.
# Do not run all examples together without
# resetting the BIT using build() or clearing it.


# --------------------------------------------------
# PROBLEM 1: DYNAMIC RANGE SUM
# --------------------------------------------------
# Problem:
# Given an array of N integers, process Q queries:
# 1. Add x to the element at index i.
# 2. Replace the element at index i with x.
# 3. Find the sum of elements in range [l, r].
#
# Approach:
# Build a Fenwick Tree from the original array.
# Use update() for addition.
# Use set_value() for replacement.
# Use range_query() for range sums.
#
# Example:
# values = [2, 4, 1, 5, 3]
#
# build(values)
#
# print(query(3))           # 7
# print(range_query(2, 4))  # 10
#
# update(3, 5)              # Index 3: 1 -> 6
# print(range_query(2, 4))  # 15
#
# set_value(2, 10)          # Index 2: 4 -> 10
# print(query(3))           # 18
#
# Complexity:
# Build O(N), each query O(log N).


# --------------------------------------------------
# PROBLEM 2: DYNAMIC K-TH SMALLEST
# --------------------------------------------------
# Problem:
# Maintain a collection of integers supporting:
# 1. Insert a number x.
# 2. Delete one occurrence of x.
# 3. Find the k-th smallest number.
# 4. Count how many numbers are <= x.
#
# Approach:
# Store FREQUENCIES instead of array values.
#
# BIT index = number value.
# BIT value = frequency of that number.
#
# Insert x:  update(x, 1)
# Delete x:  update(x, -1)
# K-th:      kth(k)
# Count <=x: query(x)
#
# Example:
# Insert numbers [5, 2, 8, 2, 6].
#
# Start with an empty BIT:
#
# for x in [5, 2, 8, 2, 6]:
#     update(x, 1)
#
# Collection (sorted): [2, 2, 5, 6, 8]
#
# print(kth(3))      # 5 (3rd smallest)
# print(query(5))    # 3 (three values <= 5)
#
# update(2, -1)      # Delete one occurrence of 2
#
# Collection: [2, 5, 6, 8]
#
# print(kth(3))      # 6
#
# Complexity: O(log N) per operation.
#
# Notes:
# - Values must be integers in [1, N].
# - Frequencies cannot become negative.
# - Use coordinate compression for large,
#   negative, or arbitrary integer values.


# --------------------------------------------------
# PROBLEM 3: K-TH REMAINING ELEMENT
# --------------------------------------------------
# Problem:
# Given an array of N integers and removal queries.
# Each query gives a position k.
# Remove and print the k-th REMAINING element.
#
# The array is NOT necessarily sorted.
# Positions change after elements are removed.
#
# Approach:
# Do not delete elements from the actual array.
# Track which ORIGINAL positions are still active.
#
# BIT index = original array position.
# BIT value = 1 if active, 0 if removed.
#
# kth(k) finds the original index of the
# k-th remaining element.
#
# Example:
# values = [2, 6, 1, 4, 2]
# removals = [3, 1, 3, 1, 1]
#
# Initialize every position as active:
#
# build([1] * len(values))
#
# Initial state:
# Position:  1  2  3  4  5
# Value:     2  6  1  4  2
# Active:    1  1  1  1  1
#
# ans = []
#
# for k in removals:
#     pos = kth(k)               # Original position
#     ans.append(values[pos - 1]) # Value to remove
#     update(pos, -1)            # Mark as removed
#
# print(*ans)                    # 1 2 2 6 4
#
# Complexity:
# Build O(N), removal queries O(log N) each.
#


# --------------------------------------------------
# PROBLEM 4: COUNT VALUES IN A RANGE
# --------------------------------------------------
# Problem:
# Maintain a collection of integers supporting:
# 1. Insert a number x.
# 2. Delete one occurrence of x.
# 3. Count numbers with values between l and r.
#
# Approach:
# Store the frequency of each number in the BIT.
#
# BIT index = number value.
# BIT value = frequency.
#
# Use range_query(l, r) to count occurrences
# of numbers whose values lie in [l, r].
#
# Example:
# Collection = [2, 2, 5, 6, 8]
#
# Start with an empty BIT:
#
# for x in [2, 2, 5, 6, 8]:
#     update(x, 1)
#
# print(range_query(2, 5))  # 3 (2, 2, 5)
# print(range_query(6, 8))  # 2 (6, 8)
#
# update(5, 1)              # Insert another 5
# print(range_query(2, 5))  # 4
#
# Complexity: O(log N) per operation.
#
# Notes:
# Values must be integers in [1, N].
