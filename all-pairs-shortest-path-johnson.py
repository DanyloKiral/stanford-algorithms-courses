from collections import defaultdict
import timer
from heap import Heap

plus_infinity = float("inf")


class AllPairsShortestPath:
    def __init__(self):
        self.additional_vertex_index = 0
        self.vertices_num = 0
        self.edges_num = 0
        # from, to: weight
        self.edges = defaultdict(dict)
        self.edges_by_end_vertex = defaultdict(dict)
        self.reweighted_edges_weights = defaultdict(dict)

    def execute(self):
        self.read_input()
        # self.read_test_input()
        # res = self.dijkstra_min_paths(1, self.edges)
        # print('f')
        self.add_zero_vertex()
        shortest_paths_to_zero_vertex = self.bellman_ford_algorithm(self.additional_vertex_index, self.vertices_num + 1)
        if not shortest_paths_to_zero_vertex:
            print('Graph has negative cycles')
            return
        self.reweight_graph(shortest_paths_to_zero_vertex)
        self.edges.pop(self.additional_vertex_index)
        self.reweighted_edges_weights.pop(self.additional_vertex_index)

        t = timer.start_timer('dijkstra shortest path for each vertex')
        shortest_paths = {}
        shortest_of_the_shortest = plus_infinity
        for v_from in range(1, self.vertices_num + 1):
            if v_from % 100 == 0:
                print('v = ' + str(v_from))
            result = self.dijkstra_min_paths(v_from, self.reweighted_edges_weights)
            for v_to, min_weight in result.items():
                init_weight = min_weight - shortest_paths_to_zero_vertex[v_from] + shortest_paths_to_zero_vertex[v_to]
                shortest_paths[v_from, v_to] = init_weight
                shortest_of_the_shortest = min(init_weight, shortest_of_the_shortest)
        t['finish_timer']()
        print('Shortest of the shortest = ' + str(shortest_of_the_shortest))

    def add_zero_vertex(self):
        t = timer.start_timer('Add zero vertex')
        for i in range(1, self.vertices_num + 1):
            self.edges[self.additional_vertex_index][i] = 0
            if i not in self.edges_by_end_vertex:
                self.edges_by_end_vertex[i] = []
            self.edges_by_end_vertex[i].append(self.additional_vertex_index)
        t['finish_timer']()

    def bellman_ford_algorithm(self, start_vertex: int, vertices_num: int) -> dict:
        t = timer.start_timer('Reweighting graph shortest paths calculations')
        prev_comp = {}
        prev_comp[start_vertex] = 0
        for i in range(1, vertices_num + 1):
            prev_comp[i] = plus_infinity if i != start_vertex else 0

        for i in range(1, vertices_num + 1):
            current_comp = {}
            can_stop = True
            for v in range(1, vertices_num + 1):
                if v == start_vertex:
                    current_comp[v] = 0
                    continue
                old_value = prev_comp[v]
                new_value = plus_infinity
                for v_from in self.edges_by_end_vertex[v]:
                    weight = self.edges[v_from][v]
                    new_value = min(prev_comp[v_from] + weight, new_value)
                if old_value <= new_value:
                    current_comp[v] = old_value
                else:
                    current_comp[v] = new_value
                    can_stop = False
            if can_stop:
                break
            elif i == vertices_num:
                # has a negative cycle
                current_comp = None
            prev_comp = current_comp
        t['finish_timer']()
        return current_comp

    def reweight_graph(self, shortest_paths_to_zero_vertex: dict):
        t = timer.start_timer('Calculating new edge weights')
        for v_from, edge_dict in self.edges.items():
            for v_to, weight in edge_dict.items():
                recalc_weight = weight + shortest_paths_to_zero_vertex[v_from] - shortest_paths_to_zero_vertex[v_to]
                self.reweighted_edges_weights[v_from][v_to] = recalc_weight
        t['finish_timer']()

    def dijkstra_min_paths(self, start_vertex: int, edges: dict) -> dict:
        vertices_processed = {}
        distances = {}
        unprocessed_heap = Heap()
        for v_from, edge_dict in edges.items():
            for v_to, weight in edge_dict.items():
                vertices_processed[v_to] = True if v_to == v_from else False
                distances[v_to] = 0 if v_to == v_from else plus_infinity
        start_edges_dict = edges[start_vertex]
        for v in range(1, self.vertices_num + 1):
            edge = start_edges_dict.get(v, None)
            unprocessed_heap.push(v, edge if edge is not None else plus_infinity)

        min_edge_to_add = unprocessed_heap.pop()
        while min_edge_to_add:
            vertex_to_add = min_edge_to_add[0]
            min_edge_weight = min_edge_to_add[1]
            vertices_processed[vertex_to_add] = True
            distances[vertex_to_add] = min_edge_weight
            for vertex_to, weight in edges[vertex_to_add].items():
                if not vertices_processed[vertex_to]:
                    current_weight = unprocessed_heap.remove(vertex_to)
                    new_weight = min(current_weight, min_edge_weight + weight)
                    unprocessed_heap.push(vertex_to, new_weight)
            min_edge_to_add = unprocessed_heap.pop()
        return distances

    def read_input(self):
        text_file = open("all-pairs-shortest-path_input/3.txt", "r")
        lines = text_file.readlines()

#         lines = '''16 26
# 1 14 39
# 1 4 81
# 1 14 14
# 1 12 -93
# 2 8 -27
# 2 7 -13
# 2 14 -39
# 3 8 17
# 3 7 53
# 4 14 -58
# 4 6 25
# 4 15 -74
# 5 9 -38
# 5 7 -52
# 5 13 52
# 7 9 31
# 7 12 42
# 7 9 59
# 8 16 26
# 8 12 -58
# 9 16 48
# 10 11 98
# 12 15 -37
# 12 13 80
# 12 14 71
# 13 16 -23'''.splitlines()

        splitted_line = lines[0].strip('\n').split(' ')
        self.vertices_num, self.edges_num = int(splitted_line[0]), int(splitted_line[1])

        self.additional_vertex_index = self.vertices_num + 1

        for line in lines[1:]:
            splitted_line = line.strip('\n').split(' ')
            v_from, v_to, weight = int(splitted_line[0]), int(splitted_line[1]), int(splitted_line[2])
            exs = self.edges[v_from].get(v_to, None)
            min_v = weight
            if exs and exs < min_v:
                min_v = exs
            self.edges[v_from][v_to] = min_v
            if v_to not in self.edges_by_end_vertex:
                self.edges_by_end_vertex[v_to] = []
            self.edges_by_end_vertex[v_to].append(v_from)

    def read_test_input(self):
        #text_file = open("graph_path_dijkstra_input.txt", "r")
        #lines = text_file.readlines()
        lines = '''1 2,1 8,2

2 1,1 3,1

3 2,1 4,1

4 3,1 5,1

5 4,1 6,1

6 5,1 7,1

7 6,1 8,1

8 7,1 1,2'''.split('\n\n')
        self.vertices_num = 8
        for line in lines:
            splitted = line.strip("\t\n").split(" ")
            v_from = int(splitted[0])
            for edge in splitted[1:]:
                splitted_edge = edge.split(",")
                v_to, weight = int(splitted_edge[0]), int(splitted_edge[1])
                self.edges[v_from][v_to] = weight
                if v_to not in self.edges_by_end_vertex:
                    self.edges_by_end_vertex[v_to] = []
                self.edges_by_end_vertex[v_to].append(v_from)


AllPairsShortestPath().execute()
