LISTBOX_MIMETYPE = "application/x-item"

FALLBACK = 1
SEQUENCE = 2
PARALLEL = 3
IS_COFFEE_READY=4
HAS_COFFEE=5
HAS_MILK=6
HAS_SUGAR=7
ADD_COFFEE=8
ADD_MILK=9
ADD_SUGAR=10


NO_EMERGENCY = 11
STOP_VECHILE = 12
ALERT_AUTHORITIES = 13
NO_TRAFFIC_LIGHT = 14
LIGHT_IS_RED = 15
LIGHT_IS_GREEN = 16
LIGHT_IS_YELLOW = 17
STOP = 18
PROCEED = 19
CAUTION = 20
WITHIN_LANE = 21
MOVE_INTO_LANE = 22
KEEP_DRIVING = 23

CRITICAL_SYSTEM_POWER = 24
POWER_CRITICAL_SYSTEM = 25
NOTIFY_ADMIN = 26
NO_EXCESS_RENEWABLE_ENERGY = 27
STORE_EXCESS_ENERGY = 28
NON_CRITICAL_SYSTEM_POWER = 29
POWER_NON_CRITICAL_SYSTEM = 30
NO_STORED_ENERGY_AVAILABLE = 31
USE_STORED_ENERGY = 32

MOVE_TO_PATIENT = 33
ASSIST_PATIENT = 34
MEDICINE_WITH_PATIENT = 35
ROBOT_AT_MEDICINE = 36 
MOVE_TO_MEDICINE = 37
PICK_UP_MEDICINE = 38
ROBOT_AT_PATIENT = 39
DELIVER_MEDICINE = 41

PARTS_IN_ASSEMBLY = 42
PICK_PARTS = 43
PLACE_PARTS_IN_ASSEMBLY = 44
PRODUCT_ASSSEMBLED = 45
ASSEMBLE_PRODUCT = 46
PRODUCTS_STORED = 47
STORE_PRODUCT = 48
PARTS_PICKED = 49

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