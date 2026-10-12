
# ==================================================
# SEGMENT TREE - ITERATIVE
# ==================================================
#
# Indexing: 0-based
# Range queries: [l, r] inclusive
#
# Time Complexity:
# Build: O(n)
# Query: O(log n)
# Point Update: O(log n)
# Point Addition: O(log n)
# Space: O(n)
#
# SUPPORTED OPERATIONS:
#
# seg_build(arr)             -> Build the tree
# seg_query(tree,size,l,r)   -> Query range [l,r]
# seg_update(tree,size,i,x)  -> Set arr[i] = x
# seg_add(tree,size,i,x)     -> Add x to arr[i]
#
# CUSTOMIZABLE QUERIES:
# SUM, MIN, MAX, XOR, GCD, AND, OR
#
# IMPORTANT:
# - Change combine and IDENTITY before building.
# - All indices are 0-based.
# - seg_update() REPLACES the element.
# - seg_add() ADDS to a single element.
# - No lazy propagation (range updates).


from math import gcd


# ==================================================
# CONFIGURATION
# ==================================================
# Change these two lines based on the problem.
#
# SUM: combine = lambda a,b: a+b
#      IDENTITY = 0
#
# MIN: combine = min
#      IDENTITY = float('inf')
#
# MAX: combine = max
#      IDENTITY = float('-inf')
#
# XOR: combine = lambda a,b: a^b
#      IDENTITY = 0
#
# GCD: combine = gcd
#      IDENTITY = 0
#
# AND: combine = lambda a,b: a&b
#      IDENTITY = -1
#
# OR:  combine = lambda a,b: a|b
#      IDENTITY = 0


combine = min
IDENTITY = float('inf')


# --------------------------------------------------
# BUILD SEGMENT TREE - O(n)
# --------------------------------------------------
# Builds from a normal 0-indexed Python list.
#
# Example:
# arr = [2, 4, 1, 5, 3]
# tree, size = seg_build(arr)
#
# Each internal node stores the combination
# of its left and right children.
#
# The array is padded to a power of 2
# using IDENTITY.

def seg_build(arr):
    n = len(arr)
    size = 1

    while size < n:
        size <<= 1

    tree = [IDENTITY] * (2 * size)
    tree[size:size + n] = arr

    for i in range(size - 1, 0, -1):
        tree[i] = combine(tree[2*i], tree[2*i+1])

    return tree, size


# --------------------------------------------------
# RANGE QUERY - O(log n)
# --------------------------------------------------
# Returns the combined result of [l, r].
# Both l and r are inclusive and 0-based.
#
# With combine = min:
# seg_query(tree,size,1,3) -> Minimum of arr[1:4]
#
# With combine = gcd:
# seg_query(tree,size,1,3) -> GCD of arr[1:4]
#
# ans_left and ans_right preserve the order
# of combination for associative operations.

def seg_query(tree, size, l, r):
    l += size
    r += size

    ans_left = IDENTITY
    ans_right = IDENTITY

    while l <= r:
        if l & 1:
            ans_left = combine(ans_left, tree[l])
            l += 1

        if not (r & 1):
            ans_right = combine(tree[r], ans_right)
            r -= 1

        l >>= 1
        r >>= 1

    return combine(ans_left, ans_right)


# --------------------------------------------------
# POINT ASSIGNMENT - O(log n)
# --------------------------------------------------
# Replaces the value at index i with val.
#
# Example:
# arr = [2, 4, 1, 5, 3]
# seg_update(tree, size, 2, 10)
#
# New values: [2, 4, 10, 5, 3]
#
# After changing the leaf, recalculate
# all its ancestors up to the root.

def seg_update(tree, size, i, val):
    i += size
    tree[i] = val

    i >>= 1

    while i:
        tree[i] = combine(tree[2*i], tree[2*i+1])
        i >>= 1


# --------------------------------------------------
# POINT ADDITION - O(log n)
# --------------------------------------------------
# Adds val to the current element at index i.
#
# Example:
# If arr[i] = 5:
# seg_add(tree,size,i,3) -> arr[i] becomes 8
#
# Reads the original value directly from
# the leaf and calls seg_update().
#
# Works for all query configurations since
# the affected aggregates are recalculated.

def seg_add(tree, size, i, val):
    old = tree[size + i]
    seg_update(tree, size, i, old + val)


# ==================================================
# APPLICATIONS / PROBLEM PATTERNS
# ==================================================
#
# Each example assumes the tree is freshly built.
# Choose combine and IDENTITY before building.
#
# The array must be non-empty, and query/update
# indices must be within the original array.


