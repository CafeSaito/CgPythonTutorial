import unittest
from unittest import TestCase
from maya import cmds, standalone
from pathlib import Path

try:
    tests_dir = Path(__file__).parent.parent.parent
    root_dir = tests_dir.parent
    script_dir = root_dir / "scripts"
except NameError:
    # ローカルで実行する場合のインポート処理。パスは適宜書き換えてください。
    import sys

    sys.path.append(r'D:/cafegroup/CgPythonTutorial/MVP/scripts')
    try:
        import importlib

        importlib.reload(sys.modules['MVPRenamer.Model.NodeModel'])
    except KeyError:
        pass
finally:
    from MVPRenamer.Model.NodeModel import NodeModel


class TestNodeModel(TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cmds.ls()
        except AttributeError:
            standalone.initialize()

    def setUp(self):
        """
        テスト用のシーンを作成する。
        """
        cmds.file(new=True, force=True)
        self.cube, _ = cmds.polyCube(name="test_cube")
        self.joint = cmds.joint(name="test_joint")
        self.camera, _ = cmds.camera(name="test_camera")
        self.locator = cmds.spaceLocator(name="test_locator")[0]
        self.circle, _ = cmds.circle(name="test_circle")
        self.group = cmds.group(name="test_grp", empty=True)

        # グループの下にプレーンを配置して誤作動しないか？
        plane, _ = cmds.polyPlane()
        cmds.parent(plane, self.group)

    def test_rename(self):
        node_model = NodeModel()

        cmds.select(self.cube)
        node_model.rename("test_cube_new")
        self.assertEqual(cmds.ls(sl=True)[0], f"test_cube_new_{NodeModel.suffix_patterns['mesh']}")

        cmds.select(self.joint)
        node_model.rename("test_joint_new")
        self.assertEqual(cmds.ls(sl=True)[0], f"test_joint_new_{NodeModel.suffix_patterns['joint']}")

        cmds.select(self.camera)
        node_model.rename("test_camera_new")
        self.assertEqual(cmds.ls(sl=True)[0], f"test_camera_new_{NodeModel.suffix_patterns['camera']}")

        cmds.select(self.locator)
        node_model.rename("test_locator_new")
        self.assertEqual(cmds.ls(sl=True)[0], f"test_locator_new_{NodeModel.suffix_patterns['locator']}")

        cmds.select(self.circle)
        node_model.rename("test_circle_new")
        self.assertEqual(cmds.ls(sl=True)[0], "test_circle_new")

        cmds.select(self.group)
        node_model.rename("test_grp_new")
        self.assertEqual(cmds.ls(sl=True)[0], "test_grp_new")

    def test_rename_error(self):
        node_model = NodeModel()

        cmds.select(clear=True)
        message = node_model.rename("test_grp_new")
        self.assertEqual(message, "Please Select node")

        cmds.select(self.group)
        message = node_model.rename("")
        self.assertEqual(message, "Node name cannot be empty")

        cmds.select(self.group)
        message = node_model.rename("test_grp")
        self.assertEqual(message, "Node name is not changed")

        cmds.select(self.group)
        message = node_model.rename("|||||")
        self.assertEqual(message, "Node name must be alphanumeric and underscore")

        cmds.select(self.group)
        message = node_model.rename("test_cube")
        self.assertEqual(message, "Node name already exists")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNodeModel)
    unittest.TextTestRunner(verbosity=2).run(suite)
