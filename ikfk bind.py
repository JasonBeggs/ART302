fk_chain = cmds.ls('*_FK_JNT')
ik_chain = cmds.ls('*_IK_JNT')
bind_chain = cmds.ls('*_bind_JNT')

for fk, ik, bind in zip(fk_chain,ik_chain, bind_chain):
    for attr in ['translate', 'rotate', 'scale']:
        bcn = cmds.createNode('blendColours', 
                              name=bind.replace('bind_JNT', attr + '_BCN'))
        
        cmds.connectAttr(ik + '.' + attr, bcn, + '.colour1')
        cmds.connectAttr(fk + '.' + attr, bcn, + '.colour2')
        cmds.connectAttr('L_arm_settings_CTRL.fkik', bcn + '.blender')
        cmds.connectAttr(bcn + '.output', bind + '.' + attr)