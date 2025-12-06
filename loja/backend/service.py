import sqlite3

# --- 1. CRIAÇÃO DE ESTRUTURA (DDL) ---

def criar_tabelas(cursor):
    """
    Cria a estrutura do banco de dados atendendo aos requisitos:
    - 6 tabelas no mínimo
    - Relacionamentos 1:1, 1:N, N:N, Ternário
    - Valor padrão e Gatilhos
    """
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cliente (
        CPF INTEGER PRIMARY KEY,
        Nome TEXT NOT NULL,
        Endereco TEXT NOT NULL
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

    # 🔒 Cada chassi só pode aparecer UMA vez em Negociacao
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_negociacao_chassi_unico
    ON Negociacao(Chassi);
    """)

    # --- GATILHO (TRIGGER) ---
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS valida_valor_negociacao
    BEFORE INSERT ON Negociacao
    BEGIN
        SELECT CASE WHEN NEW.Valor_Total <= 0 THEN
            RAISE (ABORT, 'O Valor Total da negociação deve ser positivo.')
        END;
    END;
    """)

# --- 2. OPERAÇÕES DE INSERÇÃO (CREATE) ---

def inserir_cliente(cursor, cpf, nome, endereco):
    cursor.execute(
        "INSERT INTO Cliente (CPF, Nome, Endereco) VALUES (?, ?, ?)",
        (cpf, nome, endereco)
    )

def inserir_telefone(cursor, numero, cpf):
    cursor.execute(
        "INSERT INTO Telefone (Numero, CPF) VALUES (?, ?)",
        (numero, cpf)
    )

def inserir_funcionario(cursor, matricula, nome, salario):
    cursor.execute(
        "INSERT INTO Funcionario (Matricula, Nome, Salario) VALUES (?, ?, ?)",
        (matricula, nome, salario)
    )

def inserir_gerente(cursor, matricula, vale_alimentacao):
    cursor.execute(
        "INSERT INTO Gerente (Matricula, Vale_alimentacao) VALUES (?, ?)",
        (matricula, vale_alimentacao)
    )

def inserir_vendedor(cursor, matricula, vale_transporte):
    cursor.execute(
        "INSERT INTO Vendedor (Matricula, Vale_transporte) VALUES (?, ?)",
        (matricula, vale_transporte)
    )

def inserir_carro(cursor, chassi, modelo, cor):
    if cor and cor.strip() == "":
        cor = None
    cursor.execute(
        "INSERT INTO Carro (Chassi, Modelo, Cor) VALUES (?, ?, ?)",
        (chassi, modelo, cor)
    )

def realizar_negociacao(cursor, matricula, chassi, cpf, data, valor):
    """
    Regras de negócio:
    - Funcionário deve existir
    - Carro deve existir
    - Cliente deve existir
    - Um mesmo chassi só pode aparecer em UMA negociação.
    """
    # Funcionário
    cursor.execute("SELECT 1 FROM Funcionario WHERE Matricula = ?", (matricula,))
    if cursor.fetchone() is None:
        raise Exception("Funcionário (Matrícula) inexistente para esta negociação.")

    # Carro
    cursor.execute("SELECT 1 FROM Carro WHERE Chassi = ?", (chassi,))
    if cursor.fetchone() is None:
        raise Exception("Carro (Chassi) inexistente para esta negociação.")

    # Cliente
    cursor.execute("SELECT 1 FROM Cliente WHERE CPF = ?", (cpf,))
    if cursor.fetchone() is None:
        raise Exception("Cliente (CPF) inexistente para esta negociação.")

    # Chassi único
    cursor.execute("SELECT CPF FROM Negociacao WHERE Chassi = ?", (chassi,))
    row = cursor.fetchone()
    if row is not None:
        raise Exception(
            f"Este carro (Chassi {chassi}) já foi negociado com o CPF {row[0]}."
        )

    cursor.execute("""
        INSERT INTO Negociacao (Matricula, Chassi, CPF, Data_Negociacao, Valor_Total)
        VALUES (?, ?, ?, ?, ?)
    """, (matricula, chassi, cpf, data, valor))

# --- 3. OPERAÇÕES DE LEITURA (READ) ---

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
    cursor.execute(
        "SELECT * FROM Negociacao WHERE ID_Negociacao = ?",
        (id_negociacao,)
    )
    return cursor.fetchone()

