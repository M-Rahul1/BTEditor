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

@register_node(NO_TRAFFIC_LIGHT)
class No_traffic_light(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = NO_TRAFFIC_LIGHT
    op_title = "No_traffic_light?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="No_traffic_light?")
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

class No_traffic_light_(pt.behaviour.Behaviour):   
    

    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE   
            
@register_node(WITHIN_LANE)
class Within_lane(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = WITHIN_LANE
    op_title = "Within_lane?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Within_lane?")
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
    
class Within_lane_(pt.behaviour.Behaviour):            
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.SUCCESS:
        return pt.common.Status.SUCCESS      
    
@register_node(LIGHT_IS_RED)
class Light_is_red(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = LIGHT_IS_RED
    op_title = "Light_is_red?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        #if completion_status=pt.common.Status.SUCCESS change to failure and vice versa
        
        pt.behaviours.TickCounter.__init__(self, name="Light_is_red?", duration=5, completion_status=pt.common.Status.SUCCESS)
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

class Light_is_red_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass

@register_node(LIGHT_IS_GREEN)
class Light_is_green(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = LIGHT_IS_GREEN
    op_title = "Light_is_green?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Light_is_green?", duration=5, completion_status=pt.common.Status.SUCCESS)
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
    
class Light_is_green_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass
    
@register_node(LIGHT_IS_YELLOW)
class Light_is_yellow(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = LIGHT_IS_YELLOW
    op_title = "Light_is_yellow?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Light_is_yellow?", duration=5, completion_status=pt.common.Status.SUCCESS)
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
    
class Light_is_yellow_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass
    
@register_node(STOP)
class Stop(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = STOP
    op_title = "Stop"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Stop", duration=10, completion_status=pt.common.Status.SUCCESS)
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

class Stop_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass 
          
@register_node(PROCEED)
class Proceed(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = PROCEED
    op_title = "Proceed"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Proceed", duration=10, completion_status=pt.common.Status.SUCCESS)
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

class Proceed_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass 
        
@register_node(CAUTION)
class Caution(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = CAUTION
    op_title = "Caution"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Caution", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Caution_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass 
        
@register_node(MOVE_INTO_LANE)
class Move_into_lane(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = MOVE_INTO_LANE
    op_title = "Move_into_lane"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Move_into_lane", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Move_into_lane_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass  
        
@register_node(KEEP_DRIVING)
class Keep_driving(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = KEEP_DRIVING
    op_title = "Keep_driving"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Keep_driving", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Keep_driving_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    def initialise(self) -> None:
        pass
                
@register_node(IS_COFFEE_READY)
class Is_coffee_ready(CalcNode,pt.behaviour.Behaviour):
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
class Has_coffee(CalcNode,pt.behaviour.Behaviour):
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
        
@register_node(NO_EMERGENCY)
class No_emergency(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = NO_EMERGENCY
    op_title = "No_emergency?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="No_emergency")
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
    
class No_emergency_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(MEDICINE_WITH_PATIENT)
class Medicine_with_patient(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = MEDICINE_WITH_PATIENT
    op_title = "Medicine_with_patient?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Medicine_with_patient")
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
    
class Medicine_with_patient_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(ROBOT_AT_MEDICINE)
class Robot_at_medicine(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = ROBOT_AT_MEDICINE
    op_title = "Robot_at_medicine?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Robot_at_medicine")
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
    
class Robot_at_medicine_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(ROBOT_AT_PATIENT)
class Robot_at_patient(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = ROBOT_AT_PATIENT
    op_title = "Robot_at_patient?"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Robot_at_patient")
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
    
class Robot_at_patient_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(MOVE_TO_PATIENT)
class Move_to_patient(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = MOVE_TO_PATIENT
    op_title = "Move_to_patient"
    content_label_objname = "action_node"

    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Move_to_patient", duration=10, completion_status=pt.common.Status.SUCCESS)
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

class Move_to_patient_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(ASSIST_PATIENT)
class Assist_patient(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = ASSIST_PATIENT
    op_title = "Assist_patient"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Assist_patient", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Assist_patient_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(MOVE_TO_MEDICINE)
class Move_to_medicine(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = MOVE_TO_MEDICINE
    op_title = "Move_to_medicine"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Move_to_medicine", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Move_to_medicine_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(PICK_UP_MEDICINE)
class Pick_up_medicine(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = PICK_UP_MEDICINE
    op_title = "Pick_up_medicine"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Pick_up_medicine", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Pick_up_medicine_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(DELIVER_MEDICINE)
class Deliver_medicine(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = DELIVER_MEDICINE
    op_title = "Deliver_medicine"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Deliver_medicine", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Deliver_medicine_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass   

@register_node(CRITICAL_SYSTEM_POWER)
class Critical_system_power(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = CRITICAL_SYSTEM_POWER
    op_title = "Critical_system_power?"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Critical_system_power")
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
    
class Critical_system_power_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(POWER_CRITICAL_SYSTEM)
class Power_critical_system(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = POWER_CRITICAL_SYSTEM
    op_title = "Power_critical_system"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Power_critical_system", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Power_critical_system_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(NOTIFY_ADMIN)
class Notify_admin(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = NOTIFY_ADMIN
    op_title = "Notify_admin"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Notify_admin", duration=5, completion_status=pt.common.Status.SUCCESS)
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
    
class Notify_admin_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(NO_EXCESS_RENEWABLE_ENERGY)
class No_excess_renewable_energy(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = NO_EXCESS_RENEWABLE_ENERGY
    op_title = "No_excess_renewable_energy?"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="No_excess_renewable_energy")
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
    
class No_excess_renewable_energy_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(STORE_EXCESS_ENERGY)
class Store_excess_energy(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = STORE_EXCESS_ENERGY
    op_title = "Store_excess_energy"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Store_excess_energy", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Store_excess_energy_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(NON_CRITICAL_SYSTEM_POWER)
class Non_critical_system_power(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = NON_CRITICAL_SYSTEM_POWER
    op_title = "Non_critical_system_power?"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Non_critical_system_power")
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
    
class Non_critical_system_power_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE

@register_node(POWER_NON_CRITICAL_SYSTEM)
class Power_non_critical_system(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = POWER_NON_CRITICAL_SYSTEM
    op_title = "Power_non_critical_system"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Power_non_critical_system", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Power_non_critical_system_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(NO_STORED_ENERGY_AVAILABLE)
class No_stored_energy_available(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = NO_STORED_ENERGY_AVAILABLE
    op_title = "No_stored_energy_available?"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="No_stored_energy_available")
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
    
class No_stored_energy_available_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(USE_STORED_ENERGY)
class Use_stored_energy(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = USE_STORED_ENERGY
    op_title = "Use_stored_energy"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Use_stored_energy", duration=10, completion_status=pt.common.Status.SUCCESS)
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
    
class Use_stored_energy_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(PARTS_IN_ASSEMBLY)
class Parts_in_assembly(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = PARTS_IN_ASSEMBLY
    op_title = "Parts_in_assembly?"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Parts_in_assembly")
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

class Parts_in_assembly_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    

@register_node(PICK_PARTS)
class Pick_parts(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = PICK_PARTS
    op_title = "Pick_parts"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Pick_parts", duration=2, completion_status=pt.common.Status.SUCCESS)
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

class Pick_parts_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(PLACE_PARTS_IN_ASSEMBLY)
class Place_parts_in_assembly(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = PLACE_PARTS_IN_ASSEMBLY
    op_title = "Place_parts_in_assembly"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Place_parts_in_assembly", duration=2, completion_status=pt.common.Status.SUCCESS)
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
    
class Place_parts_in_assembly_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(PRODUCT_ASSSEMBLED)
class Product_assembled(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = PRODUCT_ASSSEMBLED
    op_title = "Product_assembled?"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Product_assembled")
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
    
class Product_assembled_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(ASSEMBLE_PRODUCT)
class Assemble_product(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = ASSEMBLE_PRODUCT
    op_title = "Assemble_product"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Assemble_product", duration=2, completion_status=pt.common.Status.SUCCESS)
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
    
class Assemble_product_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(PRODUCTS_STORED)
class Products_stored(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = PRODUCTS_STORED
    op_title = "Products_stored?"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Products_stored")
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
    
class Products_stored_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    
@register_node(STORE_PRODUCT)
class Store_product(CalcNode,pt.behaviours.TickCounter):
    icon = "icons/action.png"
    op_code = STORE_PRODUCT
    op_title = "Store_product"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviours.TickCounter.__init__(self, name="Store_product", duration=2, completion_status=pt.common.Status.SUCCESS)
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
    
class Store_product_(pt.behaviours.TickCounter):
    def update(self) -> pt.common.Status:
        self.counter += 1
        if self.counter <= self.duration:
            return pt.common.Status.RUNNING
        else:
            return self.completion_status
    
    def initialise(self) -> None:
        pass
    
@register_node(PARTS_PICKED)
class Parts_picked(CalcNode,pt.behaviour.Behaviour):
    icon = "icons/action.png"
    op_code = PARTS_PICKED
    op_title = "Parts_picked?"
    content_label_objname = "action_node"
    
    def __init__(self, scene):
        CalcNode.__init__(self,scene, inputs=[1], outputs=[])
        pt.behaviour.Behaviour.__init__(self, name="Parts_picked")
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
    
class Parts_picked_(pt.behaviour.Behaviour):
    def initialise(self) -> None:
        return super().initialise()
    
    def update(self) -> pt.common.Status.FAILURE:
        return pt.common.Status.FAILURE
    