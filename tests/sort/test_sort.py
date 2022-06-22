import random
import sys

from dsa.sort.bubblesort import bubblesort
from dsa.sort.insertionsort import insertionsort
from dsa.sort.selectionsort import selectionsort

from dsa.sort.mergesort import mergesort


def is_sorted(xs) -> bool:
    """Check if the given list xs is sorted"""

    for i, x in enumerate(xs[:-1]):
        if x > xs[i+1]:
            return False
    return True


for inplace_sort in [ bubblesort, insertionsort, selectionsort ]:
    def test_sort():
        """Test an inplace sort using randomly generated lists of several different sizes."""

        # minimum and maximum elements in randomly generated list.
        MIN, MAX = -10000, 10000
        for size in [0, 1, 5, 10, 20, 40, 100, 1000, 2000, 5000]:
            xs = random.sample(range(MIN, MAX), size)
            inplace_sort(xs)
            assert is_sorted(xs)

    # monkey patch test function into the module
    setattr(sys.modules[__name__], f'test_{inplace_sort.__name__}', test_sort)


for pure_sort in [ mergesort ]:
    def test_sort():
        """Test a pure sort using randomly generated lists of several different sizes."""

        # minimum and maximum elements in randomly generated list.
        MIN, MAX = -10000, 10000
        for size in [0, 1, 5, 10, 20, 40, 100, 1000, 2000, 5000]:
            xs = random.sample(range(MIN, MAX), size)
            assert is_sorted(pure_sort(xs))

    # monkey patch test function into module
    setattr(sys.modules[__name__], f'test_{pure_sort.__name__}', test_sort)
