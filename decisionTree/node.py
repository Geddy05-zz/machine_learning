class Node:
    name = None
    children = []
    #
    # lambda =x {} predicate

    def __init__(self,name):
        self.name = name

    def add_child(self,value):
        self.children.append(value)

    def has_children(self):
        return len(self.children) > 0