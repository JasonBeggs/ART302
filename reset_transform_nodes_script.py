def reset_transforms(nodes):
    if not nodes:
        nodes = cmds.ls(selection=True)
        
    # if nodes isn't a list, make it one
    if not isinstance(nodes, list):
        nodes = [ndoes]
        
    for node in nodes:
        cmds.setAttr(node + '.translate', 0, 0, 0)
        cmds.setAttr(node + '.rotate', 0, 0, 0)
        cmds.setAttr(node + '.scale', 1, 1, 1)



reset_transforms(nodes=False)