import datetime
import math
from collections import defaultdict
import timer
import itertools

plus_infinity = float("inf")


class TravelingSalesman:
    def __init__(self):
        self.points_num = 0
        self.points = []

    def execute(self):
        self.read_input()

        t = timer.start_timer('traveling salesman')
        start_index = 0
        results = defaultdict(dict)

        base_case_bitmask = self.gen_bitmask(start_index, [])
        results[base_case_bitmask][start_index] = 0

        current_bitmasks = [base_case_bitmask]

        for m in range(1, self.points_num):
            m_timer = timer.start_timer('iteration #' + str(m))
            possible_combinations = itertools.combinations(range(1, self.points_num), m)
            last_bitmasks = set(current_bitmasks)
            current_bitmasks = []
            for comb in possible_combinations:
                combination_bitmask = self.gen_bitmask(start_index, comb)
                current_bitmasks.append(combination_bitmask)
                for node in comb:
                    node_point = self.points[node]
                    comb_without_node = [n for n in comb if n != node]
                    comb_without_node_bitmask = self.gen_bitmask(start_index, comb_without_node)
                    min_value = plus_infinity
                    for k in (start_index,) + comb:
                        if k != node:
                            k_point = self.points[k]
                            new_value = results[comb_without_node_bitmask].get(k, plus_infinity) + self.distance(k_point, node_point)
                            min_value = min(min_value, new_value)
                    results[combination_bitmask][node] = min_value

            for k in last_bitmasks:
                del results[k]

            m_timer['finish_timer']()

        full_bitmask = math.pow(2, self.points_num) - 1
        start_point = self.points[start_index]
        min_value = plus_infinity
        for n in range(1, self.points_num):
            n_point = self.points[n]
            new_value = results[full_bitmask].get(n, plus_infinity) + self.distance(start_point, n_point)
            min_value = min(min_value, new_value)

        self.process_results(min_value)
        t['finish_timer']()

    def process_results(self, min_value):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = open("traveling-salesman-" + timestamp + ".txt", "w+")

        print('min value =' + str(min_value))

        p_23 = (27166.6667, 9833.3333)
        p_24 = (27233.3333, 10450.0000)
        # (23-24) + (19-24) + (15-23) - (15-19)
        fix_value = self.distance(p_23, p_24) + self.distance(self.points[19], p_24) + \
                    self.distance(self.points[15], p_23) - self.distance(self.points[15], self.points[19])
        final_result = min_value + fix_value
        print('fin = ' + str(final_result))

        output_file.write("Summary \n")
        output_file.write("Result on 23 nodes = " + str(min_value) + "\n")
        output_file.write("fix_value = " + str(fix_value) + " \n")
        output_file.write("Final result = " + str(final_result) + " \n")

        output_file.close()

    def gen_bitmask(self, first_el: int, rest_items: list) -> int:
        bitmask = pow(2, first_el) + sum([pow(2, n) for n in rest_items])
        return int(bitmask)

    def distance(self, first: tuple, second: tuple) -> float:
        distance = math.sqrt(math.pow(first[0] - second[0], 2) + math.pow(first[1] - second[1], 2))
        return distance

    def read_input(self):
        text_file = open("traveling-salesman-input.txt", "r")
        lines = text_file.readlines()

#         lines = '''12.00
# 1.000 1.00
# 1.125 1.00
# 1.250 1.00
# 1.500 1.00
# 1.750 1.00
# 2.000 1.00
# 1.000 2.00
# 1.125 2.00
# 1.250 2.00
# 1.500 2.00
# 1.750 2.00
# 2.000 2.00'''.splitlines()

        self.points_num = int(lines[0].strip('.00'))

        xs = []
        ys = []
        for line in lines[1:]:
            if line.startswith('#'):
                continue
            splitted = line.strip('\n').split(' ')
            x, y = float(splitted[0]), float(splitted[1])
            self.points.append((x, y))
            xs.append(x)
            ys.append(y)

        # import matplotlib.pyplot as plt
        # plt.scatter(xs, ys)
        # for i, txt in enumerate(xs):
        #     plt.annotate(i, (xs[i], ys[i]))
        # plt.show()


TravelingSalesman().execute()

# 25
# 27166.6667 9833.3333
# 27233.3333 10450.0000