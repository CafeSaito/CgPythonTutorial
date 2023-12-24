"""
選択中のメッシュ同士の交差部分をpfxToonで可視化するスクリプトです。
"""

import maya.api.OpenMaya as om2
from maya import cmds


def execute(line_width=0.1):
    """
    可視化するメイン関数
    :param line_width:
    :return:
    """

    # 選択中のメッシュを取得
    selections = get_meshes_from_selections()

    # 選択数が2未満の場合はエラー
    if len(selections) < 2:
        raise ValueError('Select 2 or more meshes.')

    # pfxToonCollisionDetectノードを作成
    pfx_node = create_pfx_node(line_width)
    input_surface_node = get_input_surface_node(pfx_node)

    # 各メッシュとpfxToonCollisionDetectShapeを接続
    connect_mesh_to_pfx(selections, input_surface_node)


def get_input_surface_node(pfx_node: str) -> om2.MPlug:
    """
    pfxToonCollisionDetectShapeのinputSurfaceノードを取得する。
    :param pfx_node:
    :return:
    """
    pfx_depend_node = om2.MGlobal.getSelectionListByName(pfx_node).getDependNode(0)
    pfx_dependency_node = om2.MFnDependencyNode(pfx_depend_node)
    input_surface_node = pfx_dependency_node.findPlug('inputSurface', False)
    return input_surface_node


def get_meshes_from_selections() -> list:
    """
    選択中のものから、MFnMeshへ変換できるもののリストを作成する。
    :rtype: list[om2.MFnMesh]
    :return:
    """
    sel = om2.MGlobal.getActiveSelectionList()

    meshes = []
    for i in range(sel.length()):
        try:
            mesh = om2.MFnMesh(sel.getDagPath(i).extendToShape())
            meshes.append(mesh)
        except ValueError:
            continue

    return meshes


def connect_mesh_to_pfx(selections: list, input_surface_node: om2.MPlug) -> None:
    """
    各メッシュとpfxToonCollisionDetectShapeを接続する。
    :type selections: list[om2.MFnMesh]
    :type input_surface_node: om2.MPlug
    :param selections:
    :return:
    """
    dag_modifier = om2.MDGModifier()
    for i, mesh in enumerate(selections):
        out_mesh_plug = mesh.findPlug('outMesh', False)
        world_matrix_plug = mesh.findPlug('worldMatrix', False)

        input_surface_plug = input_surface_node.elementByLogicalIndex(i)
        surface_plug = input_surface_plug.child(0)
        input_world_matrix_plug = input_surface_plug.child(1)

        dag_modifier.connect(out_mesh_plug, surface_plug)
        dag_modifier.connect(world_matrix_plug.elementByLogicalIndex(0), input_world_matrix_plug)

    dag_modifier.doIt()


def create_pfx_node(line_width: float = 0.1) -> str:
    """
    pfxToonCollisionDetectノードを作成する。いくつかのアトリビュートは初期値を設定する。
    :param line_width: 輪郭線の大きさ
    :return: pfxToonノード名
    """
    pfx_toon_node = cmds.createNode('pfxToon')
    cmds.setAttr(f'{pfx_toon_node}.profileLines', 0)
    cmds.setAttr(f'{pfx_toon_node}.creaseLines', 0)
    cmds.setAttr(f'{pfx_toon_node}.intersectionLines', 1)
    cmds.setAttr(f'{pfx_toon_node}.displayPercent', 100)
    cmds.setAttr(f'{pfx_toon_node}.intersectionColor', 1, 0, 0, type='double3')
    cmds.setAttr(f'{pfx_toon_node}.selfIntersect', True)
    cmds.setAttr(f'{pfx_toon_node}.lineWidth', line_width)
    return pfx_toon_node


if __name__ == '__main__':
    execute()
