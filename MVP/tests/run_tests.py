# run_tests.py
import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    # パスは適宜変更してください。
    start_dir = r'D:\cafegroup\CgPythonTutorial\MVP\tests\TestRenamer'
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
