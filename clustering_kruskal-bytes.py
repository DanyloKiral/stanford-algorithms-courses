from union_find import UnionFind
import math

class Clustering:
    def __init__(self):
        super().__init__()
        self.number_of_nodes = 0
        self.number_of_bits = 0
        # edge_value: index
        self.node_bits_values = {}
        
    def execute(self):
        self.read_input()
        union_find = UnionFind(range(0, self.number_of_nodes))
        
        iteration_no = 1
        
        clusters_num = self.iteration(union_find, self.number_of_nodes, iteration_no)
        iteration_no += 1
        clusters_num = self.iteration(union_find, clusters_num, iteration_no)
        
        # 1213
        print(clusters_num)
        clusters = union_find.get_clusters()
        print(len(clusters)) # correct
        print('finish')
        
    def iteration(self, union_find, clusters_num, iteration_no):
        
        for edge_value, indexes in self.node_bits_values.items():
            if (len(indexes) > 1):
                current_item_leader = union_find.find(indexes[0])
                united_num = self.unite_nodes_if_needed(union_find, indexes[0], current_item_leader, edge_value)
                if (united_num):
                    clusters_num -= united_num
        
        masks_1 = [int(math.pow(2, i)) for i in range(self.number_of_bits)]
        
        for edge_value, indexes in self.node_bits_values.items():
            for index in indexes:
                current_item_leader = union_find.find(index)

                for mask in masks_1:
                    next_cluster_value = edge_value ^ mask
                    united_num = self.unite_nodes_if_needed(union_find, index, current_item_leader, next_cluster_value)
                    if (united_num):
                        clusters_num -= united_num
                        current_item_leader = union_find.find(index)
        
        masks_2 = []
        for j in range(self.number_of_bits):
            mask_j = int(math.pow(2, j))
            for i in range(self.number_of_bits):
                mask_i = mask_j + int(math.pow(2, i))
                if (mask_i not in masks_1):
                    masks_2.append(mask_i)
            
        masks_2 = set(masks_2)
        
        for edge_value, indexes in self.node_bits_values.items():
            for index in indexes:
                current_item_leader = union_find.find(index)

                for mask in masks_2:
                    next_cluster_value = edge_value ^ mask
                    united_num = self.unite_nodes_if_needed(union_find, index, current_item_leader, next_cluster_value)
                    if (united_num):
                        clusters_num -= united_num
                        current_item_leader = union_find.find(index)
                        
        return clusters_num
    
    # def iteration(self, union_find, clusters_num, iteration_no):
    #     discharges = range(0, self.number_of_bits)
        
    #     for edge_value, indexes in self.node_bits_values.items():
    #         for index in indexes:
    #             current_item_leader = union_find.find(index)

    #             for discharge_outer in discharges:
    #                 outer_diff_value = int(math.pow(2, discharge_outer))
    #                 if (iteration_no == 1):
    #                     next_cluster_value = edge_value ^ outer_diff_value
    #                     united_num = self.unite_nodes_if_needed(union_find, index, current_item_leader, next_cluster_value)
    #                     if (united_num):
    #                         clusters_num -= united_num
    #                         current_item_leader = union_find.find(index)
    #                 else:
    #                     for discharge_inner in discharges:
    #                         if (discharge_inner == discharge_outer):
    #                             continue
    #                         next_cluster_value = outer_diff_value + int(math.pow(2, discharge_inner))
    #                         united_num = self.unite_nodes_if_needed(union_find, index, current_item_leader, next_cluster_value)
    #                         if (united_num):
    #                             clusters_num -= united_num
    #                             current_item_leader = union_find.find(index)
    #     return clusters_num
    
    def unite_nodes_if_needed(self, union_find, current_index, current_item_leader, next_cluster_value): 
        next_cluster_indexes = self.node_bits_values.get(next_cluster_value, None)
        if (next_cluster_indexes):
            united_num = 0
            for next_cluster_index in next_cluster_indexes:
                next_cluster_leader = union_find.find(next_cluster_index)
                if (next_cluster_leader != current_item_leader and current_index != next_cluster_index):
                    union_find.union(current_index, next_cluster_index)
                    united_num += 1
            return united_num
        return 0
        
    def read_input(self):
        text_file = open("clustering-kruskal-bytes-input-test.txt", "r")
        lines = text_file.readlines()
        
