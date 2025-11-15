from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox
)
from src.controllers.funcionario_controller import FuncionarioController
from src.models.funcionario import Funcionario

class FuncionarioWindow(QDialog):
    def __init__(self, empresa_id=None):
        super().__init__()
        self.setWindowTitle("Gerenciar Funcionários")
        self.setMinimumSize(700, 400)
        self.empresa_id = empresa_id

        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Adicionar")
        self.btn_edit = QPushButton("Editar")
        self.btn_delete = QPushButton("Excluir")
        self.btn_refresh = QPushButton("Atualizar")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_refresh)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_data()

        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_add.clicked.connect(self.add_funcionario)
        self.btn_edit.clicked.connect(self.edit_funcionario)
        self.btn_delete.clicked.connect(self.delete_funcionario)

    def load_data(self):
        funcionarios = FuncionarioController.listar()
        if self.empresa_id:
            funcionarios = [f for f in funcionarios if f[4] == self.empresa_id]

        self.table.setRowCount(len(funcionarios))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Cargo", "Salário", "Empresa ID"])
        for row_idx, (id, nome, cargo, salario, empresa_id) in enumerate(funcionarios):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(nome))
            self.table.setItem(row_idx, 2, QTableWidgetItem(cargo))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(salario)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(empresa_id)))

    def get_selected_id(self):
        indexes = self.table.selectionModel().selectedRows()
        if indexes:
            row = indexes[0].row()
            return int(self.table.item(row, 0).text())
        return None

    def add_funcionario(self):
        dlg = FuncionarioFormDialog(self.empresa_id)
        if dlg.exec():
            f = Funcionario(
                nome=dlg.nome.text(),
                cargo=dlg.cargo.text(),
                salario=float(dlg.salario.text()),
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
            f = Funcionario(
                id=funcionario_id,
                nome=dlg.nome.text(),
                cargo=dlg.cargo.text(),
                salario=float(dlg.salario.text()),
                empresa_id=self.empresa_id
            )
            FuncionarioController.atualizar(f)
            self.load_data()

    def delete_funcionario(self):
        funcionario_id = self.get_selected_id()
        if funcionario_id is None:
            QMessageBox.warning(self, "Atenção", "Selecione um funcionário!")
            return
        FuncionarioController.deletar(funcionario_id)
        self.load_data()


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
