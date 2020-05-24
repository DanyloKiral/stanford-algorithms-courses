import math

class Heap:
    def __init__(self):
        super().__init__()
        self._length = 0
        self._heap_key_array = {}
        self._head_value_dictionary = {}
        
    # compared by value
    def push(self, key, value):
        new_item_index = self._length
        self._heap_key_array[new_item_index] = key
        self._head_value_dictionary[key] = value
        self._length += 1
        self._bubble_up_til_valid(new_item_index)
        
    def pop(self):
        if self._length == 0:
            return None
        root_item_key = self._heap_key_array[0]
        self._heap_key_array[0] = self._heap_key_array[self._length - 1]
        self._heap_key_array.pop(self._length - 1)
        self._length -= 1
        self._bubble_down_til_valid(0)
        return root_item_key, self._head_value_dictionary.pop(root_item_key)
    
    def get(self):
        if (self._length == 0):
            return None
        root_item_key = self._heap_key_array[0]
        return (root_item_key, self._head_value_dictionary[root_item_key])
    
    def length(self):
        return self._length
        
    def remove(self, key_to_remove):
        if (self._length == 0):
            return None
        index_to_remove = None
        for index, key in self._heap_key_array.items():
            if key == key_to_remove:
                index_to_remove = index
                break
        self._heap_key_array[index_to_remove] = self._heap_key_array[self._length - 1]
        self._heap_key_array.pop(self._length - 1)
        self._length -= 1
        self._bubble_down_til_valid(index_to_remove)
        return self._head_value_dictionary.pop(key_to_remove)
        
            
    def _bubble_up_til_valid(self, child_index):
        should_proceed = True
        while (should_proceed):
            parent_index = self._get_parent_index(child_index)
            parent_key = self._heap_key_array[parent_index]
            child_key = self._heap_key_array[child_index]
            
            should_proceed = self.compare(child_key, parent_key) < 0
            if (should_proceed):
                self._heap_key_array[child_index], self._heap_key_array[parent_index] = parent_key, child_key
                child_index = parent_index
            
    def _bubble_down_til_valid(self, parent_index):
        should_proceed = True
        while (should_proceed):
            children_indexes = self._get_children_indexes(parent_index)
            if (not children_indexes):
                return
            parent_key = self._heap_key_array[parent_index]
            first_child = (children_indexes[0], self._heap_key_array[children_indexes[0]])
            second_child = (children_indexes[1], self._heap_key_array[children_indexes[1]]) if children_indexes[1] else None
            smaller_child = first_child if not second_child or (self.compare(first_child[1], second_child[1]) < 0) else second_child
            
            should_proceed = self.compare(smaller_child[1], parent_key) < 0
            if (should_proceed):
                self._heap_key_array[smaller_child[0]], self._heap_key_array[parent_index] = parent_key, smaller_child[1]
                parent_index = smaller_child[0]
                
    def compare(self, first_key, second_key):
        first_value = self._head_value_dictionary[first_key]
        second_value = self._head_value_dictionary[second_key]
        if (first_value < second_value):
            return -1
        elif (first_value > second_value):
            return 1
        else:
            return 0
        
    def _get_parent_index(self, child_index):
        return math.floor(child_index / 2)
    
    def _get_children_indexes(self, parent_index):
        first_child = parent_index * 2
        if (first_child < self._length - 1):
            return (first_child, first_child + 1)
        elif (first_child < self._length):
            return (first_child, None)
        return None