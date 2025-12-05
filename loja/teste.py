import sqlite3
from pathlib import Path

# Caminho absoluto do db.sqlite3 ao lado do teste.py
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.sqlite3"

# importa as funções do service
from backend.service import (
    criar_tabelas,
    inserir_cliente,
    inserir_telefone,
    inserir_funcionario,
    inserir_gerente,
    inserir_vendedor,
    inserir_carro,
    realizar_negociacao,
    # funções especiais de carga e relatórios:
    carga_clientes_em_massa,
    carga_carros_em_massa,
    carga_funcionarios_em_massa,
    carga_negociacoes_em_massa,
    relatorio_avancado,
    relatorio_vendas_vendedor,
)


def main():
    # abre conexão no MESMO db.sqlite3 do Django/projeto
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute("PRAGMA foreign_keys = ON;")
    cursor = conexao.cursor()

    # 1) Criar estrutura
    criar_tabelas(cursor)
    print(f"✅ Tabelas criadas/verificadas em: {DB_PATH}")

    # 2) Popular dados de exemplo (usando inserts unitários + carga em massa)
    try:
        # --- Clientes (unitário) ---
        inserir_cliente(cursor, 123, "Ana",   "Rua Clarice Lispector")
        inserir_cliente(cursor, 456, "Bruno", "Rua Machado de Assis")
        inserir_cliente(cursor, 789, "Clara", "Rua Vinícius de Moraes")

        # --- Telefones ---
        inserir_telefone(cursor, 85958454392, 123)
        inserir_telefone(cursor, 85988819621, 123)
        inserir_telefone(cursor, 85983679472, 456)
        inserir_telefone(cursor, 85992374142, 789)

        # --- Funcionários (unitário) ---
        inserir_funcionario(cursor, 1001, "Ana Barbosa",    8500.00)
        inserir_funcionario(cursor, 1002, "Carlos Mendes",  9200.00)
        inserir_funcionario(cursor, 2001, "Fernanda Silva", 3000.00)
        inserir_funcionario(cursor, 2002, "João Pereira",   3200.00)
        inserir_funcionario(cursor, 2003, "Larissa Gomes",  3100.00)
        inserir_funcionario(cursor, 2004, "Miguel Andrade", 2900.00)

        # --- Herança 1:1 – Gerente / Vendedor ---
        inserir_gerente(cursor, 1001, 850.00)
        inserir_gerente(cursor, 1002, 900.00)

        inserir_vendedor(cursor, 2001, 150.00)
        inserir_vendedor(cursor, 2002, 180.00)
        inserir_vendedor(cursor, 2003, 160.00)
        inserir_vendedor(cursor, 2004, 170.00)

        # --- Carros (unitário) ---
        inserir_carro(cursor, "CHS1001", "Fiat Argo",       "Prata")
        inserir_carro(cursor, "CHS1002", "Volkswagen Gol",  "Preto")
        inserir_carro(cursor, "CHS1003", "Toyota Corolla",  "Branco")
        inserir_carro(cursor, "CHS1004", "Honda Civic",     "Cinza")
        inserir_carro(cursor, "CHS1005", "Jeep Compass",    "Vermelho")
        inserir_carro(cursor, "CHS1006", "Hyundai HB20",    "Azul")

        # --- Negociações (ternário, unitário) ---
        realizar_negociacao(cursor, 1001, "CHS1001", 123, "2025-11-01",  55000.00)
        realizar_negociacao(cursor, 1002, "CHS1003", 456, "2025-11-03", 142000.00)
        realizar_negociacao(cursor, 2001, "CHS1004", 789, "2025-11-05",  98000.00)
        realizar_negociacao(cursor, 2002, "CHS1002", 456, "2025-11-07",  48000.00)
        realizar_negociacao(cursor, 2003, "CHS1005", 123, "2025-11-09", 168000.00)
        realizar_negociacao(cursor, 2004, "CHS1006", 789, "2025-11-12",  42000.00)

        # --- Exemplo de carga em massa com as novas funções (opcional) ---
        # Clientes extras
        lista_clientes = [
            (111, "Cliente Extra 1", "Endereço 1"),
            (222, "Cliente Extra 2", "Endereço 2"),
        ]
        carga_clientes_em_massa(cursor, lista_clientes)

        # Carros extras
        lista_carros = [
            ("CH-9001", "Civic",   "Prata"),
            ("CH-9002", "Corolla", "Branco"),
        ]
        carga_carros_em_massa(cursor, lista_carros)

        conexao.commit()
        print("✅ Dados de exemplo inseridos com sucesso.")
    except sqlite3.IntegrityError as e:
        # Se rodar duas vezes, vai bater em PK duplicada – aqui a gente só loga
        print(f"⚠️ Inserção ignorada (provavelmente dados já existem): {e}")

    # 3) Rodar relatórios para validar JOIN / GROUP BY
    print("\n📊 Relatório de negociações (JOIN vendedor + carro):")
    rel = relatorio_avancado(cursor)
    for linha in rel:
        print(linha)

    print("\n📈 Relatório de vendas por vendedor (GROUP BY + HAVING):")
    rel2 = relatorio_vendas_vendedor(cursor)
    for linha in rel2:
        print(linha)

    # 4) Encerrar
    conexao.close()
    print("\n✅ Execução do teste.py finalizada.")


if __name__ == "__main__":
    main()
