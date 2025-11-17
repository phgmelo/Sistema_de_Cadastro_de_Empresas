# C:\Users\maru_\Sistema_de_Cadastro_de_Empresas\src\database\config.py

from dotenv import dotenv_values
config_env = dotenv_values(".env")
DB_NAME = config_env.get("DB_NAME")
DB_USER = config_env.get("DB_USER")
DB_PASSWORD = config_env.get("DB_PASSWORD")
DB_HOST = config_env.get("DB_HOST")
DB_PORT = int(config_env.get("DB_PORT, 5432"))