#         text = '''128 16
# 1 1 1 0 1 0 1 0 1 0 0 1 1 1 1 1
# 0 0 0 0 1 0 0 1 1 0 0 0 0 0 0 1
# 0 0 0 1 1 0 1 0 0 0 0 1 0 0 0 0
# 0 0 1 1 1 0 0 1 0 0 0 0 1 0 1 1
# 1 1 0 0 1 1 1 1 0 1 0 0 1 1 1 1
# 1 1 0 1 1 1 0 1 0 1 1 0 0 0 0 1
# 0 1 1 1 1 0 1 0 0 0 1 0 1 1 1 1
# 1 0 1 1 1 1 0 1 1 1 1 0 1 1 1 1
# 1 0 1 0 0 0 0 0 1 0 1 0 1 0 1 0
# 0 1 0 1 0 0 1 1 0 1 1 1 1 1 0 1
# 1 0 1 0 1 0 1 1 0 1 1 1 0 0 1 1
# 1 0 1 0 0 1 0 1 1 1 1 1 0 0 1 1
# 1 0 1 0 1 0 0 0 1 1 1 1 1 0 1 0
# 1 0 0 0 1 1 1 0 0 1 1 1 0 0 0 1
# 1 1 1 0 1 1 0 1 1 1 1 1 1 1 1 0
# 0 1 0 1 1 0 0 0 1 1 0 1 1 1 0 0
# 1 1 0 0 0 1 0 0 1 0 1 0 1 0 1 0
# 1 0 1 1 1 1 1 0 0 0 1 0 0 0 1 0
# 1 0 0 1 1 1 1 0 1 1 0 1 1 1 1 1
# 1 1 1 1 0 1 0 0 1 0 0 0 0 1 1 1
# 0 1 1 1 1 0 0 0 1 1 0 1 1 0 1 1
# 0 0 1 0 0 0 1 0 1 0 0 1 0 0 0 1
# 0 1 0 0 0 1 0 1 1 0 1 0 0 0 1 0
# 1 0 0 1 1 1 0 1 1 0 0 1 1 0 1 1
# 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 0
# 0 1 0 0 0 0 0 1 0 0 1 0 1 0 0 1
# 1 1 0 1 0 0 1 0 1 1 1 1 1 0 1 0
# 0 1 0 1 1 1 1 0 1 0 1 0 0 1 1 0
# 0 0 1 0 1 0 1 0 0 1 1 1 0 1 0 1
# 1 0 0 1 1 0 1 0 0 0 0 1 0 1 0 0
# 1 0 1 0 0 0 1 1 1 1 0 1 1 1 1 1
# 1 1 1 0 0 1 1 1 0 0 1 0 0 0 1 1
# 1 0 1 0 1 1 1 1 0 1 0 1 1 0 0 1
# 1 0 1 0 1 1 1 1 1 1 0 0 0 1 0 0
# 0 1 0 0 1 1 1 0 0 1 0 0 1 1 0 1
# 1 0 0 0 1 0 0 0 0 1 1 1 0 1 1 1
# 0 0 0 0 0 1 1 1 1 1 1 0 1 1 0 0
# 0 1 1 0 0 0 1 1 0 0 1 0 0 0 1 1
# 1 0 1 0 0 1 0 0 0 0 0 1 0 1 0 1
# 0 1 0 0 0 0 0 0 1 1 1 0 0 1 1 1
# 0 0 0 0 1 1 1 1 1 0 1 0 0 0 1 1
# 0 0 1 0 0 0 0 0 1 1 1 0 0 0 1 1
# 0 0 1 0 1 0 0 1 0 0 0 1 0 0 1 0
# 0 0 0 1 1 0 1 1 0 0 1 1 0 1 0 0
# 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
# 0 1 1 0 0 1 0 1 1 1 0 0 0 1 0 1
# 0 0 1 1 0 0 0 0 0 0 1 1 1 0 1 1
# 0 0 1 0 0 0 1 0 1 0 1 1 0 0 1 1
# 1 0 0 1 0 1 0 0 1 1 0 0 0 1 0 1
# 1 0 0 0 0 1 0 0 0 1 0 1 1 0 1 1
# 0 1 0 1 0 1 1 0 1 1 1 0 0 1 1 0
# 1 0 0 0 1 1 1 1 1 1 0 0 0 0 0 1
# 0 0 0 1 0 1 1 0 0 1 0 1 0 1 1 1
# 1 0 0 0 1 0 0 1 1 0 0 1 1 0 1 0
# 0 1 1 0 0 0 1 1 1 0 0 0 1 0 0 0
# 0 1 1 1 1 1 0 0 1 0 0 0 1 1 1 0
# 0 0 0 0 0 0 1 0 0 1 0 0 1 1 0 1
# 1 0 0 1 0 1 0 0 0 1 0 1 0 1 1 0
# 1 1 1 1 1 0 1 0 0 0 1 1 0 0 1 0
# 1 1 0 1 1 1 1 1 0 0 0 1 1 0 0 0
# 0 0 0 0 1 0 0 1 0 1 1 1 0 0 0 1
# 1 0 0 1 0 0 1 0 0 1 0 0 1 0 1 1
# 1 1 1 1 0 1 0 1 1 1 0 0 1 0 1 1
# 0 0 1 1 0 0 0 0 1 1 0 0 1 1 1 0
# 1 1 1 1 0 0 0 1 0 0 0 1 1 1 1 0
# 1 0 0 1 1 1 1 1 1 1 0 0 1 0 0 1
# 1 1 1 1 0 0 1 0 0 0 1 1 1 0 1 0
# 1 0 1 1 1 1 0 0 0 1 0 1 0 0 0 0
# 0 0 1 1 1 0 1 1 1 0 1 0 0 0 1 1
# 0 1 1 1 1 0 0 1 1 1 0 0 1 1 0 0
# 1 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0
# 1 0 0 1 0 1 1 1 0 1 1 0 0 1 0 0
# 1 0 1 1 1 0 0 1 1 0 1 0 0 0 1 0
# 0 0 1 0 1 0 1 1 0 1 1 0 1 0 1 0
# 1 0 1 0 1 1 0 1 1 0 1 0 0 1 0 0
# 1 1 0 0 1 0 1 0 1 0 0 1 0 0 0 0
# 1 1 0 0 0 1 1 1 0 1 0 1 1 1 1 0
# 0 0 0 1 0 1 0 0 0 1 1 0 0 0 0 1
# 0 1 0 0 0 0 0 1 0 1 1 0 0 0 0 0
# 0 1 1 1 1 1 0 1 1 0 0 0 0 0 0 0
# 0 1 0 0 1 1 1 1 1 0 0 1 1 0 1 1
# 1 0 1 1 1 1 1 0 1 1 1 1 1 0 1 0
# 0 0 1 1 0 0 1 1 0 0 0 1 0 0 0 1
# 0 1 1 1 1 1 1 0 1 0 1 0 0 0 1 0
# 1 1 0 1 0 0 1 1 1 1 1 0 1 0 0 1
# 0 0 0 0 1 0 1 0 0 0 1 1 1 1 0 0
# 1 1 1 0 0 1 0 0 0 0 0 1 1 1 0 1
# 1 1 0 1 1 0 0 1 0 1 1 1 1 0 1 0
# 1 0 1 1 1 0 0 0 0 0 1 0 1 0 1 1
# 1 1 0 0 0 1 0 0 1 0 0 0 1 1 0 0
# 1 1 1 0 0 0 1 0 1 1 0 0 0 1 0 0
# 0 1 1 0 1 1 0 0 1 1 1 0 1 0 1 0
# 1 1 1 0 1 1 0 0 1 0 1 1 1 0 1 1
# 0 0 1 0 1 0 0 1 0 1 0 0 1 0 0 1
# 1 0 1 0 1 1 1 1 0 1 1 1 0 0 0 0
# 0 0 0 0 1 0 1 1 0 1 1 0 1 1 1 0
# 0 1 0 1 1 0 1 0 0 0 0 0 1 0 1 1
# 1 0 0 1 0 0 1 1 0 0 0 0 1 0 1 0
# 0 0 0 0 0 1 1 1 0 1 1 1 0 0 0 1
# 1 1 1 0 1 0 0 1 1 1 1 1 0 0 1 1
# 0 1 0 0 1 0 1 1 1 1 1 1 0 0 1 1
# 1 0 0 0 1 0 1 1 1 1 1 1 0 1 1 1
# 0 1 0 1 0 1 0 0 1 0 0 0 1 0 1 1
# 0 0 1 1 0 0 0 1 1 0 1 1 0 0 0 1
# 0 1 0 1 0 1 1 0 0 1 1 0 0 0 1 1
# 1 1 0 0 1 0 1 1 1 1 1 0 1 1 1 0
# 1 1 0 1 0 1 0 1 1 1 1 1 0 1 0 1
# 1 1 1 0 0 0 0 0 0 0 1 0 1 1 1 1
# 1 0 0 1 0 0 1 1 1 0 1 1 1 0 0 1
# 0 1 1 1 0 1 1 1 0 0 0 0 1 1 1 1
# 0 0 0 1 1 0 0 0 0 1 1 0 0 1 0 1
# 1 0 0 0 0 0 1 1 0 0 1 1 1 1 1 1
# 0 1 1 1 0 0 0 1 0 0 0 0 0 1 1 0
# 1 0 1 0 0 0 1 0 0 1 0 1 1 0 1 0
# 0 1 0 0 0 1 1 0 0 1 1 1 0 1 0 1
# 0 1 0 1 1 0 1 0 1 0 1 0 0 0 0 0
# 1 0 1 0 0 0 0 0 0 1 1 0 1 0 0 0
# 0 1 1 1 1 1 0 0 1 1 0 1 1 1 1 0
# 0 0 0 0 0 0 0 1 1 0 1 1 0 1 1 0
# 0 0 0 0 1 1 0 1 0 1 1 0 0 0 1 0
# 1 1 1 0 1 1 1 0 0 0 1 0 1 0 1 0
# 1 1 1 1 0 1 1 0 0 1 1 1 1 0 1 0
# 1 0 1 0 1 0 1 0 0 0 0 0 1 1 0 0
# 0 0 1 1 0 0 0 1 0 0 0 0 0 0 0 1
# 0 0 1 1 1 1 1 0 0 1 1 1 1 0 0 0
# 1 0 1 0 1 0 0 1 1 0 0 0 1 1 1 0
# 1 0 1 0 1 1 0 1 1 0 0 1 0 1 1 1'''
#         lines = text.splitlines()
        
        first_splitted = lines[0].strip('\n').split(' ')
        self.number_of_nodes, self.number_of_bits = int(first_splitted[0]), int(first_splitted[1])

        self.node_bits_values = {}
        for index, line in enumerate(lines[1:]):
            bits = line.strip('\n').replace(' ', '')
            value = int(bits, base=2)
            if (self.node_bits_values.get(value)):
                self.node_bits_values[value].append(index)
            else:
                self.node_bits_values[value] = [index]
            
    def get_hamming_distance(self, x, y):
        return bin(x ^ y).count('1')
            
Clustering().execute()