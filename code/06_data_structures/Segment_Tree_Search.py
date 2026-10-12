
# ============================================================
# SEGMENT TREE SEARCH - ITERATIVE
# ============================================================
#
# Indexing: 0-based
# Range queries: [l, r] inclusive
#
# SEARCH OPERATIONS:
#
# 1. first_at_least(x, start)
#    Find first index >= start with arr[i] >= x.
#
# 2. kth(k)
#    Find the index of the k-th active element.
#    Also works for frequency-based multisets.
#
# 3. prefix_lower_bound(x)
#    Find first index with prefix sum >= x.
#
# SUPPORTED MODES:
# "MAX" -> First element >= x
# "SUM" -> K-th active / Prefix lower bound
#
# TIME COMPLEXITY:
# Build:        O(n)
# Point update: O(log n)
# Range query:  O(log n)
# Search:       O(log n)
# Space:        O(n)
#
# No recursion, no OOP.


# ============================================================
# CONFIGURATION
# ============================================================

MODE = "SUM"  # "SUM" or "MAX"

n = 0
size = 1
tree = []
combine = None
IDENTITY = None


# ============================================================
# BUILD - O(n)
# ============================================================
# Build from a 0-indexed list.
#
# SUM -> Each node stores its segment sum.
# MAX -> Each node stores its segment maximum.
#
# Calling build() resets the tree.

def build(values):
    global n, size, tree, combine, IDENTITY

    n = len(values)

    if n == 0:
        raise ValueError("Empty array")

    if MODE == "SUM":
        combine = lambda a, b: a + b
        IDENTITY = 0

    elif MODE == "MAX":
        combine = max
        IDENTITY = float('-inf')

    else:
        raise ValueError("Invalid MODE")

    size = 1 << (n - 1).bit_length()

    tree = [IDENTITY] * (2 * size)
    tree[size:size + n] = values

    for p in range(size - 1, 0, -1):
        tree[p] = combine(tree[2*p], tree[2*p+1])


# ============================================================
# POINT ASSIGNMENT - O(log n)
# ============================================================
# Replace arr[i] with x.

def set_value(i, x):
    p = i + size
    tree[p] = x

    while p > 1:
        p >>= 1
        tree[p] = combine(tree[2*p], tree[2*p+1])


# ============================================================
# POINT ADDITION - O(log n)
# ============================================================
# Add x to arr[i].

def add_value(i, x):
    set_value(i, tree[size + i] + x)


# ============================================================
# RANGE QUERY - O(log n)
# ============================================================
# Inclusive query [l, r].
# SUM mode returns range sum.
# MAX mode returns range maximum.

def query(l, r):
    l += size
    r += size

    left = IDENTITY
    right = IDENTITY

    while l <= r:
        if l & 1:
            left = combine(left, tree[l])
            l += 1

        if not (r & 1):
            right = combine(tree[r], right)
            r -= 1

        l >>= 1
        r >>= 1

    return combine(left, right)


# ============================================================
# SEARCH 1: FIRST ELEMENT >= X - O(log n)
# ============================================================
#
# MAX MODE ONLY.
#
# Find the smallest index i >= start such that:
#
# arr[i] >= x
#
# Returns -1 if no such index exists.
#
# Array does NOT need to be sorted.
#
# Search strategy:
# 1. Start at the leaf representing start.
# 2. Skip segments whose maximum < x.
# 3. Find the first qualifying segment.
# 4. Descend to its leftmost qualifying leaf.

def first_at_least(x, start=0):
    if MODE != "MAX":
        raise ValueError("Requires MAX mode")

    if start >= n:
        return -1

    p = start + size

    while True:

        # Move to the next segment in order.
        while p % 2 == 0:
            p >>= 1

        # This segment contains a valid answer.
        if tree[p] >= x:

            # Descend to the first qualifying leaf.
            while p < size:
                p *= 2

                if tree[p] < x:
                    p += 1

            ans = p - size

            return ans if ans < n else -1

        # Skip this entire segment.
        p += 1

        # Reached the end of the tree.
        if p & (p - 1) == 0:
            break

    return -1


# ============================================================
# SEARCH 2: PREFIX LOWER BOUND - O(log n)
# ============================================================
#
# SUM MODE ONLY.
#
# Find the smallest index i such that:
#
# arr[0] + arr[1] + ... + arr[i] >= target
#
# Returns -1 if no such index exists.
#
# IMPORTANT:
# All array values must be NON-NEGATIVE.
#
# Search strategy:
# 1. Check the left child's sum.
# 2. If it is >= target, go left.
# 3. Otherwise, subtract it and go right.

def prefix_lower_bound(target):
    if MODE != "SUM":
        raise ValueError("Requires SUM mode")

    if target <= 0 or target > tree[1]:
        return -1

    p = 1

    while p < size:
        p *= 2

        if tree[p] < target:
            target -= tree[p]
            p += 1

    ans = p - size

    return ans if ans < n else -1


