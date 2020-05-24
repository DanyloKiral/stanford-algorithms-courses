from heap import Heap

plus_infinity = float("inf")

class TreeNode:
    def __init__(self, index: int, weight: int):
        super().__init__()
        self.index: int = index
        self.weight: int = weight
        
        self.parent: TreeNode = None
        
        self.left_child: TreeNode = None
        self.right_child: TreeNode = None

class HuffmanCodes:
    def __init__(self):
        super().__init__()
        self.number_of_symbols = 0
        self.symbol_weights = {}
        self.tree_nodes = {}
        self.codes = {}
        
    def execute(self):
        self.read_input()
        heap = Heap()
        for index, symbol_weight in self.symbol_weights.items():
            heap.push(str(index), symbol_weight)
            self.tree_nodes[str(index)] = TreeNode(index, symbol_weight)
            
        tree_root = self.building_tree_huffman(heap)
        self.fill_codes_by_tree(tree_root, '')
        
        min_value, max_value = self.get_min_max_codes_length()
        print('min = ' + str(min_value))
        print('max = ' + str(max_value))
    
    def get_min_max_codes_length(self):
        min_value = plus_infinity
        max_value = 0
        for code in self.codes.values():
            length = len(code)
            if (length > max_value):
                max_value = length
            if (length < min_value):
                min_value = length
        return (min_value, max_value)
        
    def fill_codes_by_tree(self, root: TreeNode, prefix: str):
        if (not root):
            return
        if (not root.index == None):
            self.codes[root.index] = prefix
            return
        self.fill_codes_by_tree(root.left_child, prefix + '0')
        self.fill_codes_by_tree(root.right_child, prefix + '1')
        
    def building_tree_huffman(self, heap: Heap) -> TreeNode:
        while (heap.length() > 1):
            a_key, a_weight = heap.pop()
            b_key, b_weight = heap.pop()
            merged_key = a_key + '_' + b_key
            merged_weight = a_weight + b_weight
            heap.push(merged_key, merged_weight)
            
            a_node = self.tree_nodes.pop(a_key)
            b_node = self.tree_nodes.pop(b_key)
            
            parent = TreeNode(None, None)
            parent.left_child, a_node.parent = a_node, parent
            parent.right_child, b_node.parent = b_node, parent
            self.tree_nodes[merged_key] = parent
        return self.tree_nodes[merged_key]
        
        
    def read_input(self):
        #text_file = open("huffman_codes_input.txt", "r")
        #lines = text_file.readlines()
#         lines = '''5

# 5

# 25

# 32

# 20

# 18'''.split('\n\n')

        lines = '''7

20

5

17

10

20

3

25'''.split('\n\n')
        
        self.number_of_symbols = int(lines[0])
        
        for index, line in enumerate(lines[1:]):
            self.symbol_weights[index] = int(line)
            
HuffmanCodes().execute()
        
        