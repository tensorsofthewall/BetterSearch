import sys

from PySide6.QtWidgets import QApplication
from main_window import MainWindow
import tomllib

if __name__ == '__main__':
    with open(r"D:\projects\BetterSearch\src\main\python\default_config.toml","rb") as f:
        config = tomllib.load(f)
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window=MainWindow(**config)
    
    window.show()
    
    sys.exit(app.exec())