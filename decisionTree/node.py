class Node:
    name = None
    children = {}

    def __init__(self,name):
        self.name = name

    def add_child(self,key,value):
        self.children[key] = value

    def has_children(self):
        return len(self.children) > 0