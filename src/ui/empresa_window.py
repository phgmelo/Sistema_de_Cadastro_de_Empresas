from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox
)
from src.controllers.empresa_controller import EmpresaController
from src.models.empresa import Empresa
from src.ui.funcionario_window import FuncionarioWindow
import re

class EmpresaWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar Empresas")
        self.setMinimumSize(700, 450)

        layout = QVBoxLayout()

        # Campo de busca
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nome da empresa...")
        self.search_input.textChanged.connect(self.search_empresa)
        layout.addWidget(self.search_input)

        # Tabela
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Adicionar")
        self.btn_edit = QPushButton("Editar")
        self.btn_delete = QPushButton("Excluir")
        self.btn_view_func = QPushButton("Ver Funcionários")
        self.btn_refresh = QPushButton("Atualizar")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_view_func)
        btn_layout.addWidget(self.btn_refresh)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_data()

        # Conexões dos botões
        self.btn_refresh.clicked.connect(self.refresh_data)
        self.btn_add.clicked.connect(self.add_empresa)
        self.btn_edit.clicked.connect(self.edit_empresa)
        self.btn_delete.clicked.connect(self.delete_empresa)
        self.btn_view_func.clicked.connect(self.view_funcionarios)

    def load_data(self, filtro_nome=""):
        empresas = EmpresaController.listar()
        if filtro_nome:
            empresas = [e for e in empresas if filtro_nome.lower() in e[1].lower()]
        self.table.setRowCount(len(empresas))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CNPJ", "Endereço"])
        for row_idx, (id, nome, cnpj, endereco) in enumerate(empresas):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(nome))
            self.table.setItem(row_idx, 2, QTableWidgetItem(cnpj))
            self.table.setItem(row_idx, 3, QTableWidgetItem(endereco))

    def search_empresa(self):
        self.load_data(self.search_input.text())

    def refresh_data(self):
        """Limpa o campo de busca e recarrega toda a tabela"""
        self.search_input.clear()
        self.load_data()

    def get_selected_id(self):
        indexes = self.table.selectionModel().selectedRows()
        if indexes:
            row = indexes[0].row()
            return int(self.table.item(row, 0).text())
        return None

    def validate_cnpj(self, cnpj):
        cnpj = re.sub(r'\D', '', cnpj)
        return len(cnpj) == 14

    def add_empresa(self):
        dlg = EmpresaFormDialog()
        if dlg.exec():
            if not dlg.nome.text() or not dlg.cnpj.text():
                QMessageBox.warning(self, "Erro", "Nome e CNPJ são obrigatórios!")
                return
            if not self.validate_cnpj(dlg.cnpj.text()):
                QMessageBox.warning(self, "Erro", "CNPJ inválido! Deve ter 14 dígitos.")
                return
            empresa = Empresa(nome=dlg.nome.text(), cnpj=dlg.cnpj.text(), endereco=dlg.endereco.text())
            EmpresaController.criar(empresa)
            self.load_data(self.search_input.text())

    def edit_empresa(self):
        empresa_id = self.get_selected_id()
        if empresa_id is None:
            QMessageBox.warning(self, "Atenção", "Selecione uma empresa para editar!")
            return

        empresas = EmpresaController.listar()
        empresa_data = next((e for e in empresas if e[0] == empresa_id), None)
        dlg = EmpresaFormDialog(*empresa_data[1:])
        if dlg.exec():
            if not dlg.nome.text() or not dlg.cnpj.text():
                QMessageBox.warning(self, "Erro", "Nome e CNPJ são obrigatórios!")
                return
            if not self.validate_cnpj(dlg.cnpj.text()):
                QMessageBox.warning(self, "Erro", "CNPJ inválido! Deve ter 14 dígitos.")
                return
            empresa = Empresa(id=empresa_id, nome=dlg.nome.text(), cnpj=dlg.cnpj.text(), endereco=dlg.endereco.text())
            EmpresaController.atualizar(empresa)
            self.load_data(self.search_input.text())

    def delete_empresa(self):
        empresa_id = self.get_selected_id()
        if empresa_id is None:
            QMessageBox.warning(self, "Atenção", "Selecione uma empresa para excluir!")
            return
        if QMessageBox.question(self, "Confirmar", "Deseja realmente excluir esta empresa?") == QMessageBox.Yes:
            EmpresaController.deletar(empresa_id)
            self.load_data(self.search_input.text())

    def view_funcionarios(self):
        empresa_id = self.get_selected_id()
        if empresa_id is None:
            QMessageBox.warning(self, "Atenção", "Selecione uma empresa!")
            return
        dlg = FuncionarioWindow(empresa_id=empresa_id)
        dlg.exec()


class EmpresaFormDialog(QDialog):
    def __init__(self, nome="", cnpj="", endereco=""):
        super().__init__()
        self.setWindowTitle("Formulário de Empresa")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nome:"))
        self.nome = QLineEdit(nome)
        layout.addWidget(self.nome)

        layout.addWidget(QLabel("CNPJ:"))
        self.cnpj = QLineEdit(cnpj)
        layout.addWidget(self.cnpj)

        layout.addWidget(QLabel("Endereço:"))
        self.endereco = QLineEdit(endereco)
        layout.addWidget(self.endereco)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Salvar")
        self.btn_cancel = QPushButton("Cancelar")
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
