import unittest
import VisualizeIntersectionWithPfx
from maya import standalone, cmds


class TestVisualizeIntersectionWithPfx(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        standalone.initialize()

    def setUp(self):
        # テストごとにシーンをクリア
        cmds.file(new=True, force=True)

    def test_get_meshes_from_selections(self):
        # テストデータの準備----------------------------
        cube = cmds.polyCube()[0]
        sphere = cmds.polySphere()[0]
        camera = cmds.camera()[0]
        cube_shape = cmds.listRelatives(cube, s=True)[0]
        sphere_shape = cmds.listRelatives(sphere, s=True)[0]
        camera_shape = cmds.listRelatives(camera, s=True)[0]

        selections = [cube, sphere, camera]
        cmds.select(selections)

        # テスト実行----------------------------------

        meshes = VisualizeIntersectionWithPfx.get_meshes_from_selections()
        meshes = [i.name() for i in meshes]

        self.assertIn(cube_shape, meshes)
        self.assertIn(sphere_shape, meshes)
        self.assertNotIn(camera_shape, meshes)

    def test_get_input_surface_node(self):
        node = cmds.createNode('pfxToon')
        input_node = VisualizeIntersectionWithPfx.get_input_surface_node(node)
        self.assertEqual(input_node.name(), f'{node}.inputSurface')

        mesh_node = cmds.createNode('mesh')
        self.assertRaises(RuntimeError, VisualizeIntersectionWithPfx.get_input_surface_node, mesh_node)

    def test_create_pfx_node(self):
        node = VisualizeIntersectionWithPfx.create_pfx_node(1)

        # pfxノードが作成できているか？
        self.assertTrue(cmds.objExists(node))
        # ノードのデフォルト値が意図通り設定されているか？
        self.assertEqual(cmds.getAttr(f'{node}.profileLines'), 0)
        self.assertEqual(cmds.getAttr(f'{node}.creaseLines'), 0)
        self.assertEqual(cmds.getAttr(f'{node}.intersectionLines'), 1)
        self.assertEqual(cmds.getAttr(f'{node}.displayPercent'), 100)
        self.assertEqual(cmds.getAttr(f'{node}.intersectionColor'), [(1.0, 0.0, 0.0)])
        self.assertEqual(cmds.getAttr(f'{node}.selfIntersect'), True)
        self.assertEqual(cmds.getAttr(f'{node}.lineWidth'), 1)

    def test_connect_mesh_to_pfx(self):
        """
        メッシュとpfxノードの接続ができているかの確認
        :return:
        """

        # テストデータの準備----------------------------
        node = VisualizeIntersectionWithPfx.create_pfx_node()
        input_surface_node = VisualizeIntersectionWithPfx.get_input_surface_node(node)

        cube = cmds.polyCube()[0]
        cmds.select(cube)
        meshes = VisualizeIntersectionWithPfx.get_meshes_from_selections()
        cube_shape = cmds.listRelatives(cube, s=True)[0]

        # テスト実行----------------------------------

        VisualizeIntersectionWithPfx.connect_mesh_to_pfx(meshes, input_surface_node)
        self.assertEqual(cmds.listConnections(f'{node}.inputSurface', s=True, d=False, p=True)[0], f'{cube_shape}.outMesh')

    def test_execute_func(self):
        cmds.select(clear=True)

        # 何も選択してない状態でエラーするかを確認
        self.assertRaises(ValueError, VisualizeIntersectionWithPfx.execute)

        # ２つ選択しているがメッシュが２より少ない場合にエラーするか
        cube = cmds.polyCube()[0]
        camera = cmds.camera()[0]
        cmds.select(camera, cube)
        self.assertRaises(ValueError, VisualizeIntersectionWithPfx.execute)

        # 2つのメッシュを選んだ状態で実行するとpfxノードが作成されるか
        sphere = cmds.polySphere()[0]
        cmds.select(cube, sphere)
        VisualizeIntersectionWithPfx.execute()
        self.assertTrue(cmds.ls(type='pfxToon'))

    @classmethod
    def tearDownClass(cls):
        standalone.uninitialize()
