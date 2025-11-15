from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from src.ui.empresa_window import EmpresaWindow
from src.ui.funcionario_window import FuncionarioWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Empresas e Funcionários")
        self.setMinimumSize(500, 300)

        layout = QVBoxLayout()

        # Título
        title = QLabel("Sistema de Gerenciamento")
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # Botões como atributos da classe
        self.btn_empresas = QPushButton("Gerenciar Empresas")
        self.btn_funcionarios = QPushButton("Gerenciar Funcionários")
        layout.addWidget(self.btn_empresas)
        layout.addWidget(self.btn_funcionarios)

        # Conecta os botões aos métodos
        self.btn_empresas.clicked.connect(self.open_empresas)
        self.btn_funcionarios.clicked.connect(self.open_funcionarios)

        # Configura container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Abre a janela de empresas
    def open_empresas(self):
        dlg = EmpresaWindow()
        dlg.exec()

    # Abre a janela de funcionários
    def open_funcionarios(self):
        dlg = FuncionarioWindow()
        dlg.exec()
