from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from bteditor.conf import *
from bteditor.node_base import *
from nodeeditor.utils import dumpException
import py_trees as pt

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

@register_node(CUBE_IN_DELIVERY)
class Cube_in_delivery(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/thunder.png"
    op_code = CUBE_IN_DELIVERY
    op_title = "Cube_in_delivery"
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

class Cube_in_delivery_(pt.behaviour.Behaviour):   

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS
@register_node(CUBE_IN_HAND)
class Cube_in_hand(CalcNode,pt.behaviour.Behaviour):
    
    icon = "icons/thunder.png"
    op_code = CUBE_IN_HAND
    op_title = "Cube_in_hand"
    content_label_objname = "place_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Cube_in_hand?")
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

class Cube_in_hand_(pt.behaviour.Behaviour): 
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS  


@register_node(ROBOT_AT_CUBE)
class Robot_at_cube(CalcNode):
    icon = "icons/thunder.png"
    op_code = ROBOT_AT_CUBE
    op_title = "Robot_at_cube"
    content_label_objname = "move_to_station_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Robot_at_cube")
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

class Robot_at_cube_(pt.behaviour.Behaviour):   

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS
    
@register_node(MOVE_TO_CUBE)
class Move_to_cube(CalcNode):
    icon = "icons/thunder.png"
    op_code = MOVE_TO_CUBE
    op_title = "Move_to_cube"
    content_label_objname = "move_to_obj_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Move_to_cube")
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

class Move_to_cube_(pt.behaviour.Behaviour):   

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS

    
@register_node(PICK_CUBE)
class Pick_cube(CalcNode,pt.behaviour.Behaviour):
    
    icon = "icons/thunder.png"
    op_code = PICK_CUBE
    op_title = "Pick_cube"
    content_label_objname = "place_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Pick_cube?")
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

class Pick_cube_(pt.behaviour.Behaviour):   

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS

@register_node(ROBOT_AT_DELIVERY)
class Robot_at_delivery(CalcNode,pt.behaviour.Behaviour):
    
    icon = "icons/thunder.png"
    op_code = ROBOT_AT_DELIVERY
    op_title = "Robot_at_delivery"
    content_label_objname = "place_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Robot_at_delivery?")
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

class Robot_at_delivery_(pt.behaviour.Behaviour):   

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS

@register_node(MOVE_TO_DELIVERY)
class Move_to_delivery(CalcNode,pt.behaviour.Behaviour):
    
    icon = "icons/thunder.png"
    op_code = MOVE_TO_DELIVERY
    op_title = "Move_to_delivery"
    content_label_objname = "place_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Move_to_delivery?")
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

class Move_to_delivery_(pt.behaviour.Behaviour):   

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS
@register_node(PLACE_CUBE)
class Place_cube(CalcNode,pt.behaviour.Behaviour):
    
    icon = "icons/thunder.png"
    op_code = PLACE_CUBE
    op_title = "Place_cube"
    content_label_objname = "place_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Place_cube?")
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

class Place_cube_(pt.behaviour.Behaviour):   

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS
