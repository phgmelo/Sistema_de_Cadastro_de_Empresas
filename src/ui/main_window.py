from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Empresas e Funcionários 1")
        self.setMinimumSize(500, 300)

        layout = QVBoxLayout()

        title = QLabel("Sistema de Gerenciamento")
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        btn_empresas = QPushButton("Gerenciar Empresas")
        btn_funcionarios = QPushButton("Gerenciar Funcionários")
        layout.addWidget(btn_empresas)
        layout.addWidget(btn_funcionarios)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
