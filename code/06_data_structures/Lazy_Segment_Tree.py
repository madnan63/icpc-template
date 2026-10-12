
# ============================================================
# LAZY SEGMENT TREE - ITERATIVE
# ============================================================
#
# 0-based indexing; inclusive ranges [l, r].
#
# QUERY MODES: SUM, MIN, MAX
# RANGE UPDATES: ADD, SET
# POINT UPDATES: ADD, SET
#
# Build:        O(n)
# Range query:  O(log n)
# Range update: O(log n)
# Point update: O(log n)
# Memory:       O(n)
#
# No recursion, no OOP.
#
# Change MODE before calling build().


# ============================================================
# CONFIGURATION
# ============================================================

MODE = "SUM"  # "SUM", "MIN", or "MAX"

combine = None
IDENTITY = None


# ============================================================
# GLOBAL ARRAYS
# ============================================================

n = 0
size = 1
height = 0

tree = []
lazy_add = []
lazy_set = []
seg_len = []


# ============================================================
# BUILD - O(n)
# ============================================================
# Pads the array to the next power of 2.
#
# tree[p] stores the aggregate of node p.
# lazy_add[p] stores a pending addition.
# lazy_set[p] stores a pending assignment.
# seg_len[p] stores the length of node p's segment.
#
# None means no pending assignment.
# Calling build() again resets everything.

def build(a):
    global n, size, height
    global tree, lazy_add, lazy_set, seg_len
    global combine, IDENTITY

    n = len(a)

    if n == 0:
        raise ValueError("Array must not be empty")

    if MODE == "SUM":
        combine = lambda x, y: x + y
        IDENTITY = 0

    elif MODE == "MIN":
        combine = min
        IDENTITY = float('inf')

    elif MODE == "MAX":
        combine = max
        IDENTITY = float('-inf')

    else:
        raise ValueError("Invalid MODE")

    size = 1 << (n - 1).bit_length()
    height = size.bit_length() - 1

    tree = [IDENTITY] * (2 * size)
    tree[size:size + n] = a

    lazy_add = [0] * (2 * size)
    lazy_set = [None] * (2 * size)

    seg_len = [0] * (2 * size)

    for i in range(size, 2 * size):
        seg_len[i] = 1

    for i in range(size - 1, 0, -1):
        seg_len[i] = seg_len[2*i] + seg_len[2*i+1]
        tree[i] = combine(tree[2*i], tree[2*i+1])


# ============================================================
# APPLY SET TO ONE SEGMENT - O(1)
# ============================================================
# Set every element in node p's segment to x.
#
# SUM -> x * segment_length
# MIN/MAX -> x
#
# SET overrides any previous pending ADD.

def _apply_set(p, x):
    if MODE == "SUM":
        tree[p] = x * seg_len[p]
    else:
        tree[p] = x

    if p < size:
        lazy_set[p] = x
        lazy_add[p] = 0


# ============================================================
# APPLY ADD TO ONE SEGMENT - O(1)
# ============================================================
# Add x to every element in node p's segment.
#
# SUM -> increase by x * segment_length
# MIN/MAX -> increase by x
#
# If SET is pending, adjust that assignment.

def _apply_add(p, x):
    if MODE == "SUM":
        tree[p] += x * seg_len[p]
    else:
        tree[p] += x

    if p < size:
        if lazy_set[p] is not None:
            lazy_set[p] += x
        else:
            lazy_add[p] += x


# ============================================================
# PUSH LAZY UPDATES TO CHILDREN - O(1)
# ============================================================
# Used only for internal nodes.
#
# SET first, then ADD.
# Children receive pending updates before we
# read or modify their contents.

def _push(p):
    x = lazy_set[p]

    if x is not None:
        _apply_set(2*p, x)
        _apply_set(2*p+1, x)
        lazy_set[p] = None

    x = lazy_add[p]

    if x:
        _apply_add(2*p, x)
        _apply_add(2*p+1, x)
        lazy_add[p] = 0


# ============================================================
# PUSH THE TWO BOUNDARY PATHS - O(log n)
# ============================================================
# Uses half-open internal coordinates [L, R).
#
# Before an operation, push pending changes
# along boundaries that split a segment.
#
# Already aligned segments do not need pushing.

def _push_boundaries(L, R):
    for h in range(height, 0, -1):
        if L & ((1 << h) - 1):
            _push(L >> h)

        if R & ((1 << h) - 1):
            _push((R - 1) >> h)


# ============================================================
# REBUILD THE TWO BOUNDARY PATHS - O(log n)
# ============================================================
# After updating covered nodes, recalculate
# only ancestors of the split boundaries.
#
# Completely covered nodes already have
# correct aggregates from _apply_add/_apply_set.

def _pull_boundaries(L, R):
    for h in range(1, height + 1):
        if L & ((1 << h) - 1):
            p = L >> h
            tree[p] = combine(tree[2*p], tree[2*p+1])

        if R & ((1 << h) - 1):
            p = (R - 1) >> h
            tree[p] = combine(tree[2*p], tree[2*p+1])


# ============================================================
# INTERNAL RANGE UPDATE - O(log n)
# ============================================================
# Shared logic for Range ADD and Range SET.
#
# 1. Push lazy tags on the boundary paths.
# 2. Apply the update to fully covered segments.
# 3. Rebuild affected ancestors.
#
# Same bottom-up traversal as a normal
# iterative Segment Tree.

