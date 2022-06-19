"""
Implementation of a randomized mergeable (or meldable) heap.

Operation    | Running time
-------------|---------------------
minimum      | O(1)
union        | O(log max(n1, n2))
insert       | O(log n) worst case
extract_min  | O(log n)
decrease_key | O(log n) worst case
remove       | O(log n)

Doctests:

>>> x = RandomizedHeap()
>>> vals = [35, 96, 98, 45, 33, 79, 26, 39, 99, 20, 56, 46]
>>> for i in vals:
...    x.insert(i)
...

"""


from random import randint


class RandomizedHeap:
    """Implementation of a randomized mergeable heap.

    The key is the value stored in the node.
    """

    class _Node:
        """Node used by the heap data structure."""

        def __init__(self, x, parent=None):
            self.x = x
            self.parent = parent
            self.l, self.r = None, None

        def union(self, other):
            """Destructive, recursive union algorithm central to this heap implementation.

            This algorithm checks which of the two heaps has the smallest root,
                then recursively merges the other heap with one of its children.
            The child is chosen randomly.
            The heap with the smaller root is returned.
            This ensures that the min-heap property is conserved, since at each step,
                the subheap produced has the smallest element in both heaps as its root.

            Implementation detail: Both self and other are assumed to be not None.
            """

            flip = bool(randint(0, 1)) # randomly choose which child
            if self.x < other.x: # self has the smaller value
                if flip:
                    self.l = self.l.union(other) if self.l is not None else other
                    self.l.parent = self
                else:
                    self.r = self.r.union(other) if self.r is not None else other
                    self.r.parent = self
                return self
            else: # other has the smaller value
                if flip:
                    other.l = other.l.union(self) if other.l is not None else self
                    other.l.parent = other
                else:
                    other.r = other.r.union(self) if other.l is not None else self
                    other.r.parent = other
                return other

        @staticmethod
        def decrease_key(node, x):
            """Decrease the value stored in node to x.

            In order to restore the min-heap property, the node's value is switched with
                its parent's until the latter has a smaller value than x.
            """

            node.x = x
            while node.parent is not None and node.x < node.parent.x:
                node.x, node.parent.x = node.parent.x, node.x
                node = node.parent
        
        def __iter__(self):
            yield self.x
            if self.l is not None:
                yield from iter(self.l)
            if self.r is not None:
                yield from iter(self.r)


    def __init__(self):
        """Creates an empty heap."""

        self._root = None

    def minimum(self):
        """Return minimum element in the heap."""

        return self._root.x

    def union(self, other):
        """Add all the elements of other to self. other may be destroyed in the process."""

        if other._root is None:
            return
        if self._root is None:
            self._root = other._root
            return
        self._root = self._root.union(other._root)

    def insert(self, x):
        """Insert an element into the heap.

        A node is created containing just the new element.
        It is then included into self using the union algorithm.
        """

        if self._root is None:
            self._root = self._Node(x)
        else:
            self._root = self._root.union(self._Node(x))

    def extract_min(self):
        """Remove the minimum element from the heap.

        The two children of the root are merged together into a new heap
            using the union algorithm.
        The root node of the new heap becomes the new root of this heap.
        """

        min_element = self._root.x
        if self._root.l is None:
            self._root = self._root.r
            return min_element
        if self._root.r is None:
            self._root = self._root.l
            return min_element
        self._root = self._root.l.union(self._root.r)
        return min_element

    @classmethod
    def decrease_key(cls, node, x):
        """Decrease the key contained in node to x.

        This assumes that the client code has a pointer to a heap node.
        Not great for encapsulation, but only efficient way to support this operation.
        """

        return cls._Node.decrease_key(node, x)

    def remove(self, node):
        """Removes node from the heap.

        This assumes that the client code has a pointer to a heap node.
        Not great for encapsulation, but only efficient way to support this operation.
        Note also that this operation is only supported for heaps storing numerical types.

        The node's value is decreased to one less than the minimum value in the heap using
            decrease_key().
        It is then extracted from the heap using extract_min().
        """

        type(self).decrease_key(node, self.minimum()-1)
        self.extract_min()

    def __iter__(self):
        if self._root is None:
            return iter(())
        return iter(self._root)

    def __repr__(self):
        return f'{type(self).__name__}{tuple(self)}'
