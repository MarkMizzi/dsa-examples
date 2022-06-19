"""
Implementation of a binary heap.

Operation    | Running time
-------------|---------------------
minimum      | O(1)
insert       | O(log n) worst case
extract_min  | O(log n) worst case

Doctests:

"""


from collections import UserList


class BinaryHeap(UserList):
        """Implementation of a binary heap.

        The key is the value itself.
        """

        @staticmethod
        def parent(i: int) -> int:
		return -1 if i == 0 else (i-1)//2

        @staticmethod
        def left(i: int) -> int:
                return 2*i + 1

        @staticmethod
        def right(i: int) -> int:
                return 2*i + 2

        def __init__(self):
                """Creates an empty heap."""
                super().__init__()

        def minimum(self):
                """Return minimum element in the heap."""
                return self[0]

        def __bubble_up(self):
                """Fixup after insertion.

                After an insertion, the last element may violate the min-heap property.
                This function repeatedly swaps the last element with its parent
                        until its value is >= its parent's value.
                """
                i = len(self)-1
                parent_i = self.parent(i)
                while parent_i >= 0 and self[i] < self[parent_i]:
                        self[i], self[parent_i] = self[parent_i], self[i]
                        i, parent_i = parent_i, self.parent(parent_i)

        def insert(self, x):
                """Insert an element x into the heap."""
                self.append(x)
                self.__bubble_up() # fixup

        def __trickle_down(self):
                """Fixup after min_extract.

                min_extract places the last element at the beginning of the array.
                This violates the min-heap property, since last element is
                        (almost) never the smallest.
                So this function repeatedly swaps the first element with the
                        smallest of its children until the min-heap property is restored, i.e.
                        until the element is smaller than both of its children.
                """
                i = 0
                l, r = self.left(i), self.right(i)
                l, r = l if l < len(self) else i, r if r < len(self) else i # boundary check
                # find index of smallest node out of these 3
                min_i = min(i, l, r, key=lambda i: self[i])
                while min_i != i:
                        # swap element with its smallest child
                        self[i], self[min_i] = self[min_i], self[i]
                        i = min_i
                        l, r = self.left(i), self.right(i)
                        l, r = l if l < len(self) else i, r if r < len(self) else i # boundary check
                        min_i = min(i, l, r, key=lambda i: self[i])

        def extract_min(self):
                """Remove and return the minimum element in the heap."""
                min_elem = self[0]
                # replace first element with last one
                self[0] = self[-1]
                self.pop()
                self.__trickle_down() # fixup
                return min_elem

        def __repr__(self):
                return f'{type(self).__name__}({super().__repr__()})'
