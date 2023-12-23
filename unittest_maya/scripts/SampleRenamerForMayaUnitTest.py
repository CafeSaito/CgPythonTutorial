"""
Mayaでunittestを実行するためのサンプルスクリプト。
"""

from maya import cmds


def rename(node):
    object_type = cmds.objectType(node)

    if object_type == "transform":
        shapes = cmds.listRelatives(node, shapes=True)
        if shapes:
            object_type = cmds.objectType(shapes[0])

    if object_type == "mesh":
        rename_name = f'{node}_mesh'
    elif object_type == "nurbsCurve":
        rename_name = f'{node}_curveShape'
    elif object_type == "joint":
        rename_name = f'{node}_joint'
    elif object_type == "transform":
        rename_name = f'{node}_transform'
    else:
        raise Exception(f"Unknown object type: {object_type}")

    new_name = cmds.rename(node, rename_name)
    return new_name
