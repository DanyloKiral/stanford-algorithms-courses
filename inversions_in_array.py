import math

text_file = open("inversions_in_array_input.txt", "r")
lines = text_file.readlines()
input_array = list(map(int, lines))

def sort_and_count_inversions(array):
    array_length = len(array)

    if (array_length < 2):
        return (array, 0)
    elif (array_length == 2):
        return ([array[1], array[0]], 1) if (array[0] > array[1]) else (array, 0)

    split_number = math.ceil(array_length / 2)

    left_part = array[:split_number]
    right_part = array[split_number:]

    (left_part, left_count) = sort_and_count_inversions(left_part)
    (right_part, right_count) = sort_and_count_inversions(right_part)

    count = left_count + right_count

    sortedArray = [None] * array_length
    left_index = 0
    right_index = 0
    for index in range(array_length):
        if (right_index >= array_length - split_number):
            sortedArray[index] = left_part[left_index]
            left_index += 1
            continue
        elif (left_index >= split_number):
            sortedArray[index] = right_part[right_index]
            right_index += 1
            continue
 
        if (left_part[left_index] < right_part[right_index]):
            sortedArray[index] = left_part[left_index]
            left_index += 1
        elif (right_part[right_index] < left_part[left_index]):
            sortedArray[index] = right_part[right_index]
            count += split_number - left_index
            right_index += 1

    return (sortedArray, count)

#input_array = [4, 80, 70, 23, 9, 60, 68, 27, 66, 78, 12, 40, 52, 53, 44, 8, 49, 28, 18, 46, 21, 39, 51, 7, 87, 99, 69, 62, 84, 6, 79, 67, 14, 98, 83, 0, 96, 5, 82, 10, 26, 48, 3, 2, 15, 92, 11, 55, 63, 97, 43, 45, 81, 42, 95, 20, 25, 74, 24, 72, 91, 35, 86, 19, 75, 58, 71, 47, 76, 59, 64, 93, 17, 50, 56, 94, 90, 89, 32, 37, 34, 65, 1, 73, 41, 36, 57, 77, 30, 22, 13, 29, 38, 16, 88, 61, 31, 85, 33, 54 ]

(sorted_array, count_of_inversions) = sort_and_count_inversions(input_array)

print(sorted_array)
print(count_of_inversions)
        