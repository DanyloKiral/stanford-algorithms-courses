from collections import defaultdict
from timer import start_timer

plus_infinity = float("inf")

import sys
sys.setrecursionlimit(10000)

class Knapsack:
    def __init__(self):
        super().__init__()
        self.items = []
        self.knapsack_size = 0
        self.items_num = 0
        self.min_weight = plus_infinity

    def execute(self):
        self.read_input()
        timer = start_timer('knapsack')
        #self.knapsack_small()  # 1.14519s
        self.knapsack_recursive_large()
        timer['finish_timer']()

    def knapsack_small(self):
        results_table = defaultdict(dict)
        for x in range(0, self.knapsack_size + 1):
            results_table[0, x] = 0

        for i, value_weight in enumerate(self.items):
            value, weight = value_weight
            for x in range(0, self.knapsack_size + 1):
                left = results_table[i, x]
                right = (results_table[i, x - weight] + value) if weight <= x else 0
                results_table[i + 1, x] = max(left, right)

        result = results_table[self.items_num, self.knapsack_size]

        print('result = ' + str(result)) # 2493893

    def knapsack_optimal(self):
        current_table = defaultdict(dict)
        knapsack_capacity_range = range(self.min_weight, self.knapsack_size + 1)

        for i, value_weight in enumerate(self.items):
            prev_table = current_table
            current_table = defaultdict(dict)
            value, weight = value_weight

            for x in knapsack_capacity_range[weight:]:
                current_optimal = prev_table[x] or 0
                new_optimal = (prev_table[x - weight] or 0) + value
                current_table[x] = max(current_optimal, new_optimal)

        result = current_table[self.knapsack_size]

        print('result = ' + str(result)) # 2493893

    def knapsack_recursive_large(self):
        results_table = defaultdict(dict)

        def calculate_result_recursive(i, x):
            if i == 0 or x == 0:
                results_table[i, x] = 0
                return 0
            existing = results_table[i, x]
            if existing:
                return existing
            current_item_value, current_item_weight = self.items[i - 1]

            current_optimal = results_table[i - 1, x] or calculate_result_recursive(i - 1, x)
            new_optimal = ((results_table[i - 1, x - current_item_weight] or calculate_result_recursive(i - 1, x - current_item_weight)) + current_item_value) \
                if current_item_weight <= x else 0
            current_result = max(current_optimal, new_optimal)
            results_table[i, x] = current_result
            return current_result

        result = calculate_result_recursive(self.items_num, self.knapsack_size)
        print(result) # 4243395

    def read_input(self):
        text_file = open("knapsack-input-large.txt", "r")
        lines = text_file.readlines()

#         lines = '''100 10
# 44 47
# 9 43
# 19 18
# 48 22
# 33 31
# 14 12
# 7 8
# 6 16
# 46 47
# 38 30'''.splitlines() # 133

#         lines = '''6 4
# 3 4
# 2 3
# 4 2
# 4 3'''.splitlines() # 8

        line_split = lines[0].split(' ')
        self.knapsack_size, self.items_num = int(line_split[0]), int(line_split[1])

        for line in lines[1:]:
            line_split = line.split(' ')
            value = int(line_split[0])
            weight = int(line_split[1])
            self.min_weight = min(self.min_weight, weight)
            self.items.append((value, weight))


Knapsack().execute()
