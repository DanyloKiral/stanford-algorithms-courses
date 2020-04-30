import time
import datetime

class SCCs:
    def __init__(self):
        super().__init__()
        
        self.list_of_edges = {}
        self.number_of_vertices = 0
        self.edges_map = {}
        
        self.explored_vertices = {}
        self.processed_vertices_number = 0
    
    def execute(self):
        self.compute_sccs_kasaraju()
        
    def compute_sccs_kasaraju(self):
        input_read_start_time = time.perf_counter()      
        text_file = open("graph-strongly-connected-components-computation-input.txt", "r")
        lines = text_file.readlines()
        
#         input_str = '''1 2

# 2 3

# 3 1

# 3 4

# 5 4

# 6 4

# 8 6

# 6 7

# 7 8''' ## 3,3,1,1
        
#         lines = input_str.split("\n\n")

        self.number_of_vertices = 0 
        self.list_of_edges = {}
        self.edges_map = {}
        reversed_list_of_edges = {}
        reversed_edges_map = {}
        for index, line in enumerate(lines):
            text_input = line.split(" ")
            first = int(text_input[0])
            second = int(text_input[1])
            self.number_of_vertices = max(self.number_of_vertices, first, second)
            
            self.list_of_edges[index] = (first, second)
            if (first not in self.edges_map):
                self.edges_map[first] = []
            self.edges_map[first].append(index)
            
            reversed_list_of_edges[index] = (second, first)
            if (second not in reversed_edges_map):
                reversed_edges_map[second] = []
            reversed_edges_map[second].append(index)
            
            
        input_read_end_time = time.perf_counter()  

        print("Input read time = " + str(input_read_end_time - input_read_start_time) + "s")  
                 
        # list with bool values, indicating if vertex explored (starting from 1 to [vertices_number], ignore 0 index)
        start_time = time.perf_counter()    
        
        print("starting first pass")
        finishing_times, _ = self.depth_first_search_loop(reversed_list_of_edges, reversed_edges_map, self.number_of_vertices)
        first_pass_finished_time = time.perf_counter()
        print("first pass finished. Time = " + str(first_pass_finished_time - start_time) + "s")
        
        print("starting to replace nodes with finish times")
        edges_with_fin_times, edges_map_with_fin_times = self.replace_nodes_with_finishing_times(self.list_of_edges, self.edges_map, finishing_times)    
        replacing_finishing_times_in_edges_finish_time = time.perf_counter() 
        print("replace nodes with finish times finished. Time = " + str(replacing_finishing_times_in_edges_finish_time - first_pass_finished_time) + "s")
        
        print("starting second pass with finishing times")
        _, leaders = self.depth_first_search_loop(edges_with_fin_times, edges_map_with_fin_times, self.number_of_vertices) 
        second_pass_finished_time = time.perf_counter()
        print("second pass finished. Time = " + str(second_pass_finished_time - replacing_finishing_times_in_edges_finish_time) + "s")
        
        print("starting to reverse finishing time in result")
        result = self.reverse_finishing_times_in_result(leaders, finishing_times)
        fixing_result_finished_time = time.perf_counter()
        print("reverse finishing time in result finished. Time = " + str(fixing_result_finished_time - second_pass_finished_time) + "s")
        
        process_time = fixing_result_finished_time - start_time
        print("Whole process time = " + str(process_time) + "s")
        
        self.process_results(result, process_time)
        
    #
    def process_results(self, result, process_time):
        print("Count of SCCs = " + str(len(result)))
        
        def result_sort(scc):
            return len(scc[1])
        
        result.sort(key=result_sort, reverse=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = open("graph-strongly-connected-components-computation-" + timestamp + ".txt","w+")
        
        i = 1
        for scc in result:
            output_file.write("# SCC #" + str(i) + ": \n")
            # output_file.write(str(scc[0]))
            # output_file.write(": ")
            # output_file.write(str(scc[1]))
            # output_file.write("\n")
            output_file.write("Count of vertices in SCC = " + str(len(scc[1])))
            output_file.write("\n")
            i += 1
            
        output_file.write("Summary \n")
        output_file.write("Count of SCCs = " + str(len(result)) + "\n")
        output_file.write("Process time = " + str(process_time) + "s \n")
        
        output_file.close()
        
    #    
    def depth_first_search_loop(self, graph_edges, edges_map, vertices_number):
        self.processed_vertices_number = 0
        finishing_times = {}
        for index in range(vertices_number + 1):
            self.explored_vertices[index] = False
            finishing_times[index] = 0
        leaders = {}
        
        def dfs_iterative(start_node):
            self.explored_vertices[start_node] = True
            scc = [start_node]
            nodes_stack = [start_node]
            while len(nodes_stack) > 0:
                current_node = nodes_stack.pop()
                found_next_node = False
                if (current_node in edges_map):
                    for edge_index in edges_map[current_node]:
                        next_edge = graph_edges[edge_index]
                        if (not self.explored_vertices[next_edge[1]]):
                            self.explored_vertices[next_edge[1]] = True
                            nodes_stack.append(current_node)
                            nodes_stack.append(next_edge[1])
                            scc.append(next_edge[1])
                            found_next_node = True
                            break

                if (not found_next_node):
                    self.processed_vertices_number += 1
                    finishing_times[current_node] = self.processed_vertices_number
    
            return scc
            
        for i in range(vertices_number, 0, -1):
            if (not self.explored_vertices[i]):
                connected_nodes = dfs_iterative(i)
                leaders[i] = connected_nodes
        return (finishing_times, leaders)    
    
    #
    def replace_nodes_with_finishing_times(self, edges, edges_map, finishing_times):
        edges_with_finishing_times = {}
        for key, value in edges.items():
            edges_with_finishing_times[key] = (finishing_times[value[0]], finishing_times[value[1]]) 
        map_with_finishing_times = {}
        for key, value in edges_map.items():
            map_with_finishing_times[finishing_times[key]] = value
        return (edges_with_finishing_times, map_with_finishing_times)

    # 
    def reverse_finishing_times_in_result(self, result, finishing_times):
        length = len(finishing_times)
        back_finishing_times = [0 for _ in range(length)]
        for index in range(1, length):
            back_finishing_times[finishing_times[index]] = index
        
        fixed_result = []
        
        for leader, scc in result.items():
            fixed_scc = (back_finishing_times[leader], [back_finishing_times[n] for n in scc])
            fixed_result.append(fixed_scc)
            
        return fixed_result
        
    #
    def reverse_graph(self, list_of_edges):
        reversed_list_of_edges = [(edge[1], edge[0]) for edge in list_of_edges]
        return reversed_list_of_edges
       

SCCs().execute()