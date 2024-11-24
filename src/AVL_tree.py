class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
        self.successor = None  # In-order successor


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def insert(self, root, value, predecessor=None, successor=None):
        if not root:
            new_node = Node(value)
            new_node.successor = successor
            if predecessor:
                predecessor.successor = new_node
            return new_node

        if value < root.value:
            # Current node is potential successor
            root.left = self.insert(root.left, value, predecessor, root)
        else:
            # Current node is potential predecessor
            root.right = self.insert(root.right, value, root, successor)

        # Update height and balance
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        return self.rebalance(root)

    def delete(self, root, value, parent=None):
        if not root:
            return root

        if value < root.value:
            root.left = self.delete(root.left, value, root)
        elif value > root.value:
            root.right = self.delete(root.right, value, root)
        else:
            # Node with one child or no child
            if not root.left or not root.right:
                temp = root.left if root.left else root.right

                # only one child case
                if temp:
                    # Copy the contents of the non-empty child
                    temp.successor = root.successor
                
                # No child case
                else:
                    # Update successor pointers
                    self.update_successor_pointers_on_delete(root, parent, temp)

                root = temp  # Replace root with its child
            else:
                # Node with two children: Get the inorder successor
                temp = self.get_min_value_node(root.right)

                # Copy the inorder successor's value to this node
                root.value = temp.value

                # Delete the inorder successor
                root.right = self.delete(root.right, temp.value, root)

        if not root:
            return root

        # Update height and rebalance
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        return self.rebalance(root)

    def update_successor_pointers_on_delete(self, node_to_delete, parent, child):
        """Update successor pointers when a node is deleted."""
        # Update the predecessor's successor pointer
        predecessor = self.find_predecessor(self.root, node_to_delete.value)
        if predecessor:
            predecessor.successor = node_to_delete.successor
        # If the node_to_delete is the root and has no predecessor
        elif parent is None:
            if child:
                # Update successor of child if it exists
                child.successor = node_to_delete.successor

    def find_predecessor(self, root, value):
        """Find the predecessor of the node with the given value."""
        predecessor = None
        current = root
        while current:
            if value > current.value:
                predecessor = current
                current = current.right
            elif value < current.value:
                current = current.left
            else:
                if current.left:
                    predecessor = self.get_max_value_node(current.left)
                break
        return predecessor

    def get_min_value_node(self, node):
        """Get the node with the minimum value (leftmost leaf)."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def get_max_value_node(self, node):
        """Get the node with the maximum value (rightmost leaf)."""
        current = node
        while current.right is not None:
            current = current.right
        return current

    def rebalance(self, root):
        balance = self.balance(root)

        # Left Left Case
        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)

        # Left Right Case
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)

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

        # Successor pointers remain valid after rotation
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

        # Successor pointers remain valid after rotation
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

    def delete_value(self, value):
        self.root = self.delete(self.root, value)

    def inorder(self, node):
        """Helper function to perform inorder traversal (for testing)."""
        if not node:
            return []
        return self.inorder(node.left) + [node.value] + self.inorder(node.right)

# Demo main method
if __name__ == "__main__":
    avl = AVLTree()

    # Insert values
    for value in [20, 10, 30, 5, 15, 25, 35]:
        avl.insert_value(value)
        print(f"Inserted {value}: {avl.inorder(avl.root)}")

    # Perform range search before deletion
    low, high = 10, 30
    print(f"Values in the range [{low}, {high}] before deletion: {avl.search_range(low, high)}")

    # Delete a node with two children
    avl.delete_value(20)

    # Perform range search after deletion
    print(f"Values in the range [{low}, {high}] after deleting 20: {avl.search_range(low, high)}")

    # Delete a leaf node
    avl.delete_value(5)

    # Perform range search after deletion
    print(f"Values in the range [{low}, {high}] after deleting 5: {avl.search_range(low, high)}")

    # Delete a node with one child
    avl.delete_value(30)

    # Perform range search after deletion
    print(f"Values in the range [{low}, {high}] after deleting 30: {avl.search_range(low, high)}")

    # Check the in-order traversal of the tree
    print("In-order traversal of the AVL tree:", avl.inorder(avl.root))
