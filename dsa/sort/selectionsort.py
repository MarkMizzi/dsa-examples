"""Implementation of the selection sort algorithm."""

def selectionsort(xs):
    """Sorts the list xs in place using the selection sort algorithm.

    Selection sort maintains a sorted sublist at the start of the input list,
        which grows by 1 element on each iteration.
    At each iteration, the minimum element in the unsorted sublist is found,
        and swapped with the element just after the sorted sublist
        (which hence grows by one element).
    """

    for i, _ in enumerate(xs[:-1]):
        # find index of minimum element.
        min_i = min(range(i, len(xs)), key=lambda i: xs[i])
        xs[i], xs[min_i] = xs[min_i], xs[i]