# --------------------------------------------------
# PROBLEM 1: DYNAMIC RANGE SUM
# --------------------------------------------------
# Problem:
# Given an array of N integers, process Q queries:
# 1. Replace arr[i] with x.
# 2. Add x to arr[i].
# 3. Find the sum of elements in [l, r].
#
# Approach:
# Store the SUM of each segment.
# Update the affected leaf and its ancestors.
#
# Configuration:
# combine = lambda a,b: a+b
# IDENTITY = 0
#
# Example:
# arr = [2, 4, 1, 5, 3]
# tree, size = seg_build(arr)
#
# print(seg_query(tree,size,1,3))  # 10
#
# seg_update(tree,size,2,7)
# print(seg_query(tree,size,1,3))  # 16
#
# seg_add(tree,size,1,3)
# print(seg_query(tree,size,1,3))  # 19
#
# Complexity: O(log n) per query.
#
# Example: CSES - Dynamic Range Sum Queries


# --------------------------------------------------
# PROBLEM 2: DYNAMIC RANGE MINIMUM / MAXIMUM
# --------------------------------------------------
# Problem:
# Given an array, support point updates and
# queries asking for the MIN or MAX in [l,r].
#
# Approach:
# Store the minimum or maximum of each segment.
#
# MIN Configuration:
# combine = min
# IDENTITY = float('inf')
#
# MAX Configuration:
# combine = max
# IDENTITY = float('-inf')
#
# Example (MIN):
# arr = [8, 3, 5, 1, 6]
# tree, size = seg_build(arr)
#
# print(seg_query(tree,size,1,4))  # 1
#
# seg_update(tree,size,3,9)
# print(seg_query(tree,size,1,4))  # 3
#
# seg_add(tree,size,1,-2)
# print(seg_query(tree,size,1,4))  # 1
#
# Complexity: O(log n) per query.
#
# Example: CSES - Dynamic Range Minimum Queries


# --------------------------------------------------
# PROBLEM 3: DYNAMIC RANGE GCD
# --------------------------------------------------
# Problem:
# Given an array of integers, support:
# 1. Updating the value at an index.
# 2. Finding the GCD of all numbers in [l,r].
#
# Approach:
# Store the GCD of each segment.
#
# Configuration:
# combine = gcd
# IDENTITY = 0
#
# Example:
# arr = [12, 18, 6, 15]
# tree, size = seg_build(arr)
#
# print(seg_query(tree,size,0,2))  # 6
#
# seg_update(tree,size,2,9)
# print(seg_query(tree,size,0,2))  # 3
#
# Complexity: O(log n) per query.


# --------------------------------------------------
# PROBLEM 4: DYNAMIC RANGE XOR
# --------------------------------------------------
# Problem:
# Given an array, process point updates and
# queries asking for XOR of values in [l,r].
#
# Approach:
# Store XOR of each segment.
#
# Configuration:
# combine = lambda a,b: a^b
# IDENTITY = 0
#
# Example:
# arr = [1, 2, 3, 4]
# tree, size = seg_build(arr)
#
# print(seg_query(tree,size,0,2))  # 0
#
# seg_update(tree,size,2,7)
# print(seg_query(tree,size,0,2))  # 4
#
# Complexity: O(log n) per query.


# --------------------------------------------------
# PROBLEM 5: RANGE BITWISE AND / OR
# --------------------------------------------------
# Problem:
# Given an array, update individual values and
# calculate bitwise AND or OR over [l,r].
#
# Approach:
# Store the AND or OR of each segment.
#
# AND Configuration:
# combine = lambda a,b: a&b
# IDENTITY = -1
#
# OR Configuration:
# combine = lambda a,b: a|b
# IDENTITY = 0
#
# Example:
# arr = [6, 3, 5]
#
# Range AND: 6 & 3 & 5 = 0
# Range OR:  6 | 3 | 5 = 7
#
# Update a value using seg_update().
#
# Complexity: O(log n) per query.


# ==================================================
# IMPORTANT NOTES
# ==================================================
#
# 1. The query operation must be associative:
#    combine(combine(a,b),c)
#       == combine(a,combine(b,c))
#
# 2. IDENTITY must be a neutral value:
#    combine(x, IDENTITY) == x
#
# 3. The tree is 0-indexed externally.
#    Queries use inclusive ranges [l,r].
#
# 4. seg_update() replaces a single element.
#    seg_add() adds to a single element.
#
# 5. seg_add() is arithmetic addition to the
#    original value, regardless of query mode.
#
# 6. Changing combine or IDENTITY requires
#    rebuilding the Segment Tree.
#
# 7. This template does not support updating
#    an entire range in O(log n).
#    Use a Lazy Segment Tree for that.

