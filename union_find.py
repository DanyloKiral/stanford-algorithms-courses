class UnionFind:
    # each init point is own group
    def __init__(self, points):
        super().__init__()
        self.leaders_map = {}
        self.ranks = {}
        for point in points:
            self.leaders_map[point] = point
            self.ranks[point] = 0
            
    def find(self, x):
        path_compression_nodes = []
        current_node = x
        current_node_leader = self.leaders_map[current_node]
        while (current_node != current_node_leader):
            path_compression_nodes.append(current_node)
            current_node = current_node_leader
            current_node_leader = self.leaders_map[current_node]
        for node in path_compression_nodes:
            self.leaders_map[node] = current_node_leader
        return current_node_leader
    
    def union(self, x, y):
        x_leader = self.find(x)
        y_leader = self.find(y)
        if (x_leader == y_leader):
            return x_leader
        
        leader = y_leader
        child = x_leader 
        if (self.ranks[x_leader] > self.ranks[y_leader]):
            leader, child = child, leader

        self.leaders_map[child] = leader
        self.ranks[leader] = max(self.ranks[leader], self.ranks[child] + 1)
        return leader
        
    def get_clusters(self):
        clusters = {}
        for node, leader in self.leaders_map.items():
            if (not clusters.get(leader, None)):
                clusters[leader] = []
            clusters[leader].append(node)
        return clusters