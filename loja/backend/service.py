import sqlite3

# --- 1. CRIAÇÃO DE ESTRUTURA (DDL) ---

def criar_tabelas(cursor):
    """
    Cria a estrutura do banco de dados atendendo aos requisitos:
    - 6 tabelas no mínimo [cite: 13]
    - Relacionamentos 1:1, 1:N, N:N, Ternário [cite: 22, 23, 24, 25]
    - Valor padrão e Gatilhos [cite: 16, 50]
    """
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
    CREATE TABLE IF NOT EXISTS Telefone (
        Numero INTEGER PRIMARY KEY,
        CPF INTEGER,
        FOREIGN KEY (CPF) REFERENCES Cliente(CPF) ON DELETE CASCADE
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
    # Requisito: Gatilho em inserção para validar dados
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS valida_valor_negociacao
    BEFORE INSERT ON Negociacao
    BEGIN
        SELECT CASE WHEN NEW.Valor_Total <= 0 THEN
            RAISE (ABORT, 'O Valor Total da negociação deve ser positivo.')
        END;
    END;
    """)

# --- 2. OPERAÇÕES DE INSERÇÃO (CREATE) --- [cite: 32]

def inserir_cliente(cursor, cpf, nome, endereco):
    cursor.execute("INSERT INTO Cliente (CPF, Nome, Endereco) VALUES (?, ?, ?)", (cpf, nome, endereco))

def inserir_telefone(cursor, numero, cpf):
    cursor.execute("INSERT INTO Telefone (Numero, CPF) VALUES (?, ?)", (numero, cpf))

def inserir_funcionario(cursor, matricula, nome, salario):
    cursor.execute("INSERT INTO Funcionario (Matricula, Nome, Salario) VALUES (?, ?, ?)", (matricula, nome, salario))

def inserir_gerente(cursor, matricula, vale_alimentacao):
    # Relacionamento 1:1 (Herança)
    cursor.execute("INSERT INTO Gerente (Matricula, Vale_alimentacao) VALUES (?, ?)", (matricula, vale_alimentacao))

def inserir_vendedor(cursor, matricula, vale_transporte):
    # Relacionamento 1:1 (Herança)
    cursor.execute("INSERT INTO Vendedor (Matricula, Vale_transporte) VALUES (?, ?)", (matricula, vale_transporte))

def inserir_carro(cursor, chassi, modelo, cor):
    # Se cor for None, o banco usará o DEFAULT 'Preto'
    if cor and cor.strip() == "":
        cor = None
    cursor.execute("INSERT INTO Carro (Chassi, Modelo, Cor) VALUES (?, ?, ?)", (chassi, modelo, cor))

def realizar_negociacao(cursor, matricula, chassi, cpf, data, valor):
    # Relacionamento Ternário
    cursor.execute("""
        INSERT INTO Negociacao (Matricula, Chassi, CPF, Data_Negociacao, Valor_Total)
        VALUES (?, ?, ?, ?, ?)
    """, (matricula, chassi, cpf, data, valor))

# --- 3. OPERAÇÕES DE LEITURA (READ) --- [cite: 35]

def buscar_cliente(cursor, cpf):
    cursor.execute("SELECT * FROM Cliente WHERE CPF = ?", (cpf,))
    return cursor.fetchone()

def buscar_telefone(cursor, numero):
    cursor.execute("SELECT * FROM Telefone WHERE Numero = ?", (numero,))
    return cursor.fetchone()

def buscar_funcionario(cursor, matricula):
    cursor.execute("SELECT * FROM Funcionario WHERE Matricula = ?", (matricula,))
    return cursor.fetchone()

def buscar_carro(cursor, chassi):
    cursor.execute("SELECT * FROM Carro WHERE Chassi = ?", (chassi,))
    return cursor.fetchone()

def buscar_negociacao(cursor, id_negociacao):
    cursor.execute("SELECT * FROM Negociacao WHERE ID_Negociacao = ?", (id_negociacao,))
    return cursor.fetchone()

# --- 4. OPERAÇÕES DE ATUALIZAÇÃO (UPDATE) --- [cite: 33]

def atualizar_cliente(cursor, cpf, nome, endereco):
    cursor.execute("UPDATE Cliente SET Nome = ?, Endereco = ? WHERE CPF = ?", (nome, endereco, cpf))

def atualizar_funcionario(cursor, matricula, nome, salario):
    cursor.execute("UPDATE Funcionario SET Nome = ?, Salario = ? WHERE Matricula = ?", (nome, salario, matricula))

def atualizar_carro(cursor, chassi, modelo, cor):
    cursor.execute("UPDATE Carro SET Modelo = ?, Cor = ? WHERE Chassi = ?", (modelo, cor, chassi))

# --- 5. OPERAÇÕES DE REMOÇÃO (DELETE) --- [cite: 32]

def deletar_cliente(cursor, cpf):
    cursor.execute("DELETE FROM Cliente WHERE CPF = ?", (cpf,))

def deletar_funcionario(cursor, matricula):
    # O DELETE CASCADE configurado no banco deve remover Gerente/Vendedor automaticamente
    cursor.execute("DELETE FROM Funcionario WHERE Matricula = ?", (matricula,))

def deletar_carro(cursor, chassi):
    cursor.execute("DELETE FROM Carro WHERE Chassi = ?", (chassi,))

def deletar_negociacao(cursor, id_negociacao):
    cursor.execute("DELETE FROM Negociacao WHERE ID_Negociacao = ?", (id_negociacao,))

# --- 6. OPERAÇÕES ESPECIAIS (REQUISITOS AVANÇADOS) ---
def carga_clientes_em_massa(cursor, lista_dados):
    """
    Recebe uma lista de tuplas: [(CPF, Nome, Endereco), ...]
    """
    query = "INSERT OR IGNORE INTO Cliente (CPF, Nome, Endereco) VALUES (?, ?, ?)"
    cursor.executemany(query, lista_dados)

def carga_carros_em_massa(cursor, lista_dados):
    """
    Recebe uma lista de tuplas: [(Chassi, Modelo, Cor), ...]
    """
    query = "INSERT OR IGNORE INTO Carro (Chassi, Modelo, Cor) VALUES (?, ?, ?)"
    cursor.executemany(query, lista_dados)

def carga_funcionarios_em_massa(cursor, lista_dados):
    """
    Recebe uma lista de tuplas: [(Matricula, Nome, Salario), ...]
    """
    query = "INSERT OR IGNORE INTO Funcionario (Matricula, Nome, Salario) VALUES (?, ?, ?)"
    cursor.executemany(query, lista_dados)

def carga_negociacoes_em_massa(cursor, lista_dados):
    """
    Recebe lista: [(Matricula, Chassi, CPF, Data, Valor), ...]
    """
    query = """
        INSERT INTO Negociacao (Matricula, Chassi, CPF, Data_Negociacao, Valor_Total)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.executemany(query, lista_dados)

def buscar_carro_substring(cursor, termo):
    """
    Requisito: Busca com Substring case insensitive. [cite: 40, 41]
    """
    termo_formatado = f"%{termo}%"
    cursor.execute("SELECT * FROM Carro WHERE Modelo LIKE ?", (termo_formatado,))
    return cursor.fetchall()

def buscar_cliente_substring(cursor, termo):
    """
    Busca clientes cujo NOME contenha o termo pesquisado.
    """
    termo_formatado = f"%{termo}%"
    cursor.execute("SELECT * FROM Cliente WHERE Nome LIKE ?", (termo_formatado,))
    return cursor.fetchall()

def buscar_funcionario_substring(cursor, termo):
    """
    Busca funcionários cujo NOME contenha o termo pesquisado.
    """
    termo_formatado = f"%{termo}%"
    cursor.execute("SELECT * FROM Funcionario WHERE Nome LIKE ?", (termo_formatado,))
    return cursor.fetchall()

def relatorio_avancado(cursor):
    """
    Requisito: Pelo menos dois tipos diferentes de JOIN. [cite: 44]
    Retorna: Nome do Vendedor, Modelo do Carro vendido e Valor da venda.
    """
    query = """
    SELECT f.Nome as Vendedor, c.Modelo, n.Valor_Total
    FROM Negociacao n
    INNER JOIN Funcionario f ON n.Matricula = f.Matricula
    INNER JOIN Carro c ON n.Chassi = c.Chassi
    ORDER BY n.Valor_Total DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

def consulta_quantificador_any(cursor):
    """
    Requisito: Consulta com quantificador ALL ou ANY (simulado com IN/Subquery). [cite: 46]
    Retorna funcionarios que venderam carros com valor acima da média geral de vendas.
    """
    query = """
    SELECT Nome FROM Funcionario 
    WHERE Matricula IN (
        SELECT Matricula FROM Negociacao 
        WHERE Valor_Total > (SELECT AVG(Valor_Total) FROM Negociacao)
    )
    """
    cursor.execute(query)
    return cursor.fetchall()

def relatorio_vendas_vendedor(cursor):
    """
    Requisito: Consulta com Group By, Having e Ordenação. [cite: 48, 49]
    """
    query = """
    SELECT f.Nome, COUNT(n.ID_Negociacao) as Qtd_Vendas, SUM(n.Valor_Total) as Total_Faturado
    FROM Funcionario f
    LEFT JOIN Negociacao n ON f.Matricula = n.Matricula
    GROUP BY f.Nome
    HAVING Total_Faturado > 0
    ORDER BY Total_Faturado DESC
    """
    cursor.execute(query)
    return cursor.fetchall()