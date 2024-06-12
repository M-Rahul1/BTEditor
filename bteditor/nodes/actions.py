from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from bteditor.conf import *
from bteditor.node_base import *
from nodeeditor.utils import dumpException
import py_trees as pt

class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit(self.node.op_title, self)
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

@register_node(IS_COFFEE_READY)
class Is_coffee_ready_(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = IS_COFFEE_READY
    op_title = "Is_coffee_ready?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Is_coffee_ready?")
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

class Is_coffee_ready_(pt.behaviour.Behaviour):   
    

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(HAS_COFFEE)
class Has_coffee_(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = HAS_COFFEE
    op_title = "Has_coffee?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Has_coffee?")
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

class Has_coffee_(pt.behaviour.Behaviour):   
    

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE

@register_node(HAS_MILK)
class Has_milk(CalcNode,pt.behaviour.Behaviour):
    
    icon = "icons/action.png"
    op_code = HAS_MILK
    op_title = "Has_milk?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Has_milk?")
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

class Has_milk_(pt.behaviour.Behaviour):   
    

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(HAS_SUGAR)
class Has_sugar(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = HAS_SUGAR
    op_title = "Has_sugar?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Has_sugar?")
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

class Has_sugar_(pt.behaviour.Behaviour): 
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE  
    
@register_node(ADD_COFFEE)
class Add_coffee(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = ADD_COFFEE
    op_title = "Add_coffee!"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Add_coffee!", duration=10, completion_status=pt.common.Status.SUCCESS)
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
class Add_coffee_(pt.behaviours.TickCounter):   

    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass
    
@register_node(ADD_MILK)
class Add_milk(CalcNode,pt.behaviours.TickCounter):
    
    icon = "icons/action.png"
    op_code = ADD_MILK
    op_title = "Add_milk!"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Add_milk!", duration=10, completion_status=pt.common.Status.SUCCESS)
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

class Add_milk_(pt.behaviours.TickCounter):   

    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass

@register_node(ADD_SUGAR)
class Add_sugar(CalcNode,pt.behaviours.TickCounter):
    
    icon = "icons/action.png"
    op_code = ADD_SUGAR
    op_title = "Add_sugar!"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Add_sugar!", duration=10, completion_status=pt.common.Status.SUCCESS)
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

class Add_sugar_(pt.behaviours.TickCounter):   
    
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass
        
