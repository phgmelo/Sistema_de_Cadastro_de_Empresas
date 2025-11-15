from src.database.connection import get_connection
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

    @staticmethod
    def atualizar(empresa: Empresa):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE empresa SET nome=%s, cnpj=%s, endereco=%s WHERE id=%s",
            (empresa.nome, empresa.cnpj, empresa.endereco, empresa.id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def deletar(empresa_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM empresa WHERE id=%s", (empresa_id,))
        conn.commit()
        cur.close()
        conn.close()
