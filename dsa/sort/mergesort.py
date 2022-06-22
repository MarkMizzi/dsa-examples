"""Implementation of the mergesort algorithm."""

def merge(xs, ys):
    """Merges two sorted lists xs and ys into a third sorted list, returning the result."""

    zs = []
    i, j = 0, 0

    while i < len(xs) and j < len(ys):
        if xs[i] < ys[j]:
            zs.append(xs[i])
            i += 1
        else:
            zs.append(ys[j])
            j += 1

    # add remaining elements in xs to zs
    zs += xs[i:]

    # add remaining elements in ys to zs
    zs += ys[j:]

    return zs


def mergesort(xs):
    """Sorts the list xs using the mergesort algorithm, returning the result.

    Mergesort recursively sorts the left and right halves of the input list.
    These are then merged into another sorted list using the merge algorithm.
    Base cases occur when the list is empty or a singleton,
        in these two cases it is already sorted.
    """

    if len(xs) <= 1:
        return xs

    mid = len(xs) // 2

    return merge(
        mergesort(xs[:mid]),
        mergesort(xs[mid:])
    )
