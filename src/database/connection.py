import psycopg2
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

    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS empresa (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cnpj VARCHAR(20) NOT NULL,
            endereco TEXT
        );
    """)

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
