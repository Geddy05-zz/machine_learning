class Node:
    name = None
    children = []
    subset = []
    is_correct_node = None
    #
    # lambda =x {} predicate

    def __init__(self,name):
        self.name = name

    def add_child(self,value):
        self.children.append(value)

    def has_children(self):
        return len(self.children) > 0

class Leaf:
    name = None

    def __init__(self,name):
        self.name = name