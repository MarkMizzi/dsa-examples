"""Implementation of insertion sort."""

def insertionsort(xs):
    """Sorts the list xs in place using the insertion sort algorithm.

    Insertion sort scans the input list.
    For each item, it moves that item down in the list until it is greater than
        its predecessor.
    """

    for i, _ in enumerate(xs[1:]):
        j = i
        while j > 0 and xs[j] < xs[j-1]:
            xs[j], xs[j-1] = xs[j-1], xs[j]
