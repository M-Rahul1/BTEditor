import py_trees as pt
   
def onBuild():
    
    root = pt.composites.Selector("root", children=[])
    seq = pt.composites.Sequence("seq", children=[])
    root.add_child(seq)
    act1 = pt.behaviour.Behaviour("Action1")
    seq.add_child(act1)
    
    def color_from_status(status):
        if status == pt.common.Status.SUCCESS:
            return "green"
    seq_color = color_from_status(seq.status)
    
    
    return pt.trees.BehaviourTree(root)

def onRun(root: pt.behaviour.Behaviour):
    root.tick()