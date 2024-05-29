"""import os
import py_trees as pt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from py_trees.common import Status
from bteditor.conf import *
from bteditor.node_base import *
from nodeeditor.utils import dumpException

class CalcGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 100
        self.height = 50
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_height = 30.0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10
    
class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("Condition", self)
        self.edit.setAlignment(Qt.AlignCenter)
        self.edit.setObjectName(self.node.content_label_objname)
        self.edit.hide()

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(str(value))
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(ROOT)
class Root(CalcNode, pt.composites.Sequence):
    icon = os.path.join(os.path.dirname(__file__), 'icons/action.png')
    op_code = ROOT
    op_title = "Root"
    content_label_objname = "root_node"

    def __init__(self, scene):
        CalcNode.__init__(self, scene, inputs=[], outputs=[1])
        pt.composites.Sequence.__init__(self, name="Sequence",memory=False, children=[])
        self.eval()

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)
    
    def evalImplementation(self):
        u_value = self.content.edit.text()
        s_value = u_value
        self.value = s_value
        self.markDirty(False)
        self.markInvalid(False)   

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value    
    
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status:
        return super().update()
    
    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)
    
 """