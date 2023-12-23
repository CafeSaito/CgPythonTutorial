import unittest
from maya import standalone, cmds
import SampleRenamerForMayaUnitTest as sample_renamer


class SampleRenamerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        テストケースクラスのすべてのテストメソッドの実行前に一度だけ呼ばれます。
        """

        # mayaの初期化
        standalone.initialize()

    def test_rename(self):
        cube = cmds.polyCube(n="testPolyCube")
        result = sample_renamer.rename(cube[0])
        self.assertEqual(result, "testPolyCube_mesh")  # リネーム後の名前が想定通りか確認

        curve = cmds.circle(n="testCurve")
        result = sample_renamer.rename(curve[0])
        self.assertEqual(result, "testCurve_curveShape")

        joint = cmds.joint(n="testJoint")
        result = sample_renamer.rename(joint)
        self.assertEqual(result, "testJoint_joint")

        # カメラはリネームの対象外なので、例外が発生します。
        with self.assertRaises(Exception):
            camera = cmds.camera(n="testCamera")
            _ = sample_renamer.rename(camera[0])
