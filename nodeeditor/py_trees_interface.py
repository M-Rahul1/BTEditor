import py_trees as pt

class Node:
    def __init__(self, op_title, children=None):
        self.op_title = op_title
        self.children = children if children else []

    def get_pytrees(self):
        # 1. Create the corresponding PyTrees object
        py_trees_object = self.getnode()

        # 2. Call the same recursive function for every child
        for node in self.getChildrenNodes():
            child_py_trees = node.get_pytrees()
            py_trees_object.add_child(child_py_trees)

        # 4. Return the PyTrees object
        return py_trees_object

    def getnode(self):
        if self.op_title == "Sequence":
            return pt.composites.Sequence(name=self.op_title, memory=False, children=[])
        elif self.op_title == "Fallback":
            return pt.composites.Selector(name=self.op_title, memory=False, children=[])
        elif self.op_title == "Action":
            return pt.behaviour.Behaviour(name=self.op_title)

    def getChildrenNodes(self, node):
        children_nodes = []
        for output_socket in node.outputs:
            for edge in output_socket.edges:
                other_node = edge.getOtherSocket(output_socket).node
                children_nodes.append(other_node)
        return children_nodes