def _range_apply(l, r, x, apply):
    L = l + size
    R = r + size + 1

    _push_boundaries(L, R)

    a, b = L, R

    while a < b:
        if a & 1:
            apply(a, x)
            a += 1

        if b & 1:
            b -= 1
            apply(b, x)

        a >>= 1
        b >>= 1

    _pull_boundaries(L, R)


# ============================================================
# RANGE ADD - O(log n)
# ============================================================
# Add x to all elements in inclusive [l, r].

def range_add(l, r, x):
    _range_apply(l, r, x, _apply_add)


# ============================================================
# RANGE SET - O(log n)
# ============================================================
# Replace all elements in inclusive [l, r] with x.

def range_set(l, r, x):
    _range_apply(l, r, x, _apply_set)


# ============================================================
# RANGE QUERY - O(log n)
# ============================================================
# Return SUM/MIN/MAX of inclusive [l, r].
#
# Push pending updates before querying.
#
# Uses two accumulators, as in our Basic
# Segment Tree.

def query(l, r):
    L = l + size
    R = r + size + 1

    _push_boundaries(L, R)

    left = IDENTITY
    right = IDENTITY

    while L < R:
        if L & 1:
            left = combine(left, tree[L])
            L += 1

        if R & 1:
            R -= 1
            right = combine(tree[R], right)

        L >>= 1
        R >>= 1

    return combine(left, right)


# ============================================================
# POINT UPDATES - O(log n)
# ============================================================

# Replace arr[i] with x.
def set_value(i, x):
    range_set(i, i, x)


# Add x to arr[i].
def add_value(i, x):
    range_add(i, i, x)


# ============================================================
# APPLICATIONS / PROBLEM PATTERNS
# ============================================================
#
# Change MODE before build().
# Each example starts with a fresh build().


# ------------------------------------------------------------
# PROBLEM 1: RANGE ADD + RANGE SUM
# ------------------------------------------------------------
# Problem:
# Add x to every element in [l, r].
# Answer range sum queries.
#
# Approach:
# Use SUM mode. When adding x to a segment
# of length k, its sum increases by x * k.
#
# MODE = "SUM"
#
# build([2, 4, 1, 5, 3])
# range_add(1, 3, 10)
#
# # Array: [2, 14, 11, 15, 3]
#
# print(query(1, 3))  # 40
# print(query(0, 4))  # 45


# ------------------------------------------------------------
# PROBLEM 2: RANGE SET + RANGE SUM
# ------------------------------------------------------------
# Problem:
# Replace every value in [l, r] with x.
# Answer range sum queries.
#
# Approach:
# Use SUM mode. Setting a segment of
# length k to x makes its sum x * k.
#
# MODE = "SUM"
#
# build([2, 4, 1, 5, 3])
# range_set(1, 3, 7)
#
# # Array: [2, 7, 7, 7, 3]
#
# print(query(0, 4))  # 26


# ------------------------------------------------------------
# PROBLEM 3: RANGE ADD / SET + MIN / MAX
# ------------------------------------------------------------
# Problem:
# Support range additions and assignments.
# Find the minimum or maximum in [l, r].
#
# Approach:
# Use MIN or MAX mode.
# Adding x increases the min/max by x.
# Setting a segment to x makes its min/max x.
#
# MODE = "MIN"  # or "MAX"
#
# build([8, 3, 5, 1, 6])
# range_add(1, 3, 4)
#
# # Array: [8, 7, 9, 5, 6]
#
# print(query(0, 4))
# # MIN -> 5
# # MAX -> 9
#
# range_set(2, 4, 2)
#
# # Array: [8, 7, 2, 2, 2]
#
# print(query(0, 4))
# # MIN -> 2
# # MAX -> 8


# ------------------------------------------------------------
# PROBLEM 4: OVERLAPPING RANGE ADD AND SET
# ------------------------------------------------------------
# Problem:
# Range additions and assignments overlap.
# The order of operations must be preserved.
#
# Approach:
# A later SET overrides previous updates.
# A later ADD modifies a pending SET or ADD.
#
# MODE = "SUM"
#
# build([1, 2, 3, 4])
#
# range_add(0, 3, 5)    # [6, 7, 8, 9]
# range_set(1, 2, 0)    # [6, 0, 0, 9]
# range_add(2, 3, 2)    # [6, 0, 2, 11]
#
# print(query(0, 3))    # 19


# ============================================================
# IMPORTANT NOTES
# ============================================================
#
# 1. All external indices are 0-based.
#    Range boundaries [l, r] are inclusive.
#    Valid: 0 <= l <= r < n.
#
# 2. Internally, the tree uses [L, R),
#    so R = r + size + 1.
#
# 3. MODE can be "SUM", "MIN", or "MAX".
#    Set it before calling build().
#    Changing MODE requires rebuilding.
#
# 4. range_add() adds x to every element.
#    range_set() replaces every element with x.
#
# 5. lazy_set[p] = None means no pending SET.
#    A SET to zero must still be recorded.
#
# 6. A SET overwrites a previous pending ADD.
#    An ADD after SET modifies that SET value.
#
# 7. _push_boundaries() prevents stale children
#    from being used during queries/updates.
#
# 8. _pull_boundaries() updates only affected
#    ancestors, not fully covered lazy nodes.
#
# 9. Padding nodes use the neutral identity.
#    Public queries/updates must remain
#    within the original array length.
#
# 10. This template is specialized for
#     ADD/SET with SUM/MIN/MAX.
#     Other operations need different
#     lazy propagation rules.
