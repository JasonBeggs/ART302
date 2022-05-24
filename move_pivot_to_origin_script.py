# transfer pivots to either first selected object or the origin
def transfer_pivots(origin=False):
    # get selection
    sel = cmds.ls(selection=True)
    
    # move pivot to origin
    if origin:
        for s in sel:
            cmds.xform(s, worldSpace=True, pivots=(0, 0, 0)
            
    # move pivots to first selected object
    else:
        # get the rotate pivot
        first_piv = cmds.xform(sel[0], query=True, worldSpace=True,
                               rotatePivot=True)
        for s in sel[1:]:
            cmds.xform(s, worldSpace=True, pivots=first_piv)

