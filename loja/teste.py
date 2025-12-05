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
    # buscas
    buscar_cliente,
    buscar_funcionario,
    buscar_carro,
    buscar_negociacao,
    buscar_cliente_substring,
    buscar_funcionario_substring,
    buscar_carro_substring,
    # updates
    atualizar_cliente,
    atualizar_funcionario,
    atualizar_carro,
    # deletes
    deletar_cliente,
    deletar_funcionario,
    deletar_carro,
    deletar_negociacao,
    # relatórios
    relatorio_avancado,
    relatorio_vendas_vendedor,
)

def cadastrar_cliente(cursor, conn):
    print("\n🧍 Cadastro de Cliente")
    cpf = int(input("CPF (somente números): ").strip())
    nome = input("Nome: ").strip()
    endereco = input("Endereço: ").strip()
    inserir_cliente(cursor, cpf, nome, endereco)
    conn.commit()
    print("✅ Cliente cadastrado com sucesso.")


def cadastrar_telefone(cursor, conn):
    print("\n📞 Cadastro de Telefone")
    numero = int(input("Número (somente números): ").strip())
    cpf = int(input("CPF do cliente: ").strip())
    inserir_telefone(cursor, numero, cpf)
    conn.commit()
    print("✅ Telefone cadastrado com sucesso.")


def cadastrar_funcionario(cursor, conn):
    print("\n👷 Cadastro de Funcionário")
    matricula = int(input("Matrícula: ").strip())
    nome = input("Nome: ").strip()
    salario = float(input("Salário: ").replace(",", ".").strip())
    inserir_funcionario(cursor, matricula, nome, salario)

    tipo = input("Esse funcionário é (g)erente, (v)endedor ou (n)enhum? [g/v/n]: ").strip().lower()
    if tipo == "g":
        vale = float(input("Vale alimentação: ").replace(",", ".").strip())
        inserir_gerente(cursor, matricula, vale)
    elif tipo == "v":
        vale = float(input("Vale transporte: ").replace(",", ".").strip())
        inserir_vendedor(cursor, matricula, vale)

    conn.commit()
    print("✅ Funcionário cadastrado com sucesso.")


def cadastrar_carro(cursor, conn):
    print("\n🚗 Cadastro de Carro")
    chassi = input("Chassi: ").strip()
    modelo = input("Modelo: ").strip()
    cor = input("Cor (deixe vazio para usar padrão 'Preto'): ").strip()
    if cor == "":
        cor = None
    inserir_carro(cursor, chassi, modelo, cor)
    conn.commit()
    print("✅ Carro cadastrado com sucesso.")


def registrar_negociacao(cursor, conn):
    print("\n🧾 Registrar Negociação (Venda)")
    matricula = int(input("Matrícula do funcionário: ").strip())
    chassi = input("Chassi do carro: ").strip()
    cpf = int(input("CPF do cliente: ").strip())
    data = input("Data da negociação (YYYY-MM-DD): ").strip()
    valor = float(input("Valor total: ").replace(",", ".").strip())

    realizar_negociacao(cursor, matricula, chassi, cpf, data, valor)
    conn.commit()
    print("✅ Negociação registrada com sucesso.")


def listar_clientes(cursor):
    print("\n📋 Lista de Clientes:")
    cursor.execute("SELECT * FROM Cliente")
    linhas = cursor.fetchall()
    if not linhas:
        print("❌ Nenhum cliente cadastrado.")
        return
    for linha in linhas:
        print(linha)


def listar_funcionarios(cursor):
    print("\n📋 Lista de Funcionários:")
    cursor.execute("SELECT * FROM Funcionario")
    linhas = cursor.fetchall()
    if not linhas:
        print("❌ Nenhum funcionário cadastrado.")
        return
    for linha in linhas:
        print(linha)


def listar_carros(cursor):
    print("\n📋 Lista de Carros:")
    cursor.execute("SELECT * FROM Carro")
    linhas = cursor.fetchall()
    if not linhas:
        print("❌ Nenhum carro cadastrado.")
        return
    for linha in linhas:
        print(linha)


def listar_negociacoes(cursor):
    print("\n📋 Lista de Negociações:")
    cursor.execute("SELECT * FROM Negociacao")
    linhas = cursor.fetchall()
    if not linhas:
        print("❌ Nenhuma negociação cadastrada.")
        return
    for linha in linhas:
        print(linha)


def buscar_por_substring(cursor):
    print("\n🔎 Busca por substring")
    print("1 - Cliente (nome)")
    print("2 - Funcionário (nome)")
    print("3 - Carro (modelo)")
    opc = input("Escolha uma opção: ").strip()

    termo = input("Termo de busca: ").strip()
    if opc == "1":
        resultados = buscar_cliente_substring(cursor, termo)
    elif opc == "2":
        resultados = buscar_funcionario_substring(cursor, termo)
    elif opc == "3":
        resultados = buscar_carro_substring(cursor, termo)
    else:
        print("❌ Opção inválida.")
        return

    if not resultados:
        print("❌ Nenhum resultado encontrado.")
    else:
        print("✅ Resultados:")
        for linha in resultados:
            print(linha)


