"""Implementation of the bubblesort algorithm"""


def bubblesort(xs):
    """Sorts the input list xs in place using the bubblesort algorithm.

    Bubblesort works by passing over the list, moving elements up one position
        until they are smaller than their successor.
    Passes are repeated until no further change occurs.
    """

    swapped = True
    passes = 0
    while swapped:
        swapped = False
        for i in range(0, len(xs)-1-passes):
            if xs[i] > xs[i+1]:
                xs[i], xs[i+1] = xs[i+1], xs[i]
                swapped = True
        passes += 1
