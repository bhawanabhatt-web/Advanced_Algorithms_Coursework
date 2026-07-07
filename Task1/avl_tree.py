from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
V = TypeVar("V")
__all__ = ["AVLTree"]
@dataclass
class _AVLNode(Generic[V]):
    key: int
    value: V
    left: Optional["_AVLNode[V]"] = None
    right: Optional["_AVLNode[V]"] = None
    height: int = 1


class AVLTree(Generic[V]):
    

    def __init__(self) -> None:
        self._root: Optional[_AVLNode[V]] = None
        self._size: int = 0

    def __len__(self) -> int:
        """Return the number of key-value pairs currently stored."""
        return self._size

    def __contains__(self, key: int) -> bool:
        """Return ``True`` if ``key`` exists in the tree."""
        return self._find_node(key) is not None

    def insert(self, key: int, value: V) -> None:
       
        self._root = self._insert(self._root, key, value)

    def search(self, key: int) -> Optional[V]:
       
        node = self._find_node(key)
        return node.value if node is not None else None

    def delete(self, key: int) -> bool:
        
        self._root, deleted = self._delete(self._root, key)
        if deleted:
            self._size -= 1
        return deleted

    def height(self) -> int:
        """Return the height of the tree (``-1`` for an empty tree)."""
        return self._node_height(self._root) - 1

    # -- internal helpers ---------------------------------------------

    def _find_node(self, key: int) -> Optional[_AVLNode[V]]:
        """Locate the node storing ``key``, or ``None`` if absent."""
        node = self._root
        while node is not None:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    @staticmethod
    def _node_height(node: Optional[_AVLNode[V]]) -> int:
        """Return ``node.height``, or ``0`` for ``None`` (an empty subtree)."""
        return node.height if node is not None else 0

    @classmethod
    def _balance_factor(cls, node: Optional[_AVLNode[V]]) -> int:
        """Return ``height(left) - height(right)`` for ``node``."""
        if node is None:
            return 0
        return cls._node_height(node.left) - cls._node_height(node.right)

    @classmethod
    def _update_height(cls, node: _AVLNode[V]) -> None:
        """Recompute ``node.height`` from its children's heights."""
        node.height = 1 + max(cls._node_height(node.left), cls._node_height(node.right))

    @classmethod
    def _rotate_right(cls, y: _AVLNode[V]) -> _AVLNode[V]:
        """Perform a single right rotation around ``y`` and return the new subtree root."""
        x = y.left
        assert x is not None  # guaranteed by the caller's balance check
        y.left = x.right
        x.right = y
        cls._update_height(y)
        cls._update_height(x)
        return x

    @classmethod
    def _rotate_left(cls, x: _AVLNode[V]) -> _AVLNode[V]:
        """Perform a single left rotation around ``x`` and return the new subtree root."""
        y = x.right
        assert y is not None  # guaranteed by the caller's balance check
        x.right = y.left
        y.left = x
        cls._update_height(x)
        cls._update_height(y)
        return y

    @classmethod
    def _rebalance(cls, node: _AVLNode[V]) -> _AVLNode[V]:
        """Restore the AVL invariant at ``node`` via the appropriate rotation(s)."""
        cls._update_height(node)
        balance = cls._balance_factor(node)

        if balance > 1:
            if cls._balance_factor(node.left) < 0:
                node.left = cls._rotate_left(node.left)  # left-right case
            return cls._rotate_right(node)

        if balance < -1:
            if cls._balance_factor(node.right) > 0:
                node.right = cls._rotate_right(node.right)  # right-left case
            return cls._rotate_left(node)

        return node

    def _insert(self, node: Optional[_AVLNode[V]], key: int, value: V) -> _AVLNode[V]:
        """Recursively insert ``(key, value)`` into the subtree rooted at ``node``."""
        if node is None:
            self._size += 1
            return _AVLNode(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value  # overwrite existing key
            return node

        return self._rebalance(node)

    @classmethod
    def _delete(
        cls, node: Optional[_AVLNode[V]], key: int
    ) -> tuple[Optional[_AVLNode[V]], bool]:
        """Recursively delete ``key`` from the subtree rooted at ``node``.

        Returns:
            A tuple of ``(new_subtree_root, was_deleted)``.
        """
        if node is None:
            return None, False

        if key < node.key:
            node.left, deleted = cls._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = cls._delete(node.right, key)
        else:
            deleted = True
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key, node.value = successor.key, successor.value
            node.right, _ = cls._delete(node.right, successor.key)

        return cls._rebalance(node), deleted