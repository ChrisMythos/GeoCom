class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def insert(self, root, value):
        if not root:
            return Node(value)
        elif value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        # Left rotation
        if balance > 1 and value < root.left.value:
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def range_search(self, node, low, high, result):
        """Recursive helper for range search."""
        if not node:
            return
        # Check the left subtree if there is a chance of finding values in range
        if low < node.value:
            self.range_search(node.left, low, high, result)
        # If the current node is in range, add it to the result
        if low <= node.value <= high:
            result.append(node.value)
        # Check the right subtree if there is a chance of finding values in range
        if high > node.value:
            self.range_search(node.right, low, high, result)

    def search_range(self, low, high):
        """Initiate the range search."""
        result = []
        self.range_search(self.root, low, high, result)
        return result

    def insert_value(self, value):
        self.root = self.insert(self.root, value)


# Demo main method
if __name__ == "__main__":
    avl = AVLTree()
    
    # Insert values
    for value in [20, 10, 30, 5, 15, 25, 35]:
        avl.insert_value(value)
    
    # Perform range search
    low, high = 10, 30
    print(f"Values in the range [{low}, {high}]: {avl.search_range(low, high)}")