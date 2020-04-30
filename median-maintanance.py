from heap import Heap
from timer import start_timer
from search_tree import SearchTree

class HeapMedianMaintenance:
    def __init__(self):
        super().__init__()
        # returns max value
        self.left_heap = Heap()
        #return min value
        self.right_heap = Heap()
    
    def insert(self, key):
        current_median = self.get_median()
        if (current_median and key > current_median):
            self.right_heap.push(key, key)
            if ((self.right_heap.length() - self.left_heap.length()) > 0):
                right_min = self.right_heap.pop()[0]
                self.left_heap.push(-right_min, -right_min)
        else:
            self.left_heap.push(-key, -key)
            if ((self.left_heap.length() - self.right_heap.length()) > 1):
                left_max = self.left_heap.pop()[0]
                self.right_heap.push(-left_max, -left_max)
    
    def get_median(self):
        if (self.left_heap.length() == 0):
            if (self.right_heap.length() == 0):
                return None
            else:
                return self.right_heap.get()[0]
        return -self.left_heap.get()[0]

class Main:
    def __init__(self):
        super().__init__()
        
    def execute(self):
        input_stream = self.read_input()
        self.run_heap_implementation(input_stream)
        self.run_search_tree_implementation(input_stream)
        
    def run_heap_implementation(self, input_stream):
        heap_impl_timer = start_timer("Heap implementation")
        medians_sum = 0
        median_via_heap = HeapMedianMaintenance()
        for item in input_stream:
            median_via_heap.insert(item)
            median = median_via_heap.get_median()
            medians_sum += median
        heap_impl_timer["finish_timer"]()
        answer = medians_sum % 10000
        print("answer: " + str(answer))
        
    def run_search_tree_implementation(self, input_stream):
        tree_impl_timer = start_timer("Search tree implementation")
        current_length = 0
        medians_sum = 0
        tree = SearchTree()
        for item in input_stream:
            tree.insert(item)
            current_length += 1
            median = tree.select(self.get_median_index(current_length))
            medians_sum += median
        tree_impl_timer["finish_timer"]()
        answer = medians_sum % 10000
        print("answer: " + str(answer))
        
    def get_median_index(self, length):
        if (length % 2 > 0):
            return (length + 1) / 2
        else:
            return (length / 2)
        
    def read_input(self):
        read_input_timer = start_timer("reading input")
        text_file = open("median-maintanance-input.txt", "r")
        lines = text_file.readlines()
        
#         text = """6331

# 2793

# 1640

# 9290

# 225

# 625

# 6195

# 2303

# 5685

# 1354"""
#         lines = text.split("\n\n")
        read_input_timer["finish_timer"]()
        return [int(line) for line in lines]
    
Main().execute()