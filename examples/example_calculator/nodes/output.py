from PyQt5.QtCore import *
from examples.example_calculator.calc_conf import *
from examples.example_calculator.calc_node_base import *
from nodeeditor.utils import dumpException


class CalcOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("Success/Fail", self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)


@register_node(ACTION)
class Action(CalcNode):
    icon = "icons/tunder.png"
    op_code = ACTION
    op_title = "Action"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

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
