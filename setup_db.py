import psycopg2
from psycopg2 import sql
# from psycopg2.errors import DuplicateDatabase, DuplicateTable # DuplicateDatabase é pego por Exception, DuplicateTable é coberto por IF NOT EXISTS
from dotenv import dotenv_values
from pathlib import Path

# ============================================
# LOAD .ENV SAFELY
# ============================================
# Assume que o .env está na mesma pasta do setup_db.py (raiz do projeto)
env_path = Path(__file__).resolve().parent / ".env" 
config_env = dotenv_values(env_path)

DB_USER = config_env.get("DB_USER")
DB_PASSWORD = config_env.get("DB_PASSWORD")
DB_HOST = config_env.get("DB_HOST")
DB_PORT = int(config_env.get("DB_PORT", 5432)) # Adiciona um default seguro para a porta
DB_NAME = config_env.get("DB_NAME")


# ============================================
# FUNÇÃO DE CONEXÃO
# ============================================
def connect(db_name):
    return psycopg2.connect(
        dbname=db_name,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


# ============================================
# CRIAÇÃO DO BANCO
# ============================================
def create_database():
    try:
        print("🔍 Verificando banco de dados...")

        # Conecta ao banco 'postgres' (padrão) para poder criar o novo banco de dados
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_NAME,)
        )
        exists = cur.fetchone()

        if exists:
            print(f"ℹ️ Banco '{DB_NAME}' já existe.")
        else:
            print(f"🛠 Criando banco: {DB_NAME}")
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print("✅ Banco criado!")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Erro ao criar banco: {e}")


# ============================================
# CRIAÇÃO DAS TABELAS
# ============================================
def create_tables():
    try:
        print("🔍 Conectando ao banco...")
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

    except Exception as e: # Removida a captura específica de DuplicateTable
        print(f"❌ Erro ao criar tabelas: {e}")


# ============================================
# MAIN
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