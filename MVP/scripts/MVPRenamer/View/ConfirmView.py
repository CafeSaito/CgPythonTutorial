from PySide2.QtWidgets import QMessageBox
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


class ConfirmView(MayaQWidgetBaseMixin, QMessageBox):
    def __init__(self, *args, **kwargs):
        super(ConfirmView, self).__init__(*args, **kwargs)
        self.resize(400, 300)

    def show_confirm_dialog(self, message):
        self.information(self, 'Please confirm', message)
