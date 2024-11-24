class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
        self.successor = None  # Add successor pointer


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

    def insert(self, root, value, predecessor=None, successor=None):
        if not root:
            # Create new node and set its successor pointer
            new_node = Node(value)
            new_node.successor = successor
            # Update predecessor's successor pointer
            if predecessor:
                predecessor.successor = new_node
            return new_node

        elif value < root.value:
            # Current node is potential successor
            root.left = self.insert(root.left, value, predecessor, root)
        else:
            # Current node is potential predecessor
            root.right = self.insert(root.right, value, root, successor)

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        # Left Left Case
        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        # Successor pointers remain unchanged because in-order sequence is preserved
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        # Successor pointers remain unchanged because in-order sequence is preserved
        return y

    def find_min_ge(self, node, value):
        """Find the node with the minimum value >= given value."""
        if not node:
            return None
        if node.value == value:
            return node
        elif node.value < value:
            return self.find_min_ge(node.right, value)
        else:
            # node.value > value
            left_result = self.find_min_ge(node.left, value)
            return left_result if left_result else node

    def search_range(self, low, high):
        """Search for all values in the given range using successor pointers."""
        result = []
        node = self.find_min_ge(self.root, low)
        while node and node.value <= high:
            result.append(node.value)
            node = node.successor
        return result

    def insert_value(self, value):
        self.root = self.insert(self.root, value)


# Demo main method (dont use this in the actual implementation)
if __name__ == "__main__":
    avl = AVLTree()

    # Insert values
    for value in [20, 10, 30, 5, 15, 25, 35]:
        avl.insert_value(value)
        print(f"Inserted: {value}")

    # Perform range search
    low, high = 10, 30
    print(f"Values in the range [{low}, {high}]: {avl.search_range(low, high)}")
