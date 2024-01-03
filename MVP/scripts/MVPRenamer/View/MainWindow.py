from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtCore import Signal
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

CURRENT_FILE = Path(__file__)
UI_FILE = CURRENT_FILE.parent.parent / "resources" / 'UI.ui'


class MainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    rename_signal = Signal(str)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.__widget = QUiLoader().load(UI_FILE.as_posix())
        self.setCentralWidget(self.__widget)
        self.resize(400, 100)

        # UI要素をQtDesignerから取得し、変数へ入れておく
        self.__btn_rename = self.__widget.btn_rename
        self.__lineEdit_name = self.__widget.lineEdit_name

        self.__btn_rename.clicked.connect(self.on_click_rename)

    @property
    def new_name(self):
        return self.__lineEdit_name.text()

    def set_new_name(self, name: str):
        self.__lineEdit_name.setText(name)

    def on_click_rename(self):
        self.rename_signal.emit(self.new_name)

    def clear_line_edit(self):
        self.__lineEdit_name.setText("")
