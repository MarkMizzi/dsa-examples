"""Tests for dsa.heaps.binary_heap.BinaryHeap."""

import random

from dsa.heaps.binary_heap import BinaryHeap


def random_heap(minimum: int, maximum: int, n: int):
    """Return a random heap with n elements in the range [minimum, maximum]."""

    vals = random.sample(range(minimum, maximum), n)

    x = BinaryHeap()
    for i in vals:
        x.insert(i)
    return x, vals


def check_min_heap_property(heap: BinaryHeap, i: int=0) -> bool:
    """Asserts that the given binary heap has the min heap property"""

    l, r = heap.left(i), heap.right(i)
    l, r = l if l < len(heap) else i, r if r < len(heap) else i

    return (min(heap[i], heap[l], heap[r]) == heap[i]
            and (check_min_heap_property(heap, l) if l != i else True)
            and check_min_heap_property(heap, r) if r != i else True)


def test_minimum():
    x, vals = random_heap(-1000, 1000, 500)
    assert x.minimum() == min(*vals)


def test_insert():
    x, vals = random_heap(-1000, 1000, 500)

    assert check_min_heap_property(x)
    for i in vals:
        assert i in x


def test_extract_min():
    x, _ = random_heap(-1000, 1000, 500)

    while len(x) > 0:
        minimum = x.minimum()
        assert minimum == x.extract_min()
