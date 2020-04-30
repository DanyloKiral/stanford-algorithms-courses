from heap import Heap
from timer import start_timer

plus_infinity = float("inf")
needed_result_vertices_distance_in_order = [7,37,59,82,99,115,133,165,188,197]

class Main:
    def __init__(self):
        super().__init__()
        self.adjustency_list = {}
        self.vertices_processed = {}
        self.distances = {}
        
    def execute(self):
        self.read_input()
        
        processing_data_timer = start_timer("processing data")
        start_vertex = 1 
        self.vertices_processed = {}
        self.distances = {}
        unprocessed_heap = Heap()
        for vertex, edges in self.adjustency_list.items():
            self.vertices_processed[vertex] = True if vertex == start_vertex else False
            self.distances[vertex] = 0 if vertex == start_vertex else plus_infinity
            unprocessed_heap.push(vertex, plus_infinity)         
        for vertex_to, weight in self.adjustency_list[start_vertex]:
            unprocessed_heap.remove(vertex_to)
            unprocessed_heap.push(vertex_to, weight)
        processing_data_timer["finish_timer"]()
        
        main_loop_timer = start_timer("main loop")
        min_edge_to_add = unprocessed_heap.pop()
        while (min_edge_to_add):
            vertex_to_add = min_edge_to_add[0]
            min_edge_weight = min_edge_to_add[1]
            self.vertices_processed[vertex_to_add] = True
            self.distances[vertex_to_add] = min_edge_weight
            for edge in self.adjustency_list[vertex_to_add]:
                edge_vertex_to = edge[0]
                if (not self.vertices_processed[edge_vertex_to]):
                    edge_weight = edge[1]
                    current_weight = unprocessed_heap.remove(edge_vertex_to)
                    new_weight = min(current_weight, min_edge_weight + edge_weight)
                    unprocessed_heap.push(edge_vertex_to, new_weight)
            min_edge_to_add = unprocessed_heap.pop()
        main_loop_timer["finish_timer"]()
        
        result = [str(self.distances[vertex_for_result]) for vertex_for_result in needed_result_vertices_distance_in_order]
        print("Answer: " + ",".join(result))            
                 
    
    def read_input(self):
        read_input_timer = start_timer("reading input")
        text_file = open("graph_path_dijkstra_input.txt", "r")
        lines = text_file.readlines()
        # input in formar [edge_from]: (edge_to, edge_weight)
        self.adjustency_list = {}
        for line in lines:
            splitted = line.strip("\t\n").split("\t")
            vertex_from = int(splitted[0])
            vertex_to_with_weights = []
            for edge in splitted[1:]:
                splitted_edge = edge.split(",")
                vertex_to_with_weights.append((int(splitted_edge[0]), int(splitted_edge[1])))
            self.adjustency_list[vertex_from] = vertex_to_with_weights
        read_input_timer["finish_timer"]()


Main().execute()