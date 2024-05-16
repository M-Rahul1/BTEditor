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

@register_node(CUBE2_DELIVERED)
class Cube2_delivered(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = CUBE2_DELIVERED
    op_title = "Cube2_delivered?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Cube2_delivered")
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

class Cube2_delivered_(pt.behaviour.Behaviour):   
    

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE

@register_node(CUBE2_IN_HAND)
class Cube2_in_hand(CalcNode,pt.behaviour.Behaviour):
    
    icon = "icons/action.png"
    op_code = CUBE2_IN_HAND
    op_title = "Cube2_in_hand?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Cube2_in_hand")
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

class Cube2_in_hand_(pt.behaviour.Behaviour):   
    

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(ROBOT_AT_CUBE2)
class Robot_at_cube2(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = ROBOT_AT_CUBE2
    op_title = "Robot_at_cube2?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Robot_at_cube2")
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

class Robot_at_cube2_(pt.behaviour.Behaviour): 
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS  
    
@register_node(MOVE_TO_CUBE2)
class Move_to_cube2(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = MOVE_TO_CUBE2
    op_title = "Move_to_cube2!"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Move_to_cube2", duration=10, completion_status=pt.common.Status.SUCCESS)
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
class Move_to_cube2_(pt.behaviours.TickCounter):   

    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass
    
@register_node(PICK_CUBE2)
class Pick_cube2(CalcNode,pt.behaviours.TickCounter):
    
    icon = "icons/action.png"
    op_code = PICK_CUBE2
    op_title = "Pick_cube2!"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Pick_cube2?", duration=10, completion_status=pt.common.Status.SUCCESS)
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

class Pick_cube2_(pt.behaviours.TickCounter):   

    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass

@register_node(ROBOT_AT_DELIVERY)
class Robot_at_delivery(CalcNode,pt.behaviour.Behaviour):
    
    icon = "icons/action.png"
    op_code = ROBOT_AT_DELIVERY
    op_title = "Robot_at_delivery?"
    content_label_objname = "action_node"

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

    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS

@register_node(MOVE_TO_DELIVERY)
class Move_to_delivery(CalcNode,pt.behaviours.TickCounter):
    
    icon = "icons/action.png"
    op_code = MOVE_TO_DELIVERY
    op_title = "Move_to_delivery!"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Move_to_delivery?", duration=10, completion_status=pt.common.Status.SUCCESS)
        self.eval()
    
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

class Move_to_delivery_(pt.behaviours.TickCounter):   
    
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass
        
@register_node(PLACE_CUBE2)
class Place_cube2(CalcNode,pt.behaviours.TickCounter):
    
    icon = "icons/action.png"
    op_code = PLACE_CUBE2
    op_title = "Place_cube2!"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Place_cube2", duration=10, completion_status=pt.common.Status.SUCCESS)
        self.eval()
    
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

class Place_cube2_(pt.behaviours.TickCounter):   
    
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass
