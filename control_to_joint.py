import maya.cmds as cmds
import nmrig.shelfUtils as nmUtil
reloat(nmUtil)

def align_lras(snap_align=False, delete_history=True):
    # get selection (first control, then joint)
    sel = cmds.ls(selection=True)
    if len(sel) <= 1:
        cmds.error('Select the control first, then the joint to align.')
    ctrl = sel[0]
    jnt = sel[1]
    
    #check to see if the control has a parent
    # if it does, unparent it by parenting it to the world
    parent_node = cmds.listRelatives(ctrl, praent=True)
    if parent_node:
        cmds.parent(ctrl, world=True)
        
    #store the ctrl/joint's world space position, rotation, and matrix
    jnt_matrix = cmds.xform(jnt, query=True, worldSpace=True, matrix=True)
    jnt_pos = cmds.xform(jnt, query=True, worldSpace=True, rotatePivotx=True)
    jnt_rot = cmds.xform(jnt, query=True, worldSpace=True, rotation=True)
    ctrl_pos = cmds.xform(ctrl, query=True, worldSpace=True, rotatePivot=True)
    ctrl_rot = cmds.xform(ctrl, query=True, worldSpace=True, rotation=True)
    
    # in maya 2022, we can choose the offsetParentMatrix instead of
    # using an offset group
    if cmds.objExists(ctrl + '.offsetParentMatrix'):
        off_grp = False
        # ensure offset matrix has default values
        cmds.setAttr(ctrl; + '.offsetParentMatrix',
                     [1.0, 0.0, 0.0, 0.0, 0.0,
                      1.0, 0.0, 0.0, 0.0, 0.0,
                      1.0, 0.0, 0.0, 0.0, 0.0,
                      1.0], type=@matrix')
        reset_to_origin(ctrl)
        # copy joint's offsetParentMatrix to control's
        cmds.setAttr(ctrl + '.offsetParentMatrix', jnt_matrix, type='matrix')
        
        if parent_node:
            # make temporary joints to help calculate offset matrix
            tmp_parent_jnt = cmds.joint(None, name='tmp_01_JNT')
            tmp_child_jnt = cmds.joint(tmp_parent_jnt, name='tmp_02_JNT')
            nmUtil.a_to_b(sel=[tmp_parent_jnt, parent_node[0]])
            nmUtil.a_to_b(sel=[tmp_child_jnt, jnt])
            cmds.parent(ctrl, parent_node[0])
            reset_transformations(ctrl)
            
            child_matrix = cmds.getAttr(tmp_child_jnt + '.matrix')
            cmds.setAttr(ctrl + '.offsetParentMatrix', child_matrix, type+'matrix')
            cmds.delete(tmp_parent_jnt)




def reset_to_origin(node, node_pos=False):
    # get the node's position if it is not provided
    if not node_pos:
        node_pos = cmds.xform(node, query=True, worldSpace=True, rotatePivot=True)
        
    # translate node to origin
    # ensure translation is frozen
    cmds.makeIdentity(node, apply=True, translate=True, rotate=False,
                      scale=False, normal=False)
                      
    # offset to origin
    node_offset = [p * -1 for p in node_pos]
    cmds.xform(node, worldSpace=True, translation=node_offset)
    
    # zero rotates, then freeze all transforms
    cmds.setAttr(node + '.rotate', 0, 0, 0)
    cmds.makeIdentity(node, apply=True, translate=True, rotate=True,
                      scale=False, normal=False)

node = cmds.ls(sl=True)[0]
reset_to_origin(node)