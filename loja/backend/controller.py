import os
import sqlite3
from django.conf import settings
from . import service

DB_PATH = os.path.join(settings.BASE_DIR, "db.sqlite3")


def handle_request(action, entity=None, data=None):
    """
    Controlador principal que recebe a ação da View/API e chama o Service.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    response = {}

    def get_val(field):
        return data.get(field) if data else None

    try:
        # -----------------------------------------
        # 1) INICIALIZAÇÃO DO BANCO
        # -----------------------------------------
        if action == "init_db":
            service.criar_tabelas(cursor)
            response = {"message": "Tabelas e triggers criados!"}

        # -----------------------------------------
        # 2) CREATE
        # -----------------------------------------
        elif action == "add":
            if entity == "cliente":
                service.inserir_cliente(cursor, get_val("cpf"), get_val("nome"), get_val("endereco"))

            elif entity == "telefone":
                service.inserir_telefone(cursor, get_val("numero"), get_val("cpf"))

            elif entity == "funcionario":
                service.inserir_funcionario(cursor, get_val("matricula"), get_val("nome"), get_val("salario"))

            elif entity == "gerente":
                service.inserir_gerente(cursor, get_val("matricula"), get_val("vale_alimentacao"))

            elif entity == "vendedor":
                service.inserir_vendedor(cursor, get_val("matricula"), get_val("vale_transporte"))

            elif entity == "carro":
                service.inserir_carro(cursor, get_val("chassi"), get_val("modelo"), get_val("cor"))

            elif entity == "negociacao":
                service.realizar_negociacao(
                    cursor,
                    get_val("matricula"),
                    get_val("chassi"),
                    get_val("cpf"),
                    get_val("data"),
                    get_val("valor")
                )

            response = {"message": f"{entity.upper()} inserido com sucesso!"}

        # -----------------------------------------
        # 3) SEARCH
        # -----------------------------------------
        elif action == "search":
            pk = get_val("id")
            row = None

            if entity == "cliente":
                row = service.buscar_cliente(cursor, pk)
                if row: response = {"cpf": row[0], "nome": row[1], "endereco": row[2]}

            elif entity == "telefone":
                row = service.buscar_telefone(cursor, pk)
                if row: response = {"numero": row[0], "cpf": row[1]}

            elif entity == "funcionario":
                row = service.buscar_funcionario(cursor, pk)
                if row: response = {"matricula": row[0], "nome": row[1], "salario": row[2]}

            elif entity == "carro":
                row = service.buscar_carro(cursor, pk)
                if row: response = {"chassi": row[0], "modelo": row[1], "cor": row[2]}

            elif entity == "negociacao":
                row = service.buscar_negociacao(cursor, pk)
                if row:
                    response = {
                        "id": row[0],
                        "matricula": row[1],
                        "chassi": row[2],
                        "cpf": row[3],
                        "data": row[4],
                        "valor": row[5]
                    }

            if not row:
                response = {"message": "Nenhum registro encontrado."}

        # -----------------------------------------
        # 4) UPDATE
        # -----------------------------------------
        elif action == "update":
            pk = get_val("id")

            if entity == "cliente":
                service.atualizar_cliente(cursor, pk, get_val("nome"), get_val("endereco"))

            elif entity == "funcionario":
                service.atualizar_funcionario(cursor, pk, get_val("nome"), get_val("salario"))

            elif entity == "carro":
                service.atualizar_carro(cursor, pk, get_val("modelo"), get_val("cor"))

            response = {"message": f"{entity.upper()} atualizado!"}

        # -----------------------------------------
        # 5) DELETE
        # -----------------------------------------
        elif action == "remove":
            pk = get_val("id")

            if entity == "cliente":
                service.deletar_cliente(cursor, pk)

            elif entity == "funcionario":
                service.deletar_funcionario(cursor, pk)

            elif entity == "carro":
                service.deletar_carro(cursor, pk)

            elif entity == "negociacao":
                service.deletar_negociacao(cursor, pk)

            response = {"message": f"{entity.upper()} removido!"}

        # -----------------------------------------
        # 6) MASS LOAD
        # -----------------------------------------
        elif action == "mass":
            # 🔥 ajustado para bater com SEU service.py
            service.carga_clientes_em_massa(cursor, [
                (111, "Carlos", "Rua A"),
                (222, "Marcos", "Rua B"),
                (333, "Júlia", "Rua C"),
            ])

            service.carga_carros_em_massa(cursor, [
                ("X1", "Onix", "Branco"),
                ("X2", "Civic", "Preto"),
                ("X3", "Corolla", "Cinza"),
            ])

            service.carga_funcionarios_em_massa(cursor, [
                (1, "Pedro", 3500),
                (2, "Ana", 4200),
                (3, "Fernando", 5000),
            ])

            response = {"message": "Carga em massa executada com sucesso!"}

        # -----------------------------------------
        # 7) SUBSTRING (LIKE)
        # -----------------------------------------
        elif action == "substring":
            termo = get_val("termo")

            if not termo:
                response = {"error": "Digite um termo para buscar."}

            elif entity == "carro":
                rows = service.buscar_carro_substring(cursor, termo)
                response = [{"chassi": r[0], "modelo": r[1], "cor": r[2]} for r in rows]

            elif entity == "cliente":
                rows = service.buscar_cliente_substring(cursor, termo)
                response = [{"cpf": r[0], "nome": r[1], "endereco": r[2]} for r in rows]

            elif entity == "funcionario":
                rows = service.buscar_funcionario_substring(cursor, termo)
                response = [{"matricula": r[0], "nome": r[1], "salario": r[2]} for r in rows]

            else:
                response = {"error": f"Substring não implementado para {entity}"}

        # -----------------------------------------
        # 8) RELATÓRIO AVANÇADO (JOIN)
        # -----------------------------------------
        elif action == "advanced":
            rows = service.relatorio_avancado(cursor)
            response = [
                {"vendedor": r[0], "modelo": r[1], "valor": r[2]}
                for r in rows
            ]

        # -----------------------------------------
        # 9) QUANTIFICADORES (ANY/ALL)
        # -----------------------------------------
        elif action == "quantifiers":
            rows = service.consulta_quantificador_any(cursor)
            response = [{"nome_funcionario": r[0]} for r in rows]

        # -----------------------------------------
        # 10) GROUP BY / HAVING
        # -----------------------------------------
        elif action == "grouping":
            rows = service.relatorio_vendas_vendedor(cursor)
            response = [
                {"vendedor": r[0], "qtd_vendas": r[1], "total_faturado": r[2]}
                for r in rows
            ]

        else:
            response = {"error": f"Ação desconhecida: {action}"}

        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()
        response = {"error": f"Erro de banco: {str(e)}"}

    except Exception as e:
        conn.rollback()
        response = {"error": f"Erro interno: {str(e)}"}

    finally:
        conn.close()

    return response
