"""
Tests for the AVL Tree implementation.

This module contains tests for the AVL tree data structure used in the
sweep-line algorithm for finding intersections among line segments.
"""

import sys
import os
import unittest
from typing import List, Optional, Tuple

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the AVL tree implementation
from src.AVL_tree import AVLTree, Node


class TestAVLTree(unittest.TestCase):
    """Test cases for the AVL tree implementation."""

    def setUp(self):
        """Set up a new AVL tree for each test."""
        self.tree = AVLTree()

    def test_empty_tree(self):
        """Test that a new tree is empty."""
        self.assertIsNone(self.tree.root)

    def test_insert_single_value(self):
        """Test inserting a single value into the tree."""
        self.tree.insert_value(10)
        self.assertIsNotNone(self.tree.root)
        self.assertEqual(self.tree.root.key, 10)
        self.assertEqual(self.tree.root.height, 1)

    def test_insert_multiple_values(self):
        """Test inserting multiple values into the tree."""
        values = [10, 20, 30, 40, 50]
        for value in values:
            self.tree.insert_value(value)
        
        # Check that all values are in the tree
        inorder_traversal = [node[0] for node in self.tree.inorder(self.tree.root)]
        self.assertEqual(sorted(values), inorder_traversal)

    def test_tree_balancing_left_left(self):
        """Test tree balancing for left-left case."""
        # Insert values that would cause a left-left imbalance
        self.tree.insert_value(30)
        self.tree.insert_value(20)
        self.tree.insert_value(10)
        
        # After balancing, the root should be 20
        self.assertEqual(self.tree.root.key, 20)
        self.assertEqual(self.tree.root.left.key, 10)
        self.assertEqual(self.tree.root.right.key, 30)

    def test_tree_balancing_right_right(self):
        """Test tree balancing for right-right case."""
        # Insert values that would cause a right-right imbalance
        self.tree.insert_value(10)
        self.tree.insert_value(20)
        self.tree.insert_value(30)
        
        # After balancing, the root should be 20
        self.assertEqual(self.tree.root.key, 20)
        self.assertEqual(self.tree.root.left.key, 10)
        self.assertEqual(self.tree.root.right.key, 30)

    def test_tree_balancing_left_right(self):
        """Test tree balancing for left-right case."""
        # Insert values that would cause a left-right imbalance
        self.tree.insert_value(30)
        self.tree.insert_value(10)
        self.tree.insert_value(20)
        
        # After balancing, the root should be 20
        self.assertEqual(self.tree.root.key, 20)
        self.assertEqual(self.tree.root.left.key, 10)
        self.assertEqual(self.tree.root.right.key, 30)

    def test_tree_balancing_right_left(self):
        """Test tree balancing for right-left case."""
        # Insert values that would cause a right-left imbalance
        self.tree.insert_value(10)
        self.tree.insert_value(30)
        self.tree.insert_value(20)
        
        # After balancing, the root should be 20
        self.assertEqual(self.tree.root.key, 20)
        self.assertEqual(self.tree.root.left.key, 10)
        self.assertEqual(self.tree.root.right.key, 30)

    def test_delete_leaf_node(self):
        """Test deleting a leaf node."""
        # Insert some values
        values = [10, 20, 30]
        for value in values:
            self.tree.insert_value(value)
        
        # Delete a leaf node
        self.tree.delete_value(30)
        
        # Check that the node was deleted
        inorder_traversal = [node[0] for node in self.tree.inorder(self.tree.root)]
        self.assertEqual([10, 20], inorder_traversal)

    def test_delete_node_with_one_child(self):
        """Test deleting a node with one child."""
        # Insert some values
        self.tree.insert_value(20)
        self.tree.insert_value(10)
        self.tree.insert_value(5)
        
        # Delete a node with one child
        self.tree.delete_value(10)
        
        # Check that the node was deleted and the tree is still valid
        self.assertEqual(self.tree.root.key, 20)
        self.assertEqual(self.tree.root.left.key, 5)

    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children."""
        # Insert some values
        values = [20, 10, 30, 5, 15, 25, 35]
        for value in values:
            self.tree.insert_value(value)
        
        # Delete a node with two children
        self.tree.delete_value(20)
        
        # Check that the node was deleted and the tree is still valid
        inorder_traversal = [node[0] for node in self.tree.inorder(self.tree.root)]
        self.assertEqual([5, 10, 15, 25, 30, 35], inorder_traversal)

    def test_delete_root(self):
        """Test deleting the root node."""
        # Insert some values
        values = [20, 10, 30]
        for value in values:
            self.tree.insert_value(value)
        
        # Delete the root
        self.tree.delete_value(20)
        
        # Check that the root was deleted and the tree is still valid
        inorder_traversal = [node[0] for node in self.tree.inorder(self.tree.root)]
        self.assertEqual([10, 30], inorder_traversal)

    def test_successor_pointers(self):
        """Test that successor pointers are correctly maintained."""
        # Insert some values
        values = [20, 10, 30, 5, 15, 25, 35]
        for value in values:
            self.tree.insert_value(value)
        
        # Check successor pointers through inorder traversal
        inorder_with_successors = self.tree.inorder(self.tree.root)
        
        # Expected successors: 5->10, 10->15, 15->20, 20->25, 25->30, 30->35, 35->None
        expected_successors = [(5, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, None)]
        
        self.assertEqual(expected_successors, inorder_with_successors)

    def test_find_min_ge(self):
        """Test finding the node with the minimum key >= a given value."""
        # This test requires the find_min_ge method to be public
        # If it's not, you may need to modify the AVL tree implementation
        
        # Insert some values
        values = [10, 20, 30, 40, 50]
        for value in values:
            self.tree.insert_value(value)
        
        # Test finding nodes
        if hasattr(self.tree, 'find_min_ge'):
            node = self.tree.find_min_ge(self.tree.root, 25)
            self.assertEqual(node.key, 30)
            
            node = self.tree.find_min_ge(self.tree.root, 10)
            self.assertEqual(node.key, 10)
            
            node = self.tree.find_min_ge(self.tree.root, 60)
            self.assertIsNone(node)

    def test_search_range(self):
        """Test searching for values in a range."""
        # This test requires the search_range method to be public
        # If it's not, you may need to modify the AVL tree implementation
        
        # Insert some values with segments
        values = [(10, "Segment-10"), (20, "Segment-20"), (30, "Segment-30"), 
                  (40, "Segment-40"), (50, "Segment-50")]
        for key, segment in values:
            self.tree.insert_value(key, segment)
        
        # Test range search
        if hasattr(self.tree, 'search_range'):
            # Search for values in range [15, 45]
            results = self.tree.search_range(15, 45)
            expected = ["Segment-20", "Segment-30", "Segment-40"]
            self.assertEqual(expected, results)
            
            # Search for values in range [10, 10]
            results = self.tree.search_range(10, 10)
            expected = ["Segment-10"]
            self.assertEqual(expected, results)
            
            # Search for values in range [60, 70]
            results = self.tree.search_range(60, 70)
            expected = []
            self.assertEqual(expected, results)


if __name__ == '__main__':
    unittest.main()
