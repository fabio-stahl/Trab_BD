import sqlite3

def criar_tabelas(cursor):
    # --- CRIAÇÃO DAS TABELAS (DDL) ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cliente (
        CPF INTEGER PRIMARY KEY,
        Nome TEXT NOT NULL,
        Endereco TEXT NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Telefone (
        Numero INTEGER PRIMARY KEY,
        CPF INTEGER,
        FOREIGN KEY (CPF) REFERENCES Cliente(CPF)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Funcionario (
        Matricula INTEGER PRIMARY KEY,
        Nome TEXT NOT NULL,
        Salario REAL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Gerente (
        Matricula INTEGER PRIMARY KEY,
        Vale_alimentacao REAL,
        FOREIGN KEY (Matricula) REFERENCES Funcionario(Matricula) ON DELETE CASCADE
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Vendedor (
        Matricula INTEGER PRIMARY KEY,
        Vale_transporte REAL,
        FOREIGN KEY (Matricula) REFERENCES Funcionario(Matricula) ON DELETE CASCADE
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Carro (
        Chassi TEXT PRIMARY KEY,
        Modelo TEXT NOT NULL,
        Cor TEXT DEFAULT 'Preto' 
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Negociacao (
        ID_Negociacao INTEGER PRIMARY KEY AUTOINCREMENT,
        Matricula INTEGER,
        Chassi TEXT NOT NULL,
        CPF INTEGER,
        Data_Negociacao TEXT NOT NULL,
        Valor_Total REAL,
        FOREIGN KEY (Matricula) REFERENCES Funcionario(Matricula) 
            ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (Chassi) REFERENCES Carro(Chassi) 
            ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (CPF) REFERENCES Cliente(CPF) 
            ON UPDATE CASCADE ON DELETE RESTRICT
    );
    """)
    # --- GATILHO (TRIGGER) --- [cite: 50]
    # Impede negociações com valor zerado ou negativo
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS valida_valor_negociacao
    BEFORE INSERT ON Negociacao
    BEGIN
        SELECT CASE WHEN NEW.Valor_Total <= 0 THEN
            RAISE (ABORT, 'O Valor Total da negociação deve ser positivo.')
        END;
    END;
    """)

# --- OPERAÇÕES CRUD E ESPECÍFICAS ---