# ============================================================
# SEARCH 3: K-TH ACTIVE ELEMENT - O(log n)
# ============================================================
#
# SUM MODE ONLY.
#
# Store:
# 1 -> Active position
# 0 -> Removed position
#
# k is 1-based:
# kth(1) -> First active element
# kth(2) -> Second active element
#
# Returns original 0-based index.
# Returns -1 if k is invalid.
#
# With frequencies instead of 0/1, it finds
# the k-th occurrence in the multiset.
#
# Requires NON-NEGATIVE integer frequencies.

def kth(k):
    return prefix_lower_bound(k)


# ============================================================
# APPLICATIONS / PROBLEM PATTERNS
# ============================================================
#
# Each example uses a fresh build().
# Change MODE BEFORE calling build().


# ------------------------------------------------------------
# PROBLEM 1: FIRST ELEMENT >= X
# ------------------------------------------------------------
# Problem:
# Given an unsorted array, support:
#
# 1. Updating individual elements.
# 2. Finding the first index >= start whose
#    value is at least x.
#
# Approach:
# Use MAX mode.
#
# If a segment's maximum is smaller than x,
# the entire segment can be skipped.
#
# Otherwise descend to the first valid leaf.
#
# MODE = "MAX"
#
# build([2, 4, 1, 8, 3, 7])
#
# print(first_at_least(6))     # 3
# print(first_at_least(6, 4))  # 5
#
# set_value(3, 2)
#
# print(first_at_least(6))     # 5
#
# Complexity: O(log n) per operation.
#
# IMPORTANT:
# This works on UNSORTED arrays.


# ------------------------------------------------------------
# PROBLEM 2: K-TH REMAINING ELEMENT
# ------------------------------------------------------------
# Problem:
# Given an array, repeatedly:
#
# 1. Find the k-th remaining element.
# 2. Print its original value.
# 3. Remove that element.
#
# Approach:
# Use SUM mode.
# Store 1 at active positions, 0 at removed.
#
# kth(k) returns the original index of
# the k-th active element.
#
# MODE = "SUM"
#
# a = [2, 6, 1, 4, 2]
# removals = [3, 1, 3, 1, 1]
#
# build([1] * len(a))
#
# ans = []
#
# for k in removals:
#     pos = kth(k)
#     ans.append(a[pos])
#     set_value(pos, 0)
#
# print(ans)
# # [1, 2, 2, 6, 4]
#
# Complexity: O(log n) per removal.


# ------------------------------------------------------------
# PROBLEM 3: PREFIX SUM LOWER BOUND
# ------------------------------------------------------------
# Problem:
# Given an array of non-negative numbers,
# find the first index whose prefix sum
# is at least target.
#
# Approach:
# Use SUM mode.
#
# At each node:
# - If left sum >= target, go left.
# - Otherwise, subtract left sum and go right.
#
# MODE = "SUM"
#
# build([2, 0, 3, 1])
#
# # Prefix sums: [2, 2, 5, 6]
#
# print(prefix_lower_bound(1))  # 0
# print(prefix_lower_bound(3))  # 2
# print(prefix_lower_bound(5))  # 2
# print(prefix_lower_bound(6))  # 3
# print(prefix_lower_bound(7))  # -1
#
# Complexity: O(log n) per query.


# ------------------------------------------------------------
# PROBLEM 4: K-TH SMALLEST IN A MULTISET
# ------------------------------------------------------------
# Problem:
# Maintain a multiset of integer values.
#
# Support:
# 1. Insert x.
# 2. Delete one occurrence of x.
# 3. Find the k-th smallest value.
#
# Approach:
# Use SUM mode.
#
# Each index represents a VALUE.
# Each leaf stores that value's frequency.
#
# kth(k) returns the value index, not
# an original array position.
#
# MODE = "SUM"
#
# # Values allowed: 0 through 4
# build([0, 2, 1, 0, 3])
#
# # Multiset: [1, 1, 2, 4, 4, 4]
#
# print(kth(1))  # 1
# print(kth(3))  # 2
# print(kth(4))  # 4
#
# add_value(2, -1)  # Remove one value 2
#
# print(kth(3))  # 4
#
# Complexity: O(log n) per operation.
#
# Large or negative values may require
# coordinate compression.


# ============================================================
# IMPORTANT NOTES
# ============================================================
#
# 1. External indexing is 0-based.
#    Queries are inclusive [l, r].
#
# 2. All search functions return original
#    0-based indices, or -1 if not found.
#
# 3. first_at_least(x, start) needs MAX mode.
#    Valid start: 0 <= start <= n.
#    No sorted array is required.
#
# 4. kth(k) and prefix_lower_bound(x)
#    require SUM mode.
#
# 5. Prefix lower bound requires all values
#    to be NON-NEGATIVE.
#
# 6. kth(k) uses 1-based k and requires
#    non-negative integer frequencies.
#
# 7. Never delete an absent element from a
#    frequency tree. Frequencies must remain
#    non-negative.
#
# 8. kth(k) can find:
#    - K-th active original position
#    - K-th smallest value in a multiset
#
#    The meaning of indices depends on
#    what you store in the leaves.
#
# 9. Changing MODE requires rebuilding.
#
# 10. This tree supports point updates only.
#     Use Lazy Segment Tree for range updates.
