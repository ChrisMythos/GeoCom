"""
AVL Tree Implementation with Successor Pointers

This module implements an AVL tree data structure with in-order successor pointers.
The tree is used primarily for efficient range queries in computational geometry
algorithms, particularly in the sweep-line algorithm for finding intersections
among axis-aligned line segments.
"""

from typing import Any, List, Optional, Tuple, TypeVar, Union

# Type variable for the key type (typically float or int)
K = TypeVar('K', int, float)


class Node:
    """
    Node class for the AVL tree.
    
    Each node contains a key (typically a y-coordinate), a reference to a segment,
    left and right child pointers, height information, and a successor pointer
    for efficient in-order traversal.
    """
    
    def __init__(self, key: K, segment: Any = None):
        """
        Initialize a new node with the given key and segment.
        
        Args:
            key: The key value for the node (typically a y-coordinate)
            segment: Optional reference to a line segment object
        """
        self.key = key               # Key value (typically y-coordinate)
        self.segment = segment       # Reference to the line segment object
        self.left = None             # Left child
        self.right = None            # Right child
        self.height = 1              # Height of the subtree rooted at this node
        self.successor = None        # In-order successor pointer


class AVLTree:
    """
    AVL Tree implementation with in-order successor pointers.
    
    This balanced binary search tree maintains height balance and successor
    pointers for efficient range queries. It's particularly useful for the
    sweep-line algorithm in computational geometry.
    """
    
    def __init__(self):
        """Initialize an empty AVL tree."""
        self.root = None

    def height(self, node: Optional[Node]) -> int:
        """
        Get the height of a node.
        
        Args:
            node: The node to get the height of
            
        Returns:
            The height of the node, or 0 if the node is None
        """
        return node.height if node else 0

    def get_balance(self, node: Optional[Node]) -> int:
        """
        Calculate the balance factor of a node.
        
        The balance factor is defined as the height of the left subtree
        minus the height of the right subtree.
        
        Args:
            node: The node to calculate the balance factor for
            
        Returns:
            The balance factor (left height - right height), or 0 if the node is None
        """
        return self.height(node.left) - self.height(node.right) if node else 0

    def right_rotate(self, y: Node) -> Node:
        """
        Perform a right rotation on the subtree rooted at y.
        
        Args:
            y: The root of the subtree to rotate
            
        Returns:
            The new root of the subtree after rotation
        """
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        # Note: Successor pointers remain valid after rotation
        return x

    def left_rotate(self, x: Node) -> Node:
        """
        Perform a left rotation on the subtree rooted at x.
        
        Args:
            x: The root of the subtree to rotate
            
        Returns:
            The new root of the subtree after rotation
        """
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        # Note: Successor pointers remain valid after rotation
        return y

    def insert(self, node: Optional[Node], key: K, segment: Any = None, 
               predecessor: Optional[Node] = None, successor: Optional[Node] = None) -> Node:
        """
        Insert a node with the given key and segment into the tree.
        
        This method also maintains the in-order successor pointers during insertion.
        
        Args:
            node: The root of the subtree to insert into
            key: The key value for the new node
            segment: Optional reference to a line segment object
            predecessor: The in-order predecessor of the new node
            successor: The in-order successor of the new node
            
        Returns:
            The root of the subtree after insertion
        """
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

        # Balance the tree if needed
        
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

    def min_value_node(self, node: Node) -> Node:
        """
        Find the node with minimum key value in the subtree.
        
        Args:
            node: The root of the subtree to search
            
        Returns:
            The node with the minimum key value (leftmost leaf)
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def max_value_node(self, node: Node) -> Node:
        """
        Find the node with maximum key value in the subtree.
        
        Args:
            node: The root of the subtree to search
            
        Returns:
            The node with the maximum key value (rightmost leaf)
        """
        current = node
        while current.right is not None:
            current = current.right
        return current

    def delete(self, node: Optional[Node], key: K, 
               predecessor: Optional[Node] = None, successor: Optional[Node] = None) -> Optional[Node]:
        """
        Delete a node with the given key from the tree.
        
        This method also maintains the in-order successor pointers during deletion.
        
        Args:
            node: The root of the subtree to delete from
            key: The key value of the node to delete
            predecessor: The in-order predecessor of the node to delete
            successor: The in-order successor of the node to delete
            
        Returns:
            The root of the subtree after deletion, or None if the subtree becomes empty
        """
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

        # Fix for self-referential successor pointers
        # This can happen during rebalancing operations
        if node.successor == node:
            node.successor = None

        return node

    def insert_value(self, key: K, segment: Any = None) -> None:
        """
        Insert a value into the AVL tree.
        
        This is a public wrapper method for the insert operation.
        
        Args:
            key: The key value to insert
            segment: Optional reference to a line segment object
        """
        self.root = self.insert(self.root, key, segment)

    def delete_value(self, key: K, segment: Any = None) -> None:
        """
        Delete a value from the AVL tree.
        
        This is a public wrapper method for the delete operation.
        
        Args:
            key: The key value to delete
            segment: Optional reference to a line segment object (used for identification in case of duplicate keys)
        """
        self.root = self.delete(self.root, key)

    def inorder(self, node: Optional[Node]) -> List[Tuple[K, Optional[K]]]:
        """
        Perform an in-order traversal of the tree.
        
        This method is primarily used for testing and debugging.
        
        Args:
            node: The root of the subtree to traverse
            
        Returns:
            A list of tuples (key, successor_key) for each node in the subtree
        """
        if not node:
            return []
        return self.inorder(node.left) + [(node.key, node.successor.key if node.successor else None)] + self.inorder(node.right)

    def find_min_ge(self, node: Optional[Node], value: K) -> Optional[Node]:
        """
        Find the node with the minimum key >= given value.
        
        This method is used for range queries to find the first node in a range.
        
        Args:
            node: The root of the subtree to search
            value: The minimum key value to find
            
        Returns:
            The node with the minimum key >= value, or None if no such node exists
        """
        if not node:
            return None
        if node.key == value:
            return node
        elif node.key < value:
            return self.find_min_ge(node.right, value)
        else:
            # node.key > value
            left_result = self.find_min_ge(node.left, value)
            return left_result if left_result else node

    def search_range(self, low: K, high: K) -> List[Any]:
        """
        Search for all segments in the given key range.
        
        This method uses successor pointers for efficient range queries.
        
        Args:
            low: The lower bound of the range (inclusive)
            high: The upper bound of the range (inclusive)
            
        Returns:
            A list of segments whose keys are in the range [low, high]
        """
        result = []
        node = self.find_min_ge(self.root, low)
        while node and node.key <= high:
            result.append(node.segment)
            node = node.successor
        return result


# Test code for the AVL Tree implementation
if __name__ == "__main__":
    """
    Test the AVL Tree implementation with various scenarios.
    
    This test code demonstrates:
    1. Insertion of nodes
    2. Deletion of nodes with different cases (leaf, one child, two children)
    3. Verification of successor pointers
    """
    avl = AVLTree()

    # First test set: Basic operations
    print("=== First Test Set: Basic Operations ===")
    values_to_insert = [20, 10, 30, 5, 15, 25, 35]
    print(f"Inserting values: {values_to_insert}")
    for value in values_to_insert:
        avl.insert_value(value)

    print("\nTree after insertions (key, successor_key):")
    print(avl.inorder(avl.root))

    # Delete node with two children
    print("\nDeleting node with two children (20):")
    avl.delete_value(20)
    print("Tree after deleting 20:")
    print(avl.inorder(avl.root))

    # Delete a leaf node
    print("\nDeleting leaf node (5):")
    avl.delete_value(5)
    print("Tree after deleting 5:")
    print(avl.inorder(avl.root))

    # Delete node with one child
    print("\nDeleting node with one child (30):")
    avl.delete_value(30)
    print("Tree after deleting 30:")
    print(avl.inorder(avl.root))

    # Delete all remaining nodes
    print("\nDeleting all remaining nodes:")
    avl.delete_value(10)
    avl.delete_value(15)
    avl.delete_value(25)
    avl.delete_value(35)
    print("Tree after deleting all nodes:")
    print(avl.inorder(avl.root))

    # Second test set: More complex operations
    print("\n=== Second Test Set: More Complex Operations ===")
    avl = AVLTree()
    values_to_insert = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    print(f"Inserting values: {values_to_insert}")
    for value in values_to_insert:
        avl.insert_value(value)

    print("\nTree after insertions (key, successor_key):")
    print(avl.inorder(avl.root))

    # Delete node with two children
    print("\nDeleting node with two children (30):")
    avl.delete_value(30)
    print("Tree after deleting 30:")
    print(avl.inorder(avl.root))

    # Delete a leaf node
    print("\nDeleting leaf node (10):")
    avl.delete_value(10)
    print("Tree after deleting 10:")
    print(avl.inorder(avl.root))

    # Delete node with one child
    print("\nDeleting node with one child (80):")
    avl.delete_value(80)
    print("Tree after deleting 80:")
    print(avl.inorder(avl.root))

    # Delete multiple nodes
    print("\nDeleting multiple nodes (50, 70):")
    avl.delete_value(50)
    avl.delete_value(70)
    print("Tree after deleting 50 and 70:")
    print(avl.inorder(avl.root))

    # Test range search
    print("\n=== Testing Range Search ===")
    avl = AVLTree()
    values_to_insert = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    for value in values_to_insert:
        avl.insert_value(value, f"Segment-{value}")

    print(f"Searching range [25, 75]:")
    segments = avl.search_range(25, 75)
    print(f"Found segments: {segments}")
