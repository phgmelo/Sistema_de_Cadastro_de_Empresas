import psycopg2
from psycopg2 import sql
from psycopg2.errors import DuplicateDatabase, DuplicateTable

# ============================================
# CONFIGURAÇÕES DO BANCO
# ============================================
DB_USER = "postgres"
DB_PASSWORD = "123senha"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "sistema_empresas"


# ============================================
# FUNÇÃO DE CONEXÃO GENÉRICA
# ============================================
def connect(db_name):
    """Retorna uma conexão para um banco específico."""
    return psycopg2.connect(
        dbname=db_name,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


# ============================================
# CRIAÇÃO DO BANCO DE DADOS
# ============================================
def create_database():
    try:
        print("🔍 Verificando banco de dados...")

        conn = connect("postgres")
        conn.autocommit = True
        cur = conn.cursor()

        # Verifica se o BD existe
        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_NAME,)
        )
        exists = cur.fetchone()

        if exists:
            print(f"ℹ️ Banco '{DB_NAME}' já existe. Pulando criação.")
        else:
            print(f"🛠 Criando banco de dados '{DB_NAME}'...")
            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_NAME)
            ))
            print(f"✅ Banco '{DB_NAME}' criado com sucesso!")

        cur.close()
        conn.close()

    except DuplicateDatabase:
        print(f"⚠️ Banco '{DB_NAME}' já existe (erro ignorado).")

    except Exception as e:
        print("❌ Erro ao criar banco de dados:", e)


# ============================================
# CRIAÇÃO DAS TABELAS
# ============================================
def create_tables():
    try:
        print("🔍 Conectando ao banco para criar tabelas...")
        conn = connect(DB_NAME)
        cur = conn.cursor()

        print("🛠 Criando tabela empresa...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS empresa (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                cnpj VARCHAR(20) NOT NULL,
                endereco TEXT
            );
        """)

        print("🛠 Criando tabela funcionario...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS funcionario (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                cargo VARCHAR(100),
                salario NUMERIC(10,2),
                empresa_id INTEGER REFERENCES empresa(id)
            );
        """)

        conn.commit()
        cur.close()
        conn.close()

        print("✅ Tabelas criadas com sucesso!")

    except DuplicateTable:
        print("⚠️ Tabela já existe (erro ignorado).")

    except Exception as e:
        print("❌ Erro ao criar tabelas:", e)


# ============================================
# EXECUÇÃO PRINCIPAL
# ============================================
if __name__ == "__main__":
    print("====================================")
    print("🚀 Iniciando configuração do sistema")
    print("====================================")

    create_database()
    create_tables()

    print("====================================")
    print("🏁 Finalizado com sucesso!")
    print("====================================")
