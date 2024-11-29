class Node:
    def __init__(self, key, segment=None):
        self.key = key               # y-coordinate of the segment
        self.segment = segment       # Pointer to the line segment object
        self.left = None             # Left child
        self.right = None            # Right child
        self.height = 1              # Height of the subtree
        self.successor = None        # In-order successor


class AVLTree:
    def __init__(self):
        self.root = None

    # Utility function to get the height of the tree
    def height(self, node):
        return node.height if node else 0

    # Utility function to calculate balance factor of node
    def get_balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    # Right rotate subtree rooted with y
    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        # Successor pointers remain valid after rotation
        return x

    # Left rotate subtree rooted with x
    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        # Successor pointers remain valid after rotation
        return y

    # Insert a node and update successor pointers
    def insert(self, node, key, segment=None, predecessor=None, successor=None):
        # Perform standard BST insert
        if not node:
            new_node = Node(key, segment)
            new_node.successor = successor
            if predecessor:
                predecessor.successor = new_node
            return new_node

        if key < node.key:
            # Current node is potential successor
            node.left = self.insert(node.left, key, segment, predecessor, node)
        else:
            # Current node is potential predecessor
            node.right = self.insert(node.right, key, segment, node, successor)

        # Update height of this ancestor node
        node.height = 1 + max(self.height(node.left), self.height(node.right))

        # Get the balance factor to check whether this node became unbalanced
        balance = self.get_balance(node)

        # Balance the tree
        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # Find the node with minimum key value (leftmost leaf)
    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Find the node with maximum key value (rightmost leaf)
    def max_value_node(self, node):
        current = node
        while current.right is not None:
            current = current.right
        return current

    # Delete a node and update successor pointers
    # Modified delete method
# Modified delete method with the fix
    def delete(self, node, key, predecessor=None, successor=None):
        # Perform standard BST delete
        if not node:
            return node

        if key < node.key:
            # Current node is potential successor
            node.left = self.delete(node.left, key, predecessor, node)
        elif key > node.key:
            # Current node is potential predecessor
            node.right = self.delete(node.right, key, node, successor)
        else:
            # Node with one child or no child
            if not node.left or not node.right:
                temp = node.left if node.left else node.right

                if temp:
                    temp.successor = node.successor
                if predecessor:
                    predecessor.successor = node.successor
                else:
                    # If deleting the root node with no predecessor
                    if temp:
                        temp.successor = node.successor

                node = temp  # Replace node with its child (could be None)
            else:
                # Node with two children:
                # Get the inorder successor (smallest in the right subtree)
                temp = self.min_value_node(node.right)

                # Copy the inorder successor's data to this node
                node.key = temp.key
                node.segment = temp.segment

                # Delete the inorder successor
                node.right = self.delete(node.right, temp.key, node, successor)

        if not node:
            return node

        # Update height
        node.height = 1 + max(self.height(node.left), self.height(node.right))

        # Balance the tree
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and self.get_balance(node.left) >= 0:
            node = self.right_rotate(node)
        # Left Right Case
        elif balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            node = self.right_rotate(node)
        # Right Right Case
        elif balance < -1 and self.get_balance(node.right) <= 0:
            node = self.left_rotate(node)
        # Right Left Case
        elif balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            node = self.left_rotate(node)

        # Dirty fix: Ensure that the successor of the highest node is None
        if node.successor == node:
            node.successor = None

        return node
    # Public methods to insert and delete values

    def insert_value(self, key, segment=None):
        self.root = self.insert(self.root, key, segment)

    def delete_value(self, key):
        self.root = self.delete(self.root, key)

    # In-order traversal (for testing purposes)
    def inorder(self, node):
        if not node:
            return []
        return self.inorder(node.left) + [(node.key, node.successor.key if node.successor else None)] + self.inorder(node.right)


# Test the AVL Tree implementation with some examples (for testing purposes only, dont run this code in the main program)
if __name__ == "__main__":
    avl = AVLTree()

    # First Tests
    values_to_insert = [20, 10, 30, 5, 15, 25, 35]
    for value in values_to_insert:
        avl.insert_value(value)

    print("First Tests:")
    print("Tree after insertions (key, successor_key):")
    print(avl.inorder(avl.root))

    # Delete node with two children
    avl.delete_value(20)
    print("\nTree after deleting 20 (key, successor_key):")
    print(avl.inorder(avl.root))

    # Delete a leaf node
    avl.delete_value(5)
    print("\nTree after deleting 5 (key, successor_key):")
    print(avl.inorder(avl.root))

    # Delete node with one child
    avl.delete_value(30)
    print("\nTree after deleting 30 (key, successor_key):")
    print(avl.inorder(avl.root))

    # Delete all nodes
    avl.delete_value(10)
    avl.delete_value(15)
    avl.delete_value(25)
    avl.delete_value(35)
    print("\nTree after deleting all nodes:")
    print(avl.inorder(avl.root))

    # Additional Tests
    avl = AVLTree()
    values_to_insert = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for value in values_to_insert:
        avl.insert_value(value)

    print("\nAdditional Tests:")
    print("Tree after insertions (key, successor_key):")
    print(avl.inorder(avl.root))

    # Delete node with two children
    avl.delete_value(30)
    print("\nTree after deleting 30 (key, successor_key):")
    print(avl.inorder(avl.root))

    # Delete a leaf node
    avl.delete_value(10)
    print("\nTree after deleting 10 (key, successor_key):")
    print(avl.inorder(avl.root))

    # Delete node with one child
    avl.delete_value(80)
    print("\nTree after deleting 80 (key, successor_key):")
    print(avl.inorder(avl.root))

    # Delete multiple nodes
    avl.delete_value(50)
    avl.delete_value(70)
    print("\nTree after deleting 50 and 70 (key, successor_key):")
    print(avl.inorder(avl.root))
