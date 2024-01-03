from MVPRenamer.Model.NodeModel import NodeModel
from MVPRenamer.View.ConfirmView import ConfirmView
from MVPRenamer.View.MainWindow import MainWindow
from functools import partial


class Presenter:

    def __init__(self,
                 main_window: MainWindow,
                 confirm_view: ConfirmView,
                 node_model: NodeModel):
        self.__view = main_window
        self.__confirm_view = confirm_view
        self.__node_model = node_model

        # viewの操作をシグナルから受取ます。
        self.__view.rename_signal.connect(lambda x: self.on_rename(x))

    def setup(self):
        self.__view.show()

    def on_rename(self, new_name: str):
        message = self.__node_model.rename(new_name)

        # メッセージがあれば、確認ダイアログを表示します。
        if message:
            self.__confirm_view.show_confirm_dialog(message)
        else:
            self.__view.clear_line_edit()
