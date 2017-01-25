class Node(object):
    name = None
    children = []
    subset = []
    is_correct_node = None
    __value = None
    is_leaf = False
    #
    # lambda =x {} predicate

    def __init__(self,name,value):
        self.name = name
        self.children = []
        self.subset = []
        self.is_leaf = False
        self.is_correct_node=None
        self.__value = value

    def match(self,given):
        return given == self.__value

    def add_child_node(self, value):
        self.children.append(value)

    def has_children(self):
        return len(self.children) > 0