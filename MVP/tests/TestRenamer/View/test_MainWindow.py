import unittest
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
    import importlib

    try:
        importlib.reload(sys.modules['MVPRenamer.View.MainWindow'])
    except KeyError:
        pass
finally:
    from MVPRenamer.View import MainWindow


class TestMainWindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cmds.ls()
        except AttributeError:
            standalone.initialize()

    def setUp(self):
        self.main_window = MainWindow.MainWindow()

    def test_show(self):
        self.assertTrue(MainWindow.UI_FILE.exists())

        self.main_window.show()
        self.assertTrue(self.main_window.isVisible())

    def test_on_click_rename(self):
        self.main_window.show()
        self.main_window.set_new_name("viewtest")

        self.main_window.rename_signal.connect(lambda x: self.assertEqual(x, "viewtest"))
        self.main_window.on_click_rename()

    def test_clear_line_edit(self):
        self.main_window.show()
        self.main_window.set_new_name("viewtest")

        self.main_window.clear_line_edit()
        self.assertEqual(self.main_window.new_name, "")

    def tearDown(self):
        self.main_window.close()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMainWindow)
    unittest.TextTestRunner(verbosity=2).run(suite)
