from src.database.connection import get_connection
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

    @staticmethod
    def atualizar(funcionario: Funcionario):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE funcionario SET nome=%s, cargo=%s, salario=%s, empresa_id=%s WHERE id=%s",
            (funcionario.nome, funcionario.cargo, funcionario.salario, funcionario.empresa_id, funcionario.id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def deletar(funcionario_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM funcionario WHERE id=%s", (funcionario_id,))
        conn.commit()
        cur.close()
        conn.close()
