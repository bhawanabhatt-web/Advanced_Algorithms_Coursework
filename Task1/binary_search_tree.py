from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

V = TypeVar("V")

__all__ = ["BinarySearchTree"]


@dataclass
class _BSTNode(Generic[V]):
    key: int
    value: V
    left: Optional["_BSTNode[V]"] = None
    right: Optional["_BSTNode[V]"] = None

class BinarySearchTree(Generic[V]):

    def __init__(self) -> None:
        self._root: Optional[_BSTNode[V]] = None
        self._size: int = 0

    def __len__(self) -> int:
        """Return the number of key-value pairs currently stored."""
        return self._size

    def __contains__(self, key: int) -> bool:
        """Return ``True`` if ``key`` exists in the tree."""
        return self._find_node(key) is not None

    def insert(self, key: int, value: V) -> None:
        
        if self._root is None:
            self._root = _BSTNode(key, value)
            self._size += 1
            return

        node = self._root
        while True:
            if key < node.key:
                if node.left is None:
                    node.left = _BSTNode(key, value)
                    self._size += 1
                    return
                node = node.left
            elif key > node.key:
                if node.right is None:
                    node.right = _BSTNode(key, value)
                    self._size += 1
                    return
                node = node.right
            else:
                node.value = value  # overwrite existing key
                return

    def search(self, key: int) -> Optional[V]:
        """Look up the value stored under ``key``.

        Args:
            key: The key to search for.

        Returns:
            The associated value, or ``None`` if ``key`` is not present.
        """
        node = self._find_node(key)
        return node.value if node is not None else None

    def delete(self, key: int) -> bool:
        """Remove ``key`` (and its value) from the tree, if present.

        Args:
            key: The key to remove.

        Returns:
            ``True`` if a node was removed, ``False`` if ``key`` was not
            found.
        """
        self._root, deleted = self._delete(self._root, key)
        if deleted:
            self._size -= 1
        return deleted

    def height(self) -> int:
        """Return the height of the tree (``-1`` for an empty tree).

        Returns:
            The number of edges on the longest path from the root to a
            leaf. A single-node tree has height ``0``.
        """
        return self._height(self._root)

    def _find_node(self, key: int) -> Optional[_BSTNode[V]]:
        """Locate the node storing ``key``, or ``None`` if absent."""
        node = self._root
        while node is not None:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    @classmethod
    def _delete(
        cls, node: Optional[_BSTNode[V]], key: int
    ) -> tuple[Optional[_BSTNode[V]], bool]:
        """Recursively delete ``key`` from the subtree rooted at ``node``.

        Returns:
            A tuple of ``(new_subtree_root, was_deleted)``.
        """
        if node is None:
            return None, False
        if key < node.key:
            node.left, deleted = cls._delete(node.left, key)
            return node, deleted
        if key > node.key:
            node.right, deleted = cls._delete(node.right, key)
            return node, deleted

        # `node` is the target: handle the three classic BST deletion cases.
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True

        successor = node.right
        while successor.left is not None:
            successor = successor.left
        node.key, node.value = successor.key, successor.value
        node.right, _ = cls._delete(node.right, successor.key)
        return node, True

    @classmethod
    def _height(cls, node: Optional[_BSTNode[V]]) -> int:
        """Recursively compute the height of the subtree rooted at ``node``."""
        if node is None:
            return -1
        return 1 + max(cls._height(node.left), cls._height(node.right))