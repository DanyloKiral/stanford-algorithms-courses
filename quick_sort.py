import math

text_file = open("quick_sort_input.txt", "r")
lines = text_file.readlines()
input_array = list(map(int, lines))

# returns number of comparisons made
def quick_sort(array, start_index, length):
    if (length - start_index <= 1):
        return 0

    number_of_comparisons = 0
    # choose pivot and place it at first array position
    pivot = choose_pivot_first(array, start_index, length - start_index)

    # partition
    i = start_index + 1
    for j in range(start_index + 1, length):
        if (array[j] < pivot):
            array[j], array[i] = array[i], array[j]
            i += 1
            
        number_of_comparisons += 1

    # place pivot in the middle of two subarrays
    array[start_index], array[i - 1] = array[i - 1], array[start_index]

    number_of_comparisons += quick_sort(array, start_index, i - 1)
    number_of_comparisons += quick_sort(array, i, length)

    return number_of_comparisons


def choose_pivot_first(array, start_index, length):
    return array[start_index]

def choose_pivot_last(array, start_index, length):
    array[length + start_index - 1], array[start_index] = array[start_index], array[length + start_index - 1]
    return array[start_index]

def choose_pivot_three_median(array, start_index, length):
    middle_index = math.floor((length - 1) / 2 + start_index)
    last_index = length + start_index - 1

    start_value = array[start_index]
    middle_value = array[middle_index]
    last_value = array[last_index]

    if (middle_value <= start_value < last_value or last_value < start_value <= middle_value):
        return start_value
        
    if (start_value < last_value < middle_value or middle_value < last_value < start_value):
        array[start_index], array[last_index] = array[last_index], array[start_index]
        return last_value

    if (start_value < middle_value < last_value or last_value < middle_value < start_value):
        array[start_index], array[middle_index] = array[middle_index], array[start_index]
        return middle_value

comp = quick_sort(input_array, 0, len(input_array))
print(comp)
#print(input_array)