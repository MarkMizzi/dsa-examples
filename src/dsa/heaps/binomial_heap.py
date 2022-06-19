"""
Implementation of a binomial heap data structure.

Operation    | Running time
-------------|---------------------
minimum      | O(log n) worst case
union        | O(log max(n1, n2))
insert       | O(log n)
extract_min  | O(log n)
decrease_key | O(log n) worst case
remove       | O(log n)

Doctests:

>>> x = BinomialHeap()
>>> vals = [83, 38, 27, 29, 98, 93, 67, 85, 5, 76, 88, 9]
>>> for i in vals:
...    x.insert(i)
...
>>> x
BinomialHeap(None, None, _BinomialTree(5, 9, 88, 76), _BinomialTree(27, 67, 93, 98, 85, 38, 83, 29))

"""


class BinomialHeap:
    """Implementation of a binomial heap.

    The key is the value stored in the node.
    """

    class _BinomialTree:
        """Implementation of binomial trees used by heap.

        Uses leftmost child - next sibling representation.
        """
        def __init__(self, x, lchild=None, rsib=None, parent=None):
            """Constructor, client code should use directly only for 0th order tree"""
            self.x = x
            self.lchild = lchild
            self.rsib = rsib
            self.parent = parent

        def merge(self, other):
            """Merge two p-order binomial trees into one p+1 binomial tree.

            Constant time, simply links the roots of self and other together.
            Assumes self and other have same order.
            min-heap property is conserved.
            """
            if self.x < other.x: # self is the new root.
                other.parent = self
                other.rsib = self.lchild
                self.lchild = other
                return self
            else: # other is the new root
                self.parent = other
                self.rsib = other.lchild
                other.lchild = self
                return other

        def split(self):
            """Split a tree of order p into p trees of order 0,..., p-1 by removing the root.

            This is useful for the extract_min operation.
            """

            if self.lchild is None:
                return self.x, []

            trees = [ self.lchild ]
            while trees[-1].rsib is not None:
                trees.append(trees[-1].rsib)

            for t in trees:
                t.parent = None

            return self.x, trees

        def __iter__(self):
            yield self.x
            if self.lchild is not None:
                yield from iter(self.lchild)
            if self.rsib is not None:
                yield from iter(self.rsib)

        def __repr__(self):
            return f'{type(self).__name__}{tuple(iter(self))}'

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

    @staticmethod
    def _safe_merge(t1, t2, i):
        """Safely merge two binomial trees (with None checks)

        Returns i+1 if a merge occurs, i otherwise.
        """
        if t1 is None:
            return i, t2
        if t2 is None:
            return i, t1
        return i+1, t1.merge(t2)

    def __init__(self, trees=None):
        """Binomial trees are kept in sorted order from lowest order to highest."""
        if trees is None:
            self._trees = []
        else:
            self._trees = trees

    def minimum(self):
        """Return the minimum element in the heap.

        Since each binomial tree has the min-heap property, the minimum element must be
            one of the roots.
        """

        # filter None trees
        trees = filter(lambda x: x is not None, self._trees)
        return min(trees, key=lambda t: t.x).x

    def union(self, other):
        """Heap merge operation. Most other heap operations use this.

        The method is fairly straightforward.
        Each of the same order binomial trees in self and other are merged into
            a higher order tree in the result.
        If one heap (or both) do not have a tree for some order, the other heap's
            tree is copied directly.
        Note that merging creates a higher order tree, but copying does not.
        So copied trees must be merged with higher order trees
            created by previous iterations.
        """
        n_trees = max(len(self._trees), len(other._trees)) + 1
        trees = [ None ] * n_trees # binomial trees for the new heap.

        min_trees = min(len(self._trees), len(other._trees))

        for i in range(min_trees):
            j, tree = self._safe_merge(self._trees[i], other._trees[i], i)
            # merge with trees[i] if last merge failed.
            # Otherwise will always merge with None,
            #   since trees[i+1] has not yet been filled.
            k, tree = self._safe_merge(tree, trees[j], j)
            trees[j] = None # if last merge succeeds, removes leftover lower order tree.
            trees[k] = tree

        for i in range(min_trees, len(self._trees)):
            # _safe_merge only matters for trees[len(other._trees)].
            j, tree = self._safe_merge(trees[i], self._trees[i], i)
            trees[i] = None # if merge succeeds, removes leftover lower order tree.
            trees[j] = tree
            i = j

        for i in range(min_trees, len(other._trees)):
            j, tree = self._safe_merge(trees[i], other._trees[i], i)
            trees[i] = None # if merge succeeds, removes leftover lower order tree.
            trees[j] = tree

        if trees[-1] is None:
            trees.pop()

        self._trees = trees

    def insert(self, x):
        """Insert x into the heap."""

        n_heap = type(self)([ self._BinomialTree(x) ])
        self.union(n_heap)

    def extract_min(self):
        """Extract the minimum element from the heap.

        When the root of a binomial tree of order p is removed, this creates
            p trees of order 0, ..., p-1 (see _BinomialTree.split()).
        These are used to build a new heap, which is re-merged with the old one.
        """

        min_i, min_t = 0, self._trees[0]
        for i, t in enumerate(self._trees):
            if t is None:
                pass
            elif min_t is None:
                min_i, min_t = i, t
            elif t.x < min_t.x:
                min_i, min_t = i, t

        # split the tree containing minimum element
        min_elem, n_trees = self._trees[min_i].split()
        self._trees[min_i] = None # remove the split tree.

        # create a new heap from the tree fragments, recombine with this one.
        n_heap = type(self)(n_trees)
        self.union(n_heap)

        return min_elem

    @classmethod
    def decrease_key(cls, node, x):
        """Decrease the key contained in node to x.

        This assumes that the client code has a pointer into a tree in the heap (node).
        Not great for encapsulation, but only efficient way to support this operation.
        """

        return cls._BinomialTree.decrease_key(node, x)

    def remove(self, node):
        """Removes node from the heap.

        This assumes that the client code has a pointer into a tree in the heap (node).
        Not great for encapsulation, but only efficient way to support this operation.
        Note also that this operation is only supported for heaps storing numerical types.

        The node's value is decreased to one less than the minimum value in the heap using
            decrease_key().
        It is then extracted from the heap using extract_min().
        """

        type(self).decrease_key(node, self.minimum()-1)
        self.extract_min()

    def __repr__(self):
        return f'{type(self).__name__}{tuple(self._trees)}'
