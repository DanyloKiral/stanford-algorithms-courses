from heap import Heap
from random import randint

plus_infinity = float("inf")
        
class Main:
    def __init__(self):
        super().__init__()
        self.number_of_edges = None
        self.number_of_vertices = None
        self.node_edges_map = {}
        
    def main(self):
        self.read_input()
        self.calculate_min_spanning_tree_prim()
        
    def calculate_min_spanning_tree_prim(self):
        discovered_nodes = {}
        nodes_in_heap = {}
        unprocessed_heap = Heap()
        for i in range(1, self.number_of_vertices + 1):
            discovered_nodes[i] = False
            nodes_in_heap[i] = False
        start_node = randint(1, self.number_of_vertices)
        discovered_nodes[start_node] = True
        discovered_nodes_count = 1
        self.insert_min_edges_to_heap(unprocessed_heap, self.node_edges_map[start_node], discovered_nodes, nodes_in_heap)
        min_tree_cost = 0
        while discovered_nodes_count < self.number_of_vertices:
            (next_node_key, cost) = unprocessed_heap.pop()
            nodes_in_heap[next_node_key] = False
            discovered_nodes[next_node_key] = True
            discovered_nodes_count += 1
            min_tree_cost += cost
            self.insert_min_edges_to_heap(unprocessed_heap, self.node_edges_map[next_node_key], discovered_nodes, nodes_in_heap)
            
        result = min_tree_cost
        print(result)
        
    def insert_min_edges_to_heap(self, heap, node_edges, discovered_nodes, nodes_in_heap):
        for edge in node_edges:
            current_edge_weight = plus_infinity
            if (nodes_in_heap[edge[0]]):
                current_edge_weight = heap.remove(edge[0])
                nodes_in_heap[edge[0]] = False
            if (not discovered_nodes[edge[0]]):
                heap.push(edge[0], min(current_edge_weight, edge[1]))
                nodes_in_heap[edge[0]] = True
        
    def read_input(self):
        text_file = open("prim-minimum-spanning-tree_input.txt", "r")
        lines = text_file.readlines()
#         lines = """4 5

# 1 2 1

# 2 4 2

# 3 1 4

# 4 3 5

# 4 1 3""".split("\n\n")
        (self.number_of_vertices, self.number_of_edges) = (int(numb) for numb in lines[0].split(" "))
        for line in lines[1:]:
            (node1, node2, weight) = (int(numb) for numb in line.split(" "))
            self.push_node_edge_to_map(node1, node2, weight)
            self.push_node_edge_to_map(node2, node1, weight)
            #self.edges.append(GraphEdge(node1, node2, weight))
            
    def push_node_edge_to_map(self, node_from, node_to, weight):
        if (node_from not in self.node_edges_map):
            self.node_edges_map[node_from] = []
        self.node_edges_map[node_from].append((node_to, weight))
        
    
    
Main().main()