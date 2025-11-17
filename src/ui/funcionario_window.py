from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QFileDialog, QComboBox # Adicione QComboBox
)
from src.controllers.funcionario_controller import FuncionarioController
from src.controllers.empresa_controller import EmpresaController # Importe o controlador de empresa
from src.models.funcionario import Funcionario
import pandas as pd

class FuncionarioWindow(QDialog):
    def __init__(self, empresa_id=None):
        super().__init__()
        self.setWindowTitle("Gerenciar Funcionários")
        self.setMinimumSize(800, 400)
        self.empresa_id = empresa_id # Mantém para filtrar a janela se aberta por empresa

        layout = QVBoxLayout()

        # Campo de busca (ATUALIZA ENQUANTO DIGITA)
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar por nome:"))
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_funcionario)
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
        self.btn_refresh.clicked.connect(self.refresh_data)
        self.btn_add.clicked.connect(self.add_funcionario)
        self.btn_edit.clicked.connect(self.edit_funcionario)
        self.btn_delete.clicked.connect(self.delete_funcionario)
        self.btn_export.clicked.connect(self.export_csv)

    def load_data(self, search_term=""):
        # Agora FuncionarioController.listar() retorna (id, nome, cargo, salario, empresa_id, empresa_nome)
        funcionarios = FuncionarioController.listar()

        # Filtra por empresa se a janela foi aberta com um empresa_id específico
        if self.empresa_id:
            funcionarios = [f for f in funcionarios if f[4] == self.empresa_id] # f[4] ainda é o empresa_id

        # Filtra por nome digitado
        if search_term:
            funcionarios = [f for f in funcionarios if search_term.lower() in f[1].lower()] # f[1] é o nome do funcionário

        self.table.setRowCount(len(funcionarios))
        self.table.setColumnCount(6) # 6 colunas agora: ID, Nome, Cargo, Salário, Empresa ID, Empresa Nome
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Cargo", "Salário", "ID Empresa", "Empresa"]) # Cabeçalhos atualizados

        for row_idx, (id, nome, cargo, salario, empresa_id, empresa_nome) in enumerate(funcionarios): # Desestruturação atualizada
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(nome))
            self.table.setItem(row_idx, 2, QTableWidgetItem(cargo))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(salario)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(empresa_id))) # Mantemos o ID da empresa para referência
            self.table.setItem(row_idx, 5, QTableWidgetItem(empresa_nome)) # Nova coluna: Nome da Empresa

        self.table.resizeColumnsToContents() # Ajusta o tamanho das colunas para o conteúdo

    def refresh_data(self):
        self.search_input.clear()
        self.load_data()

    def get_selected_id(self):
        indexes = self.table.selectionModel().selectedRows()
        if indexes:
            row = indexes[0].row()
            return int(self.table.item(row, 0).text())
        return None

    def add_funcionario(self):
        # Passa o empresa_id da janela para pré-selecionar no formulário, se houver
        dlg = FuncionarioFormDialog(default_empresa_id=self.empresa_id)
        if dlg.exec():
            # A validação de empresa_id agora está no accept_form do dialog
            try:
                salario = float(dlg.salario.text())
            except ValueError:
                QMessageBox.warning(self, "Erro", "Salário inválido! Digite um número válido.")
                return
            if not dlg.nome.text():
                QMessageBox.warning(self, "Erro", "Nome é obrigatório!")
                return

            f = Funcionario(
                nome=dlg.nome.text(),
                cargo=dlg.cargo.text(),
                salario=salario,
                empresa_id=dlg.selected_empresa_id # Pega o ID da empresa selecionada no dialog
            )
            FuncionarioController.criar(f)
            self.load_data()

    def edit_funcionario(self):
        funcionario_id = self.get_selected_id()
        if funcionario_id is None:
            QMessageBox.warning(self, "Atenção", "Selecione um funcionário!")
            return

        # Para editar, precisamos de todos os dados do funcionário, incluindo o empresa_id atual.
        # FuncionarioController.listar() já retorna (id, nome, cargo, salario, empresa_id, empresa_nome)
        all_funcionarios = FuncionarioController.listar()
        f_data_tuple = next((f for f in all_funcionarios if f[0] == funcionario_id), None)

        if f_data_tuple is None:
            QMessageBox.warning(self, "Erro", "Dados do funcionário não encontrados!")
            return

        # Converte a tupla para dicionário para passar para o diálogo de forma mais legível
        f_data_dict = {
            'id': f_data_tuple[0],
            'nome': f_data_tuple[1],
            'cargo': f_data_tuple[2],
            'salario': f_data_tuple[3],
            'empresa_id': f_data_tuple[4],
            'empresa_nome': f_data_tuple[5]
        }
        
        # Passa os dados completos do funcionário para o diálogo de edição
        dlg = FuncionarioFormDialog(funcionario_data=f_data_dict)
        
        if dlg.exec():
            # A validação de empresa_id agora está no accept_form do dialog
            try:
                salario = float(dlg.salario.text())
            except ValueError:
                QMessageBox.warning(self, "Erro", "Salário inválido! Digite um número válido.")
                return
            if not dlg.nome.text():
                QMessageBox.warning(self, "Erro", "Nome é obrigatório!")
                return

            f = Funcionario(
                id=funcionario_id,
                nome=dlg.nome.text(),
                cargo=dlg.cargo.text(),
                salario=salario,
                empresa_id=dlg.selected_empresa_id # Pega o ID da empresa selecionada no dialog
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

        # Retorna a lista de funcionários com o nome da empresa
        funcionarios_data_for_csv = FuncionarioController.listar()

        # Filtra por empresa se a janela foi aberta com um empresa_id específico
        if self.empresa_id:
            funcionarios_data_for_csv = [f for f in funcionarios_data_for_csv if f[4] == self.empresa_id]

        # Criar DataFrame com os cabeçalhos corretos para a exportação
        df = pd.DataFrame(funcionarios_data_for_csv, columns=["ID", "Nome", "Cargo", "Salário", "ID Empresa", "Empresa"])
        df.to_csv(path, index=False)

        QMessageBox.information(self, "Exportar CSV", f"Arquivo exportado para {path} com sucesso!")


class FuncionarioFormDialog(QDialog):
    # Alterado para aceitar funcionario_data para edição e default_empresa_id para criação no contexto de uma empresa
    def __init__(self, funcionario_data=None, default_empresa_id=None):
        super().__init__()
        self.setWindowTitle("Formulário de Funcionário")
        self.funcionario_data = funcionario_data # Dicionário com os dados do funcionário para edição
        self.default_empresa_id = default_empresa_id # ID da empresa para pré-seleção (se estiver criando um novo funcionário a partir da tela de empresas)
        self.selected_empresa_id = None # Para armazenar o ID da empresa selecionada antes de fechar o diálogo
        
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

        # Novo QComboBox para Empresa
        layout.addWidget(QLabel("Empresa:"))
        self.comboBoxEmpresa = QComboBox()
        layout.addWidget(self.comboBoxEmpresa)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Salvar")
        self.btn_cancel = QPushButton("Cancelar")
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Conecta o botão Salvar ao novo método accept_form para validação
        self.btn_ok.clicked.connect(self.accept_form)
        self.btn_cancel.clicked.connect(self.reject)

        # Carrega as empresas no combobox
        self.load_empresas_into_combobox()
        
        # Preenche o formulário e pré-seleciona a empresa se estiver editando ou criando no contexto de uma empresa
        if self.funcionario_data:
            self.load_funcionario_data_for_editing()
        elif self.default_empresa_id:
            self.set_default_empresa()
            self.comboBoxEmpresa.setEnabled(False)


    def load_empresas_into_combobox(self):
        self.comboBoxEmpresa.clear()
        self.comboBoxEmpresa.addItem("Selecione uma empresa...", userData=None) # Opção padrão "nula"
        empresas = EmpresaController.listar() # Pega todas as empresas
        for empresa_id, nome, cnpj, endereco in empresas:
            self.comboBoxEmpresa.addItem(nome, userData=empresa_id)

    def load_funcionario_data_for_editing(self):
        # funcionario_data agora é um dicionário, mais fácil de acessar
        self.nome.setText(self.funcionario_data['nome'])
        self.cargo.setText(self.funcionario_data['cargo'])
        self.salario.setText(str(self.funcionario_data['salario']))
        
        # Selecionar a empresa correta no combobox
        empresa_id_to_select = self.funcionario_data['empresa_id']
        for i in range(self.comboBoxEmpresa.count()):
            if self.comboBoxEmpresa.itemData(i) == empresa_id_to_select:
                self.comboBoxEmpresa.setCurrentIndex(i)
                break

    def set_default_empresa(self):
        # Se a janela de funcionário foi aberta no contexto de uma empresa, pré-seleciona essa empresa
        if self.default_empresa_id:
            for i in range(self.comboBoxEmpresa.count()):
                if self.comboBoxEmpresa.itemData(i) == self.default_empresa_id:
                    self.comboBoxEmpresa.setCurrentIndex(i)
                    break

    def accept_form(self):
        # Validação para garantir que uma empresa foi selecionada
        if self.comboBoxEmpresa.currentData() is None:
            QMessageBox.warning(self, "Erro", "Por favor, selecione uma empresa para o funcionário!")
            return
        
        # Armazena o ID da empresa selecionada antes de fechar o diálogo
        self.selected_empresa_id = self.comboBoxEmpresa.currentData()
        self.accept() # Chama o método accept() da QDialog para fechar o diálogo
