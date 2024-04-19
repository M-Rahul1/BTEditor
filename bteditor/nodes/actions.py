from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from py_trees.common import Status
from bteditor.conf import *
from bteditor.node_base import *
from nodeeditor.utils import dumpException
import py_trees as pt

class CalcOutputContent(QDMNodeContentWidget):
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
    
    
    def update(self):
        return pt.common.Status.SUCCESS
    
    
    
    def initInnerClasses(self):
        self.content = CalcOutputContent(self)
        self.grNode = CalcGraphicsNode(self)

    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return

        val = input_node.eval()

        if val is None:
            self.grNode.setToolTip("Input is NaN")
            self.markInvalid()
            return

        self.content.edit.setText("%d" % val)
        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        return val

class Pick(pt.behaviour.Behaviour):
    

    def update(self):
        return pt.common.Status.SUCCESS
