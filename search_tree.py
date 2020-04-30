class TreeNode:
    def __init__(self, parent, key):
        super().__init__()
        self.key = key
        self.parent = parent
        self.left_child = None
        self.right_child = None
        self.rank = 1
        
    def recalculate_rank(self):
        self.rank = 1
        if (self.left_child):
            self.rank += self.left_child.recalculate_rank()
        if (self.right_child):
            self.rank += self.right_child.recalculate_rank()         
        return self.rank
    
    def insert(self, key):
        if (self.key == key):
            raise Exception("Duplicates are not allowed")
        self.rank += 1
        if (key < self.key):
            if (self.left_child):
                self.left_child.insert(key)
            else:
                self.left_child = TreeNode(self, key)
        else:
            if (self.right_child):
                self.right_child.insert(key)
            else:
                self.right_child = TreeNode(self, key)
                
    def select(self, i):
        left_child_rank = self.left_child.rank if (self.left_child) else 0
        if (left_child_rank == i - 1):
            return self.key
        if (left_child_rank >= i):
            return self.left_child.select(i)
        if (left_child_rank < i - 1):
            return self.right_child.select(i - left_child_rank - 1)
        
class SearchTree:
    def __init__(self):
        super().__init__()
        self.root = None
        
    def insert(self, key):
        if (not self.root):
            self.root = TreeNode(None, key)
            return
        self.root.insert(key)
        
    def select(self, i):
        if (not self.root):
            return None
        return self.root.select(i)