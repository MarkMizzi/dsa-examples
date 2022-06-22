"""Tests for sorts in dsa.sort."""

from functools import partial
import random
import sys

from dsa.sort.bubblesort import bubblesort
from dsa.sort.insertionsort import insertionsort
from dsa.sort.selectionsort import selectionsort
from dsa.sort.shellsort import shellsort

from dsa.sort.mergesort import mergesort


def is_sorted(xs) -> bool:
    """Check if the given list xs is sorted"""

    for i, x in enumerate(xs[:-1]):
        if x > xs[i+1]:
            return False
    return True


def monkeypatch_inplace_sort(sort):
    """Monkey patch a test for an inplace sort into the current module."""

    def test_sort():
        """Test an inplace sort using randomly generated lists of several different sizes."""

        # minimum and maximum elements in randomly generated list.
        MIN, MAX = -10000, 10000
        for size in [0, 1, 5, 10, 20, 40, 100, 1000, 2000, 5000]:
            xs = random.sample(range(MIN, MAX), size)
            sort(xs)
            assert is_sorted(xs)

    # monkey patch test function into the module
    setattr(sys.modules[__name__], f'test_{sort.__name__}', test_sort)


def monkeypatch_pure_sort(sort):
    """Monkey patch a test for a pure sort into the current module."""

    def test_sort():
        """Test a pure sort using randomly generated lists of several different sizes."""

        # minimum and maximum elements in randomly generated list.
        MIN, MAX = -10000, 10000
        for size in [0, 1, 5, 10, 20, 40, 100, 1000, 2000, 5000]:
            xs = random.sample(range(MIN, MAX), size)
            assert is_sorted(sort(xs))

    # monkey patch test function into module
    setattr(sys.modules[__name__], f'test_{sort.__name__}', test_sort)


for inplace_sort in [ bubblesort, insertionsort, selectionsort ]:
    monkeypatch_inplace_sort(inplace_sort)


for pure_sort in [ mergesort ]:
    monkeypatch_pure_sort(pure_sort)
