import random
import copy

text_file = open("graph_min_cut_input.txt", "r")
lines = text_file.readlines()

adjacency_list_input = {}

for row in lines:
    splitted = row.split("\t")
    adjacency_list_input[int(splitted[0])] = [int(num) for num in splitted[1:-1]]

def calc_min_cut(adjacency_list):
    merged_vertices = {}

    def findVertixAlreadyMergedIn(vert):
        for key in list(merged_vertices.keys()):
            if (vert in merged_vertices[key]):
                return key
        return 0

    def contraction():
        # choose random edge (pair of vertices)
        random_vert = random.choice(list(adjacency_list.keys()))
        random_vert2 = random.choice(adjacency_list[random_vert])

        merged_in = findVertixAlreadyMergedIn(random_vert2)
        if (merged_in > 0):
            random_vert2 = merged_in

        # record to merged_vertices
        vert_merged_values = merged_vertices.pop(random_vert, [])
        vert2_merged_values = merged_vertices.pop(random_vert2, [])
        merged_vertices[random_vert] = vert_merged_values + vert2_merged_values + [random_vert2]

        # merge without self loops
        adjacency_list[random_vert] = [v for v in (adjacency_list[random_vert] + adjacency_list.pop(random_vert2, [])) \
            if v != random_vert and v != random_vert2 and v not in merged_vertices[random_vert]]
    
    while len(adjacency_list) > 2:
        contraction()

    print("end")
        
    keys = list(adjacency_list.keys())

    # map adjacency list only to existing(merged) nodes
    if (keys[1] in merged_vertices): 
        for i in range(len(adjacency_list[keys[0]])):
            if (adjacency_list[keys[0]][i] in merged_vertices[keys[1]]):
                adjacency_list[keys[0]][i] = keys[1]

    if (keys[0] in merged_vertices): 
        for i in range(len(adjacency_list[keys[1]])):
            if (adjacency_list[keys[1]][i] in merged_vertices[keys[0]]):
                adjacency_list[keys[1]][i] = keys[0]

    # both should be same
    local_min_cut = max(adjacency_list[keys[0]].count(keys[1]), adjacency_list[keys[1]].count(keys[0]))
    print("local min cut: " + str(local_min_cut))

    return local_min_cut

min_cut = len(adjacency_list_input)

for i in lines:
    result = calc_min_cut(copy.deepcopy(adjacency_list_input))
    min_cut =  min(min_cut, result) if result > 0 else min_cut

print("end of iterations")

print("final min cut: " + str(min_cut))




    