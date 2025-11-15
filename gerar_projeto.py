import os

# -------------------------
# Conteúdos dos arquivos
# -------------------------

main_py = """from src.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
"""

requirements_txt = """pyside6
psycopg2-binary
python-dotenv
pandas
"""

main_window_py = """from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Empresas e Funcionários")
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
"""

config_py = """DB_NAME = "sistema_empresas"
DB_USER = "postgres"
DB_PASSWORD = "sua_senha"
DB_HOST = "localhost"
DB_PORT = 5432
"""

connection_py = """import psycopg2
from .config import *

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(\""" 
        CREATE TABLE IF NOT EXISTS empresa (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cnpj VARCHAR(20) NOT NULL,
            endereco TEXT
        );
    \""")

    cur.execute(\""" 
        CREATE TABLE IF NOT EXISTS funcionario (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cargo VARCHAR(100),
            salario NUMERIC(10,2),
            empresa_id INTEGER REFERENCES empresa(id)
        );
    \""")

    conn.commit()
    cur.close()
    conn.close()
"""

empresa_py = """class Empresa:
    def __init__(self, id=None, nome=None, cnpj=None, endereco=None):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.endereco = endereco
"""

funcionario_py = """class Funcionario:
    def __init__(self, id=None, nome=None, cargo=None, salario=None, empresa_id=None):
        self.id = id
        self.nome = nome
        self.cargo = cargo
        self.salario = salario
        self.empresa_id = empresa_id
"""

empresa_controller_py = """from src.database.connection import get_connection
from src.models.empresa import Empresa

class EmpresaController:

    @staticmethod
    def criar(empresa: Empresa):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO empresa (nome, cnpj, endereco) VALUES (%s, %s, %s)",
            (empresa.nome, empresa.cnpj, empresa.endereco)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, cnpj, endereco FROM empresa")
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return dados
"""

funcionario_controller_py = """from src.database.connection import get_connection
from src.models.funcionario import Funcionario

class FuncionarioController:

    @staticmethod
    def criar(funcionario: Funcionario):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO funcionario (nome, cargo, salario, empresa_id) VALUES (%s, %s, %s, %s)",
            (funcionario.nome, funcionario.cargo, funcionario.salario, funcionario.empresa_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, cargo, salario, empresa_id FROM funcionario")
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return dados
"""

# -------------------------
# Função que cria o projeto
# -------------------------

def criar_projeto():
    print("📦 Criando estrutura do projeto...")

    estrutura = {
        "Sistema_de_Cadastro_de_Empresas": {
            "main.py": main_py,
            "requirements.txt": requirements_txt,
            # README.md removido
            "src": {
                "__init__.py": "",
                "ui": {
                    "__init__.py": "",
                    "main_window.py": main_window_py
                },
                "database": {
                    "__init__.py": "",
                    "config.py": config_py,
                    "connection.py": connection_py
                },
                "models": {
                    "__init__.py": "",
                    "empresa.py": empresa_py,
                    "funcionario.py": funcionario_py
                },
                "controllers": {
                    "__init__.py": "",
                    "empresa_controller.py": empresa_controller_py,
                    "funcionario_controller.py": funcionario_controller_py
                }
            }
        }
    }

    criar_estrutura(".", estrutura)
    print("✅ Projeto gerado com sucesso!")


def criar_estrutura(base, estrutura):
    for nome, conteudo in estrutura.items():
        caminho = os.path.join(base, nome)

        # Se o conteúdo é um dict → pasta
        if isinstance(conteudo, dict):
            os.makedirs(caminho, exist_ok=True)
            criar_estrutura(caminho, conteudo)
        else:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)


if __name__ == "__main__":
    criar_projeto()
