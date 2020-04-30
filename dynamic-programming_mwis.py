
# maximun-weight independent set
class Mwis:
    def __init__(self):
        super().__init__()
        self.indexes_to_check = [1, 2, 3, 4, 17, 117, 517, 997]
        self.number_of_vertices = 0
        self.vertices_weights = {}
        self.results = {}
        self.path = []
        
    def execute(self):
        self.read_input()
        self.calculate_results_set()
        self.reconstruct_mwis()
        
        result = ''
        for index in self.indexes_to_check:
            if (index in self.path):
                result += '1'
            else:
                result += '0'
            
        print('result = ' + result)
        
    def reconstruct_mwis(self):
        index = self.number_of_vertices
        while (index >= 1):
            if (self.results[index - 1] > (self.results[index - 2] + self.vertices_weights[index])):
                index -= 1
            else:
                self.path.append(index)
                index -= 2      
        
    def calculate_results_set(self):
        self.results[-1] = 0
        self.results[0] = 0
        self.results[1] = self.vertices_weights[1]
        for index in range(2, self.number_of_vertices + 1):
            self.results[index] = max(self.results[index - 1], self.results[index - 2] + self.vertices_weights[index])    
        
    def read_input(self):
        text_file = open("dynamic-programming_mwis_input.txt", "r")
        lines = text_file.readlines()
        
#         lines = '''10
# 280
# 618
# 762
# 908
# 409
# 34
# 59
# 277
# 246
# 779'''.splitlines()
        
        self.number_of_vertices = int(lines[0])
        
        for index, line in enumerate(lines[1:]):
            self.vertices_weights[index + 1] = int(line)
            
Mwis().execute()