import py_trees as pt
   
def onBuild():
    
    selector = pt.composites.Selector("selector", children=[])
    seq = pt.composites.Sequence("seq", children=[])
    selector.add_child(seq)
    act1 = pt.behaviour.Behaviour("Action1")
    seq.add_child(act1)
    
    def color_from_status(status):
        if status == pt.common.Status.SUCCESS:
            return "green"
    seq_color = color_from_status(seq.status)
    
    
    return pt.trees.BehaviourTree(selector)

def onRun(selector: pt.behaviour.Behaviour):
    selector.tick()