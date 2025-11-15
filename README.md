# 📦 Sistema de Gerenciamento de Empresas e Funcionários

![Python](https://img.shields.io/badge/Python-3.12)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento-yellow)

Sistema de gerenciamento desenvolvido em **Python + PySide6** com persistência em **PostgreSQL**.
Permite gerenciar empresas e seus respectivos funcionários através de uma interface gráfica moderna e intuitiva.

---

## 🔗 **Links Importantes**

- 🔹 **Repositório do GitHub:**
  https://github.com/phgmelo/Sistema_de_Cadastro_de_Empresas
- 🔹 **Documentação PySide6:**
  https://doc.qt.io/qtforpython/
- 🔹 **PostgreSQL:**
  https://www.postgresql.org/download/

---

## 🧰 **Funcionalidades Principais**

- ✔️ CRUD completo de **empresas**
- ✔️ CRUD completo de **funcionários**
- ✔️ Visualização de funcionários por empresa
- ✔️ Interface gráfica responsiva com **PySide6**
- ✔️ Persistência em banco de dados relacional (**PostgreSQL**)

---

## ⭐ **Funcionalidades Bônus**

- 🔍 Busca por nome (empresa ou funcionário)
- 🔒 Validação de CNPJ
- 🧾 Exportação de funcionários para CSV
- 🛠️ **Criação automática do banco via script (`setup_db.py`)**
- ⚙️ **Geração automatizada da estrutura do projeto (`gerar_projeto.py`)**

---

## 🧱 **Arquitetura do Projeto**

```
/src
├── /controllers -> Regras de negócio
├── /database -> Conexão e queries com PostgreSQL
├── /models -> Classes Empresa e Funcionario
└── /ui -> Interface PySide6 (.ui ou .py)
main.py -> Arquivo principal da aplicação
requirements.txt -> Dependências do projeto
README.md -> Documentação do projeto
```

---

## 📦 **Instalação do Ambiente**

### 1️⃣ **Clone o repositório**

```bash
git clone git@github-paulo:phgmelo/Sistema_de_Cadastro_de_Empresas.git
cd Sistema_de_Cadastro_de_Empresas
```

### 🐍 2️⃣ Crie o ambiente virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 📦 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 🗄️ 4️⃣ Configuração do Banco PostgreSQL

Crie o banco:

```sql
CREATE DATABASE sistema_empresas;
```

Edite o arquivo (exemplo em `src/database/config.py`):

```python
DB_NAME = "sistema_empresas"
DB_USER = "postgres"
DB_PASSWORD = "sua_senha_aqui"
DB_HOST = "localhost"
DB_PORT = 5432
```

### ▶️ 5️⃣ Executar o Sistema

```bash
python main.py
```

---

## 💡 Futuras Melhorias

- 📊 Dashboard com gráficos
- 🔑 Acesso por usuário e permissões
- ☁️ Integração com API externa de CNPJ
- 🖨️ Relatórios PDF

---

## 🤝 Contribuição

Pull requests são bem-vindos.
Antes de enviar, abra uma issue explicando sua sugestão.

---

## 📄 Licença

Distribuído sob a licença MIT.
