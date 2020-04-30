from timer import start_timer
import time
import datetime

class Main:
    def __init__(self):
        super().__init__()
        self.input_array = []
        self.left_edge = -10000
        self.right_edge = 10000
        
    def execute(self):
        self.read_input()
        existing_sums = {}
        for sum in range(self.left_edge, self.right_edge + 1):
            two_sum_result = self.calculate_distinct_two_sum(sum)
            if (len(two_sum_result) > 0):
                existing_sums[sum] = two_sum_result    
        result = len(existing_sums)
        print("Result = " + str(result))
        
    def execute_group(self):
        self.read_input()
        self.calculate_group_distinct_two_sum(self.left_edge, self.right_edge)
        
    def execute_via_sort(self):
        self.read_input()
        self.calculate_via_sort_distinct_two_sum(self.left_edge, self.right_edge)
        
    def calculate_via_sort_distinct_two_sum(self, left_edge, right_edge):
        self.input_array.sort()
        indexes_table = {}
        result = set()
        input_length = len(self.input_array)
        max_value = self.input_array[-1]
        
        indexing_input_timer = start_timer("indexing")

        for index, num in enumerate(self.input_array):
            indexes_table[num] = index
        indexing_input_timer["finish_timer"]()
        
        pass_input_timer = start_timer("pass")
        start_time = pass_input_timer["start_time"]
        last_time = start_time
        for index, numb in enumerate(self.input_array):
            if (index % 1000 == 0):
                current_time = time.perf_counter()
                print("Pass on " + str(index) + " iteration from 0 to " + str(input_length) + ". Iteration time = " + str(current_time - last_time) + "s. Total Time = " + str(current_time - start_time) + "s")
                last_time = current_time
            left_diff = left_edge - numb
            right_diff = right_edge - numb
            right_diff = right_diff if right_diff < max_value else max_value
            
            start_value = left_diff
            index = -1
            while (start_value <= right_diff):
                if (start_value in indexes_table):
                    index = indexes_table[start_value]
                    break
                else:
                    start_value += 1
            if (index < 0):
                continue

            #for diff in self.input_array[index:]:
            #for diff_index in range(start_index, right_edge + 1):
            while (index < input_length):
                diff = self.input_array[index]
                if (diff > right_diff):
                    break
                if (diff != numb):
                    sum = diff + numb
                    if (sum not in result):
                        result.add(sum)
                index += 1
                    
        finish_time = pass_input_timer["finish_timer"]()["duration_s"]
        print("Result = " + str(len(result)))
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = open("two-sum-result-" + timestamp + ".txt","w+")
        
        output_file.write("Result = " + str(len(result)) + "\n")
        output_file.write("Execution time = " + str(finish_time) + "s\n")
        
        output_file.close()
        
    def calculate_group_distinct_two_sum(self, left_edge, right_edge):
        
        # sort_timer = start_timer("sorting")
        # self.input_array.sort()
        # sort_timer["finish_timer"]()
        
        table = set(self.input_array)

        pass_input_timer = start_timer("pass")
        result = set()
        
        # for sum in range(self.left_edge, self.right_edge + 1):
        #     if (sum % 100 == 0):
        #         print("Sum on " + str(sum) + " iteration from " + str(self.left_edge) + " to " + str(self.right_edge))
        #     for numb in self.input_array:
        #         diff = sum - numb
        #         if (diff != numb and diff in table):
        #             result[sum] = 1
        #             break
        input_length = len(self.input_array)
        start_time = pass_input_timer["start_time"]
        last_time = start_time
        for index, numb in enumerate(self.input_array):
            if (index % 1000 == 0):
                current_time = time.perf_counter()
                print("Pass on " + str(index) + " iteration from 0 to " + str(input_length) + ". Iteration time = " + str(current_time - last_time) + "s. Total Time = " + str(current_time - start_time) + "s")
                last_time = current_time
            left_diff = left_edge - numb
            right_diff = right_edge - numb
            for diff in range(left_diff, right_diff + 1):
                sum = diff + numb
                if (diff != numb and sum not in result and diff in table):
                   result.add(sum)
        pass_input_timer["finish_timer"]()  
        print("Result = " + str(len(result)))
        
    def calculate_distinct_two_sum(self, sum_value):
        table = {}
        dict_input_timer = start_timer("Move to dict")
        for index, numb in enumerate(self.input_array):
            table[numb] = index
        dict_input_timer["finish_timer"]()
        
        pass_input_timer = start_timer("pass")
        sum_couples = []
        for index, numb in enumerate(self.input_array):
            difference = sum_value - numb
            if (difference == numb or not (self.left_edge < difference and difference < self.right_edge)):
                pass
            second_part_index = table.pop(difference, None)
            if (second_part_index):
                sum_couples.append((numb, difference))
        pass_input_timer["finish_timer"]()
        return sum_couples     
        
    def read_input(self):
        read_input_timer = start_timer("reading input")
        text_file = open("two-sum-input.txt", "r")
        lines = text_file.readlines()
#         text = """-3

# -1

# 1

# 2

# 9

# 11

# 7

# 6

# 2"""
#         lines = text.split("\n\n")
#         self.left_edge = 3
#         self.right_edge = 10
        self.input_array = [int(line) for line in lines]
        read_input_timer["finish_timer"]()
        
Main().execute_via_sort()