from lab1 import quick_sort, merge_sort
from timing import timing
import random

@timing
def onsets(data, p, algorithm):
    gen = ((el[1], el[0]) for el in enumerate(data) if el[1] > p)
    elements = [next(gen) for i in range(3)]

    if algorithm.__name__ == 'quick_sort':
        algorithm(elements, 0, len(elements)-1)

    if algorithm.__name__ == 'merge_sort':
        algorithm(elements)

    return ','.join([str(x[1]) for x in elements[::-1]]) + '\n'


if __name__ == "__main__":
    test1 = ([9, 1, 1, 1, 0, 0, 0, 8, 10, 11, 14, 213232, 24324563], 2)
    test2 = (random.sample(range(100000), 100000), 95000)

    print(onsets(test1[0], test1[1], quick_sort))
    print(onsets(test1[0], test1[1], merge_sort))

    print(onsets(test2[0], test2[1], quick_sort))
    print(onsets(test2[0], test2[1], merge_sort))





