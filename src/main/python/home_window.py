from PySide6.QtWidgets import QWidget

from ui.widgets.home_widget import Ui_home_widget

class HomeWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.home_ui = Ui_home_widget()
        self.home_ui.setupUi(self)