def atualizar_registros(cursor, conn):
    print("\n✏ Atualizar registros")
    print("1 - Cliente")
    print("2 - Funcionário")
    print("3 - Carro")
    opc = input("Escolha: ").strip()

    if opc == "1":
        cpf = int(input("CPF do cliente: ").strip())
        nome = input("Novo nome: ").strip()
        endereco = input("Novo endereço: ").strip()
        atualizar_cliente(cursor, cpf, nome, endereco)
        conn.commit()
        print("✅ Cliente atualizado.")
    elif opc == "2":
        matricula = int(input("Matrícula do funcionário: ").strip())
        nome = input("Novo nome: ").strip()
        salario = float(input("Novo salário: ").replace(",", ".").strip())
        atualizar_funcionario(cursor, matricula, nome, salario)
        conn.commit()
        print("✅ Funcionário atualizado.")
    elif opc == "3":
        chassi = input("Chassi do carro: ").strip()
        modelo = input("Novo modelo: ").strip()
        cor = input("Nova cor: ").strip()
        atualizar_carro(cursor, chassi, modelo, cor)
        conn.commit()
        print("✅ Carro atualizado.")
    else:
        print("❌ Opção inválida.")


def deletar_registros(cursor, conn):
    print("\n🗑 Remover registros")
    print("1 - Cliente")
    print("2 - Funcionário")
    print("3 - Carro")
    print("4 - Negociação")
    opc = input("Escolha: ").strip()

    if opc == "1":
        cpf = int(input("CPF do cliente: ").strip())
        deletar_cliente(cursor, cpf)
        conn.commit()
        print("✅ Cliente removido.")
    elif opc == "2":
        matricula = int(input("Matrícula do funcionário: ").strip())
        deletar_funcionario(cursor, matricula)
        conn.commit()
        print("✅ Funcionário removido.")
    elif opc == "3":
        chassi = input("Chassi do carro: ").strip()
        deletar_carro(cursor, chassi)
        conn.commit()
        print("✅ Carro removido.")
    elif opc == "4":
        id_neg = int(input("ID da negociação: ").strip())
        deletar_negociacao(cursor, id_neg)
        conn.commit()
        print("✅ Negociação removida.")
    else:
        print("❌ Opção inválida.")


def mostrar_relatorios(cursor):
    print("\n📊 Relatórios")
    print("1 - Negociações (JOIN vendedor + carro)")
    print("2 - Vendas por vendedor (GROUP BY + HAVING)")
    opc = input("Escolha: ").strip()

    if opc == "1":
        print("\n📊 Relatório de negociações:")
        rel = relatorio_avancado(cursor)
        if not rel:
            print("❌ Nenhuma negociação encontrada.")
        else:
            for linha in rel:
                print(linha)
    elif opc == "2":
        print("\n📈 Relatório de vendas por vendedor:")
        rel2 = relatorio_vendas_vendedor(cursor)
        if not rel2:
            print("❌ Nenhum dado encontrado.")
        else:
            for linha in rel2:
                print(linha)
    else:
        print("❌ Opção inválida.")


def main():
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute("PRAGMA foreign_keys = ON;")
    cursor = conexao.cursor()

    criar_tabelas(cursor)
    conexao.commit()
    print(f"✅ Tabelas criadas/verificadas em: {DB_PATH}")

    while True:
        print("\n=====================")
        print("  MENU PRINCIPAL  ")
        print("=====================")
        print("1 - Cadastrar Cliente")
        print("2 - Cadastrar Telefone")
        print("3 - Cadastrar Funcionário")
        print("4 - Cadastrar Carro")
        print("5 - Registrar Negociação")
        print("6 - Listar Clientes")
        print("7 - Listar Funcionários")
        print("8 - Listar Carros")
        print("9 - Listar Negociações")
        print("10 - Buscar por substring (nome/modelo)")
        print("11 - Atualizar registros")
        print("12 - Deletar registros")
        print("13 - Relatórios")
        print("0 - Sair")
        opc = input("Escolha uma opção: ").strip()

        if opc == "1":
            cadastrar_cliente(cursor, conexao)
        elif opc == "2":
            cadastrar_telefone(cursor, conexao)
        elif opc == "3":
            cadastrar_funcionario(cursor, conexao)
        elif opc == "4":
            cadastrar_carro(cursor, conexao)
        elif opc == "5":
            registrar_negociacao(cursor, conexao)
        elif opc == "6":
            listar_clientes(cursor)
        elif opc == "7":
            listar_funcionarios(cursor)
        elif opc == "8":
            listar_carros(cursor)
        elif opc == "9":
            listar_negociacoes(cursor)
        elif opc == "10":
            buscar_por_substring(cursor)
        elif opc == "11":
            atualizar_registros(cursor, conexao)
        elif opc == "12":
            deletar_registros(cursor, conexao)
        elif opc == "13":
            mostrar_relatorios(cursor)
        elif opc == "0":
            print("👋 Saindo...")
            break
        else:
            print("❌ Opção inválida, tente novamente.")

    conexao.close()
    print("✅ Conexão encerrada. Fim do programa.")


if __name__ == "__main__":
    main()
