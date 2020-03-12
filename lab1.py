from timeit import default_timer as timer
import random

def partition(array, start, end): 
    low_index = start - 1
    pivot = array[end]
    for high_index in range(start, end): 
        if array[high_index] < pivot: 
            low_index += 1 
            array[low_index], array[high_index] = array[high_index], array[low_index] 
    array[low_index + 1], array[end] = array[end], array[low_index + 1] 
    return low_index + 1

def quickSort(array, start, end):
    if start < end: 
        pivot = partition(array, start, end)
        quickSort(array, start, pivot - 1) 
        quickSort(array, pivot + 1, end) 

if __name__ == "__main__":
    array_to_sort = random.sample(range(100000), 100000)

    start1 = timer()
    quickSort(array_to_sort, 0, len(array_to_sort)-1) 
    end1 = timer()

    print("Quick sort: {} seconds".format(round(end1-start1, 4)))