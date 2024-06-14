from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_socket import TOP_CENTER, BOTTOM_CENTER
from nodeeditor.utils import dumpException
import py_trees as pt
import bteditor.nodes.actions as action


class CalcGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("icons/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )

def sort_nodes_by_pos_x(nodes):
    """
    Sorts the given list of nodes by their pos_x value.

    :param nodes: List of nodes to be sorted.
    :return: Sorted list of nodes.
    """
    return sorted(nodes, key=lambda node: node.pos.x())

class CalcContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class CalcNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    GraphicsNode_class = CalcGraphicsNode
    NodeContent_class = CalcContent

    def __init__(self, scene, inputs=[2,2], outputs=[1]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.value = None

        # it's really important to mark all nodes Dirty by default
        self.markDirty()
                          
        
    def get_pytrees(self):
        # 1. Create the corresponding PyTrees object
        self.py_trees_object = self.getnode()
        
        # 2. Call the same recursive function for every child
        
        for node in self.getChildrenNodes():
            child_py_trees = node.get_pytrees()
            self.py_trees_object.add_child(child_py_trees)
            #print(self.py_trees_object)
        # 4. Return the PyTrees object
        return self.py_trees_object
    
    def getnode(self):
        try:
            
            if self.op_title == "Root":
                return pt.composites.Sequence(name=self.op_title, memory=False, children=[])
            elif self.op_title == "Sequence":
                return pt.composites.Sequence(name=self.op_title, memory=False, children=[])
            elif self.op_title == "Fallback":
                return pt.composites.Selector(name=self.op_title, memory=False, children=[])
            elif self.op_title == "Parallel":
                return pt.composites.Parallel(name=self.op_title, policy="", children=[])
            elif self.op_title == "No_traffic_light?":
                return action.No_traffic_light_(name=self.op_title)
            elif self.op_title == "Light_is_red?":
                #if completion_status=pt.common.Status.SUCCESS change to failure and vice versa
                return action.Light_is_red_(name=self.op_title, duration=5, completion_status=pt.common.Status.SUCCESS)
            elif self.op_title == "Light_is_green?":
                return action.Light_is_green_(name=self.op_title, duration=5, completion_status=pt.common.Status.SUCCESS)
            elif self.op_title == "Light_is_yellow?":
                return action.Light_is_yellow_(name=self.op_title, duration=5, completion_status=pt.common.Status.SUCCESS)
            elif self.op_title == "Within_lane?":
                return action.Within_lane_(name=self.op_title)
            elif self.op_title == "Stop":
                return action.Stop_(name=self.op_title, duration=10, completion_status=pt.common.Status.SUCCESS)
            elif self.op_title == "Proceed":
                return action.Proceed_(name=self.op_title, duration=10, completion_status=pt.common.Status.SUCCESS)
            elif self.op_title == "Caution":
                return action.Caution_(name=self.op_title, duration=10, completion_status=pt.common.Status.SUCCESS)
            elif self.op_title == "Move_into_lane":
                return action.Move_into_lane_(name=self.op_title, duration=10, completion_status=pt.common.Status.SUCCESS)
            elif self.op_title == "Keep_driving":
                return action.Keep_driving_(name=self.op_title, duration=10, completion_status=pt.common.Status.SUCCESS)
            
            elif self.op_title == "Is_coffee_ready?":
                return action.Is_coffee_ready_(name=self.op_title)
            elif self.op_title == "Has_coffee?":
                return action.Has_coffee_(name=self.op_title)
            elif self.op_title == "Has_milk?":
                return action.Has_milk_(name=self.op_title)
            elif self.op_title == "Has_sugar?":
                return action.Has_sugar_(name=self.op_title)
            elif self.op_title == "Add_coffee!":
                return action.Add_coffee_(name=self.op_title, duration=10, completion_status=pt.common.Status.SUCCESS)
            elif self.op_title == "Add_milk!":
                return action.Add_milk_(name=self.op_title, duration=10, completion_status=pt.common.Status.SUCCESS)
            elif self.op_title == "Add_sugar!":
                return action.Add_sugar_(name=self.op_title, duration=10, completion_status=pt.common.Status.SUCCESS)
            else :
                print("Invalid node")                    
        except Exception as e:
            print(e)
            return None
            


    def getChildrenNodes(self):
        children_nodes = []
        for output_socket in self.outputs:
            for edge in output_socket.edges:
                other_node = edge.getOtherSocket(output_socket).node
                children_nodes.append(other_node)
                #print(children_nodes)
        #sort chilren nodes according to their pos_x
        children_nodes = sort_nodes_by_pos_x(children_nodes)
        return children_nodes
    
    def initSettings(self):
        super().initSettings()
        self.input_socket_position = TOP_CENTER
        self.output_socket_position = BOTTOM_CENTER

    def evalOperation(self, input1, input2):
        return 123

    def evalImplementation(self):
        i1 = self.getInput(0)
        i2 = self.getInput(1)

        if i1 is None or i2 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None

        else:
            val = self.evalOperation(i1.eval(), i2.eval())
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
            return self.value

        try:

            val = self.evalImplementation()
            return val
        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)

    def onInputChanged(self, socket=None):
        print("%s:: InputChanged" % self.__class__.__name__)
        self.markDirty()
        self.eval()


    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res