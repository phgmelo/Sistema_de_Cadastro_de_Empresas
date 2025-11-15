from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QFileDialog
)
from src.controllers.funcionario_controller import FuncionarioController
from src.models.funcionario import Funcionario
import pandas as pd

class FuncionarioWindow(QDialog):
    def __init__(self, empresa_id=None):
        super().__init__()
        self.setWindowTitle("Gerenciar Funcionários")
        self.setMinimumSize(800, 400)
        self.empresa_id = empresa_id

        layout = QVBoxLayout()

        # Campo de busca (ATUALIZA ENQUANTO DIGITA)
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar por nome:"))
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_funcionario)  # <<< AQUI
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Tabela
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Adicionar")
        self.btn_edit = QPushButton("Editar")
        self.btn_delete = QPushButton("Excluir")
        self.btn_refresh = QPushButton("Atualizar")
        self.btn_export = QPushButton("Exportar CSV")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_export)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_data()

        # Conexões
        self.btn_refresh.clicked.connect(self.refresh_data)   # <<< ATUALIZADO
        self.btn_add.clicked.connect(self.add_funcionario)
        self.btn_edit.clicked.connect(self.edit_funcionario)
        self.btn_delete.clicked.connect(self.delete_funcionario)
        self.btn_export.clicked.connect(self.export_csv)

    def load_data(self, search_term=""):
        funcionarios = FuncionarioController.listar()

        # Filtra por empresa
        if self.empresa_id:
            funcionarios = [f for f in funcionarios if f[4] == self.empresa_id]

        # Filtra por nome digitado
        if search_term:
            funcionarios = [f for f in funcionarios if search_term.lower() in f[1].lower()]

        self.table.setRowCount(len(funcionarios))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Cargo", "Salário", "Empresa ID"])

        for row_idx, (id, nome, cargo, salario, empresa_id) in enumerate(funcionarios):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(nome))
            self.table.setItem(row_idx, 2, QTableWidgetItem(cargo))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(salario)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(empresa_id)))

    def refresh_data(self):
        """Limpa busca e atualiza lista — igual EmpresaWindow."""
        self.search_input.clear()
        self.load_data()

    def get_selected_id(self):
        indexes = self.table.selectionModel().selectedRows()
        if indexes:
            row = indexes[0].row()
            return int(self.table.item(row, 0).text())
        return None

    def add_funcionario(self):
        dlg = FuncionarioFormDialog(self.empresa_id)
        if dlg.exec():
            try:
                salario = float(dlg.salario.text())
            except ValueError:
                QMessageBox.warning(self, "Erro", "Salário inválido!")
                return
            if not dlg.nome.text():
                QMessageBox.warning(self, "Erro", "Nome é obrigatório!")
                return

            f = Funcionario(
                nome=dlg.nome.text(),
                cargo=dlg.cargo.text(),
                salario=salario,
                empresa_id=dlg.empresa_id
            )
            FuncionarioController.criar(f)
            self.load_data()

    def edit_funcionario(self):
        funcionario_id = self.get_selected_id()
        if funcionario_id is None:
            QMessageBox.warning(self, "Atenção", "Selecione um funcionário!")
            return

        funcionarios = FuncionarioController.listar()
        f_data = next((f for f in funcionarios if f[0] == funcionario_id), None)

        dlg = FuncionarioFormDialog(self.empresa_id)
        dlg.nome.setText(f_data[1])
        dlg.cargo.setText(f_data[2])
        dlg.salario.setText(str(f_data[3]))

        if dlg.exec():
            try:
                salario = float(dlg.salario.text())
            except ValueError:
                QMessageBox.warning(self, "Erro", "Salário inválido!")
                return

            f = Funcionario(
                id=funcionario_id,
                nome=dlg.nome.text(),
                cargo=dlg.cargo.text(),
                salario=salario,
                empresa_id=self.empresa_id
            )
            FuncionarioController.atualizar(f)
            self.load_data()

    def delete_funcionario(self):
        funcionario_id = self.get_selected_id()
        if funcionario_id is None:
            QMessageBox.warning(self, "Atenção", "Selecione um funcionário!")
            return

        if QMessageBox.question(self, "Confirmar", "Deseja realmente excluir este funcionário?") == QMessageBox.Yes:
            FuncionarioController.deletar(funcionario_id)
            self.load_data()

    def search_funcionario(self):
        self.load_data(self.search_input.text())

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Salvar CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        funcionarios = FuncionarioController.listar()

        if self.empresa_id:
            funcionarios = [f for f in funcionarios if f[4] == self.empresa_id]

        df = pd.DataFrame(funcionarios, columns=["ID", "Nome", "Cargo", "Salário", "Empresa ID"])
        df.to_csv(path, index=False)

        QMessageBox.information(self, "Exportar CSV", f"Arquivo exportado para {path} com sucesso!")


class FuncionarioFormDialog(QDialog):
    def __init__(self, empresa_id=None):
        super().__init__()
        self.setWindowTitle("Formulário de Funcionário")
        self.empresa_id = empresa_id

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nome:"))
        self.nome = QLineEdit()
        layout.addWidget(self.nome)

        layout.addWidget(QLabel("Cargo:"))
        self.cargo = QLineEdit()
        layout.addWidget(self.cargo)

        layout.addWidget(QLabel("Salário:"))
        self.salario = QLineEdit()
        layout.addWidget(self.salario)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Salvar")
        self.btn_cancel = QPushButton("Cancelar")
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
