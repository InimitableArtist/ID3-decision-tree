class Node:
    
    def __init__(self, value, parent = None):
        self.value = value
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, list_of_children):
        for child in list_of_children:
            self.add_child(child)

    def __repr__(self):
        return self.value

    def getChildren(self):
        return self.children
    
    def getValue(self):
        return self.value
    
    def getParent(self):
        return self.parent

