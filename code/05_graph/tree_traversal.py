# Binary tree:
# tree[node] = (left_child, right_child)

def inorder_traversal(tree, root):
    inorder = []
    stack = []
    current = root

    while current is not None or stack:
        while current is not None:
            stack.append(current)
            current = tree.get(current, (None, None))[0]

        current = stack.pop()
        inorder.append(current)

        current = tree.get(current, (None, None))[1]

    return inorder


# N-ary tree:
# tree[node] = [child1, child2, ...]

def dfs_nary(tree, root):
    preorder = []
    postorder = []

    stack = [(root, 0)]

    while stack:
        node, i = stack.pop()

        if i == 0:
            preorder.append(node)

        children = tree.get(node, [])

        if i < len(children):
            stack.append((node, i + 1))
            stack.append((children[i], 0))
        else:
            postorder.append(node)

    return preorder, postorder
