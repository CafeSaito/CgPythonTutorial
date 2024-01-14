from maya import cmds

values = {
    't': (1, 2, 3),
    'ro': (0, 0, 0),
    'objectSpace': True,
}

cmds.xform('pCube1', **values)
