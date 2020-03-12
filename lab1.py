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

def quick_sort(array, start, end):
    if start < end: 
        pivot = partition(array, start, end)
        quick_sort(array, start, pivot - 1) 
        quick_sort(array, pivot + 1, end) 

def merge_sort(array): 
    if len(array) > 1: 
        mid_index = len(array) // 2
        left_side = array[:mid_index]
        right_side = array[mid_index:]
  
        merge_sort(left_side)
        merge_sort(right_side)

        left_index = right_index = array_index = 0

        while left_index < len(left_side) and right_index < len(right_side): 
            if left_side[left_index] < right_side[right_index]: 
                array[array_index] = left_side[left_index] 
                left_index += 1
            else: 
                array[array_index] = right_side[right_index] 
                right_index += 1
            array_index += 1

        while left_index < len(left_side): 
            array[array_index] = left_side[left_index] 
            left_index += 1
            array_index += 1
          
        while right_index < len(right_side): 
            array[array_index] = right_side[right_index] 
            right_index += 1
            array_index += 1


if __name__ == "__main__":
    array_to_sort_1 = random.sample(range(100000), 100000)
    array_to_sort_2 = random.sample(range(100000), 100000)

    start1 = timer()
    quick_sort(array_to_sort_1, 0, len(array_to_sort_1)-1) 
    end1 = timer()

    start2 = timer()
    merge_sort(array_to_sort_2)
    end2 = timer()
    
    print("Quick sort: {} seconds".format(round(end1-start1, 4)))
    print("Merge sort: {} seconds".format(round(end2-start2, 4)))
    