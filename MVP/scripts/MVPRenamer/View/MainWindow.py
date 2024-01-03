from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtCore import Signal
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

# このファイルのパスを__file__から取得し、pathlib.Pathインスタンスを作成する。
CURRENT_FILE = Path(__file__)
# QtDesignerのUIファイルのパスをこのファイルからの相対パスで取得する。pathlib.PATHインスタンスは / でパスの結合ができます。
UI_FILE = CURRENT_FILE.parent.parent / "resources" / 'UI.ui'


class MainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    rename_signal = Signal(str)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # UIファイルをロードし、ウィジェットとして使えるようにする。
        self.__widget = QUiLoader().load(UI_FILE.as_posix())
        # MayaUIのセントラルウィジェットに設定する。
        self.setCentralWidget(self.__widget)
        self.resize(400, 100)

        # UI要素をQtDesignerから取得し、変数へ入れておく
        self.__btn_rename = self.__widget.btn_rename
        self.__lineEdit_name = self.__widget.lineEdit_name

        # リネームボタンをクリックしたときに実行するメソッドとの紐づけ
        self.__btn_rename.clicked.connect(self.on_click_rename)

    @property
    def new_name(self):
        """
        リネームする名前をQLineEditから取得する。
        @propertyというのは、このメソッドを属性として扱えるようにするものです。これにより呼び出し時の()を省略できます。
        """
        return self.__lineEdit_name.text()

    def set_new_name(self, name: str):
        """
        QLineEditにname(str)をセットするメソッドです。
        """
        self.__lineEdit_name.setText(name)

    def on_click_rename(self):
        """
        リネームボタンをクリックしたときに実行されるメソッドです。
        シグナルを実行してPresenterに通知します。
        """
        self.rename_signal.emit(self.new_name)

    def clear_line_edit(self):
        """
        QLineEditを空にするメソッドです。
        """
        self.__lineEdit_name.setText("")
