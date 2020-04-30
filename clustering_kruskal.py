from union_find import UnionFind

class Clustering:
    def __init__(self):
        super().__init__()
        self.number_of_nodes = 0
        # (edge_cost, node1, node2)
        self.edges = []
        self.target_clusters_num = 4
        
    def execute(self):
        self.read_input()
        
        sorted_edges = sorted(self.edges, key=lambda edge: edge[0])
        union_find = UnionFind(range(0, self.number_of_nodes))
        clusters_num = self.number_of_nodes
        maximum_spacing = None
        for edge in sorted_edges:
            cost, node1, node2 = edge
            node1_leader, node2_leader = union_find.find(node1), union_find.find(node2)
            if (node1_leader != node2_leader):
                if (clusters_num == self.target_clusters_num):
                    maximum_spacing = edge[0]
                    break
                union_find.union(node1, node2)
                clusters_num -= 1
        # 106
        print(maximum_spacing)

        
    def read_input(self):
        text_file = open("clustering-kruskal-input.txt", "r")
        lines = text_file.readlines()
        
        self.number_of_nodes = int(lines[0])
        self.target_clusters_num = 4
        
        for line in lines[1:]:
            splitted = line.split(' ')
            node1, node2, cost = splitted
            edge_record = (int(cost), int(node1) - 1, int(node2) - 1)
            self.edges.append(edge_record)
            
Clustering().execute()