from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from bteditor.calc_conf import *
from bteditor.calc_node_base import *
from nodeeditor.utils import dumpException

class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit("Condition", self)
        self.edit.setAlignment(Qt.AlignCenter)
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

@register_node(SEQUENCE)
class Sequence(CalcNode):
    icon = "icons/right_arrow.png"
    op_code = SEQUENCE
    op_title = "Sequence"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        u_value = self.content.edit.text()
        s_value = int(u_value)
        self.value = s_value
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value


@register_node(FALLBACK)
class Fallback(CalcNode):
    icon = "icons/question.png"
    op_code = FALLBACK
    op_title = "Fallback"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        u_value = self.content.edit.text()
        s_value = int(u_value)
        self.value = s_value
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value


# way how to register by function call
# register_node_now(SEQUENCE, Sequence)