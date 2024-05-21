LISTBOX_MIMETYPE = "application/x-item"

ROOT = 0
FALLBACK = 1
SEQUENCE = 2
PARALLEL = 3
CUBE2_DELIVERED=5
CUBE2_IN_HAND=6
ROBOT_AT_CUBE2=7
MOVE_TO_CUBE2=8
PICK_CUBE2=9
ROBOT_AT_DELIVERY=10
MOVE_TO_DELIVERY=11
PLACE_CUBE2=12



CALC_NODES = {
}


class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass


def register_node_now(op_code, class_reference):
    if op_code in CALC_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" %(
            op_code, CALC_NODES[op_code]
        ))
    CALC_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator

def get_class_from_opcode(op_code):
    if op_code not in CALC_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return CALC_NODES[op_code]



# import all nodes and register them
from bteditor.nodes import *