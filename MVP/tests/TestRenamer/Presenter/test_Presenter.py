import unittest
from pathlib import Path
from unittest.mock import MagicMock

from maya import cmds, standalone

import sys

try:
    tests_dir = Path(__file__).parent.parent.parent
    root_dir = tests_dir.parent
    script_dir = root_dir / "scripts"
    sys.path.append(script_dir.as_posix())
except NameError:
    # ローカルで実行する場合のインポート処理。パスは適宜書き換えてください。
    sys.path.append(r'D:/cafegroup/CgPythonTutorial/MVP/scripts')

    try:
        import importlib

        importlib.reload(sys.modules['MVPRenamer.Model.NodeModel'])
        importlib.reload(sys.modules['MVPRenamer.View.ConfirmView'])
        importlib.reload(sys.modules['MVPRenamer.View.MainWindow'])
        importlib.reload(sys.modules['MVPRenamer.Presenter.Presenter'])
    except KeyError:
        pass
finally:
    from MVPRenamer.Model.NodeModel import NodeModel
    from MVPRenamer.View.MainWindow import MainWindow
    from MVPRenamer.Presenter.Presenter import Presenter
    from MVPRenamer.View.ConfirmView import ConfirmView


class TestPresenter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cmds.ls()
        except AttributeError:
            standalone.initialize()

    def setUp(self):
        cmds.file(new=True, force=True)

        self.cube = cmds.polyCube(name="test_cube")
        self.model = NodeModel()
        self.main_window = MainWindow()

        self.confirm_view = ConfirmView()
        self.confirm_view.show_confirm_dialog = MagicMock(return_value=0)

        self.presenter = Presenter(self.main_window, self.confirm_view, self.model)

    def test_rename_success(self):
        self.presenter.setup()

        cmds.select(self.cube)
        self.presenter.on_rename("test")
        self.assertEqual(cmds.ls(sl=True)[0], "test_geo")
        self.assertEqual(self.main_window.new_name, '')

    def test_rename_fail(self):
        self.presenter.setup()

        cmds.select(self.cube)

        self.presenter.on_rename("")
        self.assertEqual(cmds.ls(sl=True)[0], "test_cube")
        self.assertEqual(self.main_window.new_name, '')

    def tearDown(self):
        self.main_window.close()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPresenter)
    unittest.TextTestRunner(verbosity=2).run(suite)
