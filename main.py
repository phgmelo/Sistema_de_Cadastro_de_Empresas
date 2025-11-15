import sys
import os

# Adiciona a pasta raiz ao path
sys.path.append(os.path.dirname(__file__))

from src.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