def listar_todos_clientes(cursor):
    cursor.execute("SELECT * FROM Cliente")
    return cursor.fetchall()

def listar_todos_funcionarios(cursor):
    cursor.execute("SELECT * FROM Funcionario")
    return cursor.fetchall()

def listar_todos_carros(cursor):
    cursor.execute("SELECT * FROM Carro")
    return cursor.fetchall()

def listar_todas_negociacoes(cursor):
    cursor.execute("SELECT * FROM Negociacao")
    return cursor.fetchall()

def listar_todos_telefones(cursor):
    cursor.execute("SELECT * FROM Telefone")
    return cursor.fetchall()

# --- 4. OPERAÇÕES DE ATUALIZAÇÃO (UPDATE) ---

def atualizar_cliente(cursor, cpf, nome, endereco):
    cursor.execute(
        "UPDATE Cliente SET Nome = ?, Endereco = ? WHERE CPF = ?",
        (nome, endereco, cpf)
    )

def atualizar_funcionario(cursor, matricula, nome, salario):
    cursor.execute(
        "UPDATE Funcionario SET Nome = ?, Salario = ? WHERE Matricula = ?",
        (nome, salario, matricula)
    )

def atualizar_vendedor(cursor, matricula, vale_transporte):
    cursor.execute(
        "UPDATE Vendedor SET Vale_transporte = ? WHERE Matricula = ?",
        (vale_transporte, matricula)
    )

def atualizar_gerente(cursor, matricula, vale_alimentacao):
    cursor.execute(
        "UPDATE Gerente SET Vale_alimentacao = ? WHERE Matricula = ?",
        (vale_alimentacao, matricula)
    )

def atualizar_carro(cursor, chassi, modelo, cor):
    cursor.execute(
        "UPDATE Carro SET Modelo = ?, Cor = ? WHERE Chassi = ?",
        (modelo, cor, chassi)
    )

def atualizar_negociacao(cursor, id_negociacao, matricula, chassi, cpf, data, valor):
    cursor.execute("""
        UPDATE Negociacao 
        SET Matricula = ?, 
            Chassi = ?, 
            CPF = ?, 
            Data_Negociacao = ?, 
            Valor_Total = ?
        WHERE ID_Negociacao = ?
    """, (matricula, chassi, cpf, data, valor, id_negociacao))
    print("DEBUG atualizar_negociacao - linhas afetadas:", cursor.rowcount)

# --- 5. OPERAÇÕES DE REMOÇÃO (DELETE) ---

def deletar_cliente(cursor, cpf):
    cursor.execute("DELETE FROM Cliente WHERE CPF = ?", (cpf,))

def deletar_funcionario(cursor, matricula):
    cursor.execute("DELETE FROM Funcionario WHERE Matricula = ?", (matricula,))

def deletar_carro(cursor, chassi):
    cursor.execute("DELETE FROM Carro WHERE Chassi = ?", (chassi,))

def deletar_negociacao(cursor, id_negociacao):
    cursor.execute(
        "DELETE FROM Negociacao WHERE ID_Negociacao = ?",
        (id_negociacao,)
    )

def deletar_telefone(cursor, cpf, numero):
    cursor.execute(
        "DELETE FROM Telefone WHERE CPF = ? AND Numero = ?",
        (cpf, numero)
    )

# --- 6. OPERAÇÕES ESPECIAIS (REQUISITOS AVANÇADOS) ---

def carga_clientes_em_massa(cursor, lista_dados):
    query = "INSERT OR IGNORE INTO Cliente (CPF, Nome, Endereco) VALUES (?, ?, ?)"
    cursor.executemany(query, lista_dados)

def carga_carros_em_massa(cursor, lista_dados):
    query = "INSERT OR IGNORE INTO Carro (Chassi, Modelo, Cor) VALUES (?, ?, ?)"
    cursor.executemany(query, lista_dados)

def carga_funcionarios_em_massa(cursor, lista_dados):
    query = "INSERT OR IGNORE INTO Funcionario (Matricula, Nome, Salario) VALUES (?, ?, ?)"
    cursor.executemany(query, lista_dados)

