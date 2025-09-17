class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Insert a key into the BST."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key):
        """Search for a key in the BST."""
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def inorder(self):
        """In-order traversal (Left, Root, Right)"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def delete(self, key):
        """Delete a key from the BST."""
        self.root = self._delete(self.root, key)

    def _delete(self, node: Node, key):
        if not node:
            return None

        if node.key < key:
            node.left = self._delete(node, key)
        elif node.key > key:
            node.right = self._delete(node, key)
        else:

            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # get the min value ndoe from the right or max value from left
            min_value_node = self._min_value_node(node.right)
            node.key = min_value_node.key
            node.right = self._delete(node.right, min_value_node.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def min_value(self):
        """Return the minimum value in the BST."""
        current = self.root
        while current and current.left:
            current = current.left
        return current.key if current else None

    def max_value(self):
        """Return the maximum value in the BST."""
        current = self.root
        while current and current.right:
            current = current.right
        return current.key if current else None
