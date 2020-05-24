from collections import defaultdict

import timer

plus_infinity = float("inf")


class AllPairsShortestPath:
    def __init__(self):
        self.vertices_num = 0
        self.edges_num = 0
        # from, to: weight
        self.edges = {}

    def execute(self):
        self.read_input()
        vertices_range = range(1, self.vertices_num + 1)

        read_timer = timer.start_timer('Init table with base cases')
        results = defaultdict()
        for i in vertices_range:
            for j in vertices_range:
                base_value = plus_infinity
                if i == j:
                    base_value = 0
                else:
                    i_j_edge_weight = self.edges.get((i, j), None)
                    if i_j_edge_weight:
                        base_value = i_j_edge_weight
                results[i, j, 0] = base_value

        read_timer['finish_timer']()

        computing_timer = timer.start_timer('Computing result matrix')
        for k in vertices_range:
            if k % 25 == 0:
                print('k = ' + str(k))
            for i in vertices_range:
                for j in vertices_range:
                    old_value = results[i, j, k - 1]
                    new_value = results[i, k, k - 1] + results[k, j, k - 1]
                    results[i, j, k] = min(old_value, new_value)
        computing_timer['finish_timer']()

        process_results_timer = timer.start_timer('Process results')
        has_negative_cycle = False
        for i in vertices_range:
            if results[i, i, self.vertices_num] < 0:
                has_negative_cycle = True
                break
        if has_negative_cycle:
            print('Has negative cycle!')
        else:
            min_value = plus_infinity
            for i in vertices_range:
                for j in vertices_range:
                    if not i == j:
                        min_value = min(min_value, results[i, j, self.vertices_num])

            print('Shortest shortest path = ' + str(min_value))

        process_results_timer['finish_timer']()

    def read_input(self):
        text_file = open("all-pairs-shortest-path_input/1.txt", "r")
        lines = text_file.readlines()

        splitted_line = lines[0].strip('\n').split(' ')
        self.vertices_num, self.edges_num = int(splitted_line[0]), int(splitted_line[1])

        for line in lines[1:]:
            splitted_line = line.strip('\n').split(' ')
            v_from, v_to, weight = int(splitted_line[0]), int(splitted_line[1]), int(splitted_line[2])
            self.edges[v_from, v_to] = weight

AllPairsShortestPath().execute()


