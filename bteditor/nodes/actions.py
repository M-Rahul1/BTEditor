from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from bteditor.conf import *
from bteditor.node_base import *
from nodeeditor.utils import dumpException
import py_trees as pt
import py_trees

class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("Success/Fail", self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)

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

@register_node(ACTION)
class Action(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/thunder.png"
    op_code = ACTION
    op_title = "Action"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Action")
        self.eval()

    def update(self) -> pt.common.Status:
        return super().update()
    
    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = CalcGraphicsNode(self)

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

class Turn(py_trees.behaviour.Behaviour):

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return super().update()
    
    def terminate(self) -> None:
        return super().terminate()