def carga_negociacoes_em_massa(cursor, lista_dados):
    query = """
        INSERT INTO Negociacao (Matricula, Chassi, CPF, Data_Negociacao, Valor_Total)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.executemany(query, lista_dados)

def buscar_carro_substring(cursor, termo):
    termo_formatado = f"%{termo.lower()}%"
    cursor.execute("SELECT * FROM Carro WHERE Modelo LIKE ?", (termo_formatado,))
    return cursor.fetchall()

def buscar_cliente_substring(cursor, termo):
    termo_formatado = f"%{termo.lower()}%"
    cursor.execute("SELECT * FROM Cliente WHERE Nome LIKE ?", (termo_formatado,))
    return cursor.fetchall()

def buscar_funcionario_substring(cursor, termo):
    termo_formatado = f"%{termo.lower()}%"
    cursor.execute("SELECT * FROM Funcionario WHERE Nome LIKE ?", (termo_formatado,))
    return cursor.fetchall()

def relatorio_avancado(cursor):
    query = """
    SELECT f.Nome as Vendedor, c.Modelo, n.Valor_Total
    FROM Negociacao n
    INNER JOIN Funcionario f ON n.Matricula = f.Matricula
    LEFT JOIN Carro c ON n.Chassi = c.Chassi
    ORDER BY n.Valor_Total DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

def relatorio_inner_join(cursor):
    """
    INNER JOIN: Traz apenas os dados que têm correspondência nas duas tabelas.
    Cenário: Listar apenas vendas concretizadas, ignorando funcionários sem vendas.
    """
    query = """
    SELECT n.ID_Negociacao, f.Nome as Vendedor, n.Valor_Total
    FROM Negociacao n
    INNER JOIN Funcionario f ON n.Matricula = f.Matricula
    ORDER BY n.ID_Negociacao
    """
    cursor.execute(query)
    return cursor.fetchall()

def relatorio_left_join(cursor):
    """
    LEFT JOIN: Traz todos os registros da tabela da ESQUERDA (Funcionario),
    mesmo que não tenha correspondência na direita (Negociacao).
    Cenário: Listar TODOS os funcionários e suas vendas (se houver).
    """
    query = """
    SELECT f.Nome as Funcionario, n.ID_Negociacao, n.Valor_Total
    FROM Funcionario f
    LEFT JOIN Negociacao n ON f.Matricula = n.Matricula
    ORDER BY f.Nome
    """
    cursor.execute(query)
    return cursor.fetchall()

def relatorio_right_join_simulado(cursor):
    """
    RIGHT JOIN (Simulado no SQLite): O SQLite não tem RIGHT JOIN.
    Lógica: "Trazer todos os Carros (Direita), mesmo que não estejam em Negociação (Esquerda)".
    Solução: Invertemos para 'FROM Carro LEFT JOIN Negociacao'.
    """
    query = """
    SELECT c.Modelo, c.Cor, n.Data_Negociacao, 
           CASE WHEN n.ID_Negociacao IS NULL THEN 'Disponível' ELSE 'Vendido' END as Status
    FROM Carro c
    LEFT JOIN Negociacao n ON c.Chassi = n.Chassi
    ORDER BY c.Modelo
    """
    cursor.execute(query)
    return cursor.fetchall()

def consulta_quantificador_any(cursor):
    query = """
    SELECT f.Nome, n1.Valor_Total
    FROM Negociacao n1
    JOIN Funcionario f ON n1.Matricula = f.Matricula
    WHERE n1.Valor_Total > (
        SELECT AVG(n2.Valor_Total)
        FROM Negociacao n2
        WHERE n2.Matricula = n1.Matricula
    )
    """
    cursor.execute(query)
    return cursor.fetchall()

def relatorio_media_vendas_por_modelo(cursor):
    query = """
    SELECT c.Modelo, COUNT(n.ID_Negociacao) as Qtd, AVG(n.Valor_Total) as Media_Valor
    FROM Negociacao n
    INNER JOIN Carro c ON n.Chassi = c.Chassi
    GROUP BY c.Modelo
    ORDER BY Qtd DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

def consulta_quantificador_any(cursor):
    query = """
    SELECT f.Nome, n1.Valor_Total
    FROM Negociacao n1
    JOIN Funcionario f ON f.Matricula = n1.Matricula
    WHERE n1.Valor_Total > (
        SELECT MIN(n2.Valor_Total)
        FROM Negociacao n2
        WHERE n2.Matricula = n1.Matricula
    )
    """
    cursor.execute(query)
    return cursor.fetchall()

def consulta_quantificador_all(cursor):
    query = """
    SELECT f.Nome, n1.Valor_Total
    FROM Negociacao n1
    JOIN Funcionario f ON f.Matricula = n1.Matricula
    WHERE n1.Valor_Total > (
        SELECT MAX(n2.Valor_Total)
        FROM Negociacao n2
        WHERE n2.Matricula = n1.Matricula
          AND n2.ID_Negociacao <> n1.ID_Negociacao
    )
    """
    cursor.execute(query)
    return cursor.fetchall()
def relatorio_vendas_vendedor(cursor):
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

def relatorio_vendas_por_cor(cursor):
    """
    Agrupamento de vendas por COR do carro
    """
    query = """
    SELECT c.Cor, COUNT(n.ID_Negociacao) as Qtd_Vendas, SUM(n.Valor_Total) as Total_Faturado
    FROM Negociacao n
    INNER JOIN Carro c ON n.Chassi = c.Chassi
    GROUP BY c.Cor
    ORDER BY Total_Faturado DESC
    """
    cursor.execute(query)
    return cursor.fetchall()


def relatorio_vendas_por_cliente(cursor):
    """
    Agrupamento de vendas por CLIENTE
    """
    query = """
    SELECT cl.Nome, COUNT(n.ID_Negociacao) as Qtd_Vendas, SUM(n.Valor_Total) as Total_Faturado
    FROM Negociacao n
    INNER JOIN Cliente cl ON n.CPF = cl.CPF
    GROUP BY cl.Nome
    ORDER BY Total_Faturado DESC
    """
    cursor.execute(query)
    return cursor.fetchall()


def relatorio_vendas_por_funcionario(cursor):
    """
    Agrupamento de vendas por FUNCIONÁRIO (geral)
    """
    query = """
    SELECT f.Nome, COUNT(n.ID_Negociacao) as Qtd_Vendas, SUM(n.Valor_Total) as Total_Faturado
    FROM Negociacao n
    INNER JOIN Funcionario f ON n.Matricula = f.Matricula
    GROUP BY f.Nome
    ORDER BY Total_Faturado DESC
    """
    cursor.execute(query)
    return cursor.fetchall()


def relatorio_vendas_por_data(cursor):
    """
    Agrupamento de vendas por DATA da negociação
    """
    query = """
    SELECT n.Data_Negociacao, COUNT(n.ID_Negociacao) as Qtd_Vendas, SUM(n.Valor_Total) as Total_Faturado
    FROM Negociacao n
    GROUP BY n.Data_Negociacao
    ORDER BY n.Data_Negociacao DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

def relatorio_vendas_vendedor_minimo(cursor, minimo):
    """
    Variante com HAVING parametrizado (mínimo de faturamento).
    """
    query = """
    SELECT f.Nome,
           COUNT(n.ID_Negociacao) as Qtd_Vendas,
           SUM(n.Valor_Total) as Total_Faturado
    FROM Funcionario f
    LEFT JOIN Negociacao n ON f.Matricula = n.Matricula
    GROUP BY f.Nome
    HAVING Total_Faturado >= ?
    ORDER BY Total_Faturado DESC
    """
    cursor.execute(query, (minimo,))
    return cursor.fetchall()

def relatorio_ordenado(cursor, tipo, ordem):
    """
    Consulta com ordenação configurável (ASC/DESC).
    tipo: "modelo" ou "vendedor"
    ordem: "ASC" ou "DESC"
    """
    ordem_sql = "DESC" if str(ordem).upper() != "ASC" else "ASC"

    if tipo == "modelo":
        query = f"""
        SELECT c.Modelo,
               COUNT(n.ID_Negociacao) as Qtd,
               AVG(n.Valor_Total) as Media_Valor
        FROM Negociacao n
        INNER JOIN Carro c ON n.Chassi = c.Chassi
        GROUP BY c.Modelo
        ORDER BY Media_Valor {ordem_sql}
        """
        cursor.execute(query)
    else:
        query = f"""
        SELECT f.Nome,
               COUNT(n.ID_Negociacao) as Qtd_Vendas,
               SUM(n.Valor_Total) as Total_Faturado
        FROM Funcionario f
        LEFT JOIN Negociacao n ON f.Matricula = n.Matricula
        GROUP BY f.Nome
        ORDER BY Total_Faturado {ordem_sql}
        """
        cursor.execute(query)

    return cursor.fetchall()
