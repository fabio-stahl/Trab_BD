# backend/controller.py
import os
import sqlite3
from django.conf import settings
from . import service 
import subprocess
import sys
from pathlib import Path

DB_PATH = os.path.join(settings.BASE_DIR, "db.sqlite3")


def handle_request(action, entity=None, data=None):
    conn = sqlite3.connect(DB_PATH)
    # Garantir integridade referencial
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    response = {}

    def get_val(field):
        return data.get(field) if data else None

    # --- FUNÇÃO AUXILIAR PARA RETORNAR DADOS ATUALIZADOS ---
    def obter_dados_atualizados(entidade):
        """Busca todos os registros da entidade para atualizar a tabela no front"""
        registros = []

        if entidade == "cliente":
            rows = service.listar_todos_clientes(cursor)
            registros = [{"cpf": r[0], "nome": r[1], "endereco": r[2]} for r in rows]

        elif entidade == "funcionario":
            rows = service.listar_todos_funcionarios(cursor)
            registros = [{"matricula": r[0], "nome": r[1], "salario": r[2]} for r in rows]

        elif entidade == "carro":
            rows = service.listar_todos_carros(cursor)
            registros = [{"chassi": r[0], "modelo": r[1], "cor": r[2]} for r in rows]

        elif entidade == "negociacao":
            rows = service.listar_todas_negociacoes(cursor)
            registros = [
                {
                    "id": r[0],
                    "matricula": r[1],
                    "chassi": r[2],
                    "cpf": r[3],
                    "data": r[4],
                    "valor": r[5],
                }
                for r in rows
            ]

        elif entidade == "telefone":
            rows = service.listar_todos_telefones(cursor)
            registros = [{"numero": r[0], "cpf": r[1]} for r in rows]

        return registros

    try:
        # 1) INICIALIZAÇÃO
        if action == "init_db":
            reset_path = Path(__file__).resolve().parent.parent / "reset.py"
            subprocess.run([sys.executable, str(reset_path)], check=True)
            reset_path = Path(__file__).resolve().parent.parent / "reset.py"
            subprocess.run([sys.executable, str(reset_path)], check=True)
            service.criar_tabelas(cursor)
            response = {"message": "Tabelas e triggers criados!"}

        # 2) CREATE
        elif action == "add":
            if entity == "cliente":
                service.inserir_cliente(
                    cursor,
                    get_val("cpf"),
                    get_val("nome"),
                    get_val("endereco"),
                )

            elif entity == "telefone":
                service.inserir_telefone(cursor, get_val("numero"), get_val("cpf"))

            elif entity == "funcionario":
                service.inserir_funcionario(
                    cursor,
                    get_val("matricula"),
                    get_val("nome"),
                    get_val("salario"),
                )

            elif entity == "gerente":
                service.inserir_gerente(
                    cursor,
                    get_val("matricula"),
                    get_val("vale_alimentacao"),
                )
                # Truque: atualiza grid de funcionários
                entity = "funcionario"

            elif entity == "vendedor":
                service.inserir_vendedor(
                    cursor,
                    get_val("matricula"),
                    get_val("vale_transporte"),
                )
                entity = "funcionario"

            elif entity == "carro":
                service.inserir_carro(
                    cursor,
                    get_val("chassi"),
                    get_val("modelo"),
                    get_val("cor"),
                )

            elif entity == "negociacao":
                service.realizar_negociacao(
                    cursor,
                    get_val("matricula"),
                    get_val("chassi"),
                    get_val("cpf"),
                    get_val("data"),
                    get_val("valor"),
                )

            response = {
                "message": f"{entity.upper()} inserido com sucesso!",
                "data": obter_dados_atualizados(entity),
            }

        # 3) SEARCH (Busca por ID)
        elif action == "search":
            pk = get_val("id")
            row = None
            lista_retorno = []

            if entity == "cliente":
                row = service.buscar_cliente(cursor, pk)
                if row:
                    lista_retorno = [
                        {"cpf": row[0], "nome": row[1], "endereco": row[2]}
                    ]

            elif entity == "funcionario":
                row = service.buscar_funcionario(cursor, pk)
                if row:
                    lista_retorno = [
                        {"matricula": row[0], "nome": row[1], "salario": row[2]}
                    ]

            elif entity == "carro":
                row = service.buscar_carro(cursor, pk)
                if row:
                    lista_retorno = [
                        {"chassi": row[0], "modelo": row[1], "cor": row[2]}
                    ]

            elif entity == "negociacao":
                row = service.buscar_negociacao(cursor, pk)
                if row:
                    lista_retorno = [
                        {
                            "id": row[0],
                            "matricula": row[1],
                            "chassi": row[2],
                            "cpf": row[3],
                            "data": row[4],
                            "valor": row[5],
                        }
                    ]

            elif entity == "telefone":
                row = service.buscar_telefone(cursor, pk)
                if row:
                    lista_retorno = [{"numero": row[0], "cpf": row[1]}]

            if not row:
                response = {"message": "Nenhum registro encontrado.", "data": []}
            else:
                response = {"data": lista_retorno}

        # 4) UPDATE
        elif action == "update":
            linhas_afetadas = 0  # <<< chave do controle

            if entity == "cliente":
                service.atualizar_cliente(
                    cursor,
                    get_val("cpf"),
                    get_val("nome"),
                    get_val("endereco"),
                )
                linhas_afetadas = cursor.rowcount

            elif entity == "funcionario":
                service.atualizar_funcionario(
                    cursor,
                    get_val("matricula"),
                    get_val("nome"),
                    get_val("salario"),
                )
                linhas_afetadas = cursor.rowcount

            elif entity == "carro":
                service.atualizar_carro(
                    cursor,
                    get_val("chassi"),
                    get_val("modelo"),
                    get_val("cor"),
                )
                linhas_afetadas = cursor.rowcount

            elif entity == "vendedor":
                service.atualizar_vendedor(
                    cursor,
                    get_val("matricula"),
                    get_val("vale_transporte"),
                )
                linhas_afetadas = cursor.rowcount
                entity = "funcionario"

            elif entity == "gerente":
                service.atualizar_gerente(
                    cursor,
                    get_val("matricula"),
                    get_val("vale_alimentacao"),
                )
                linhas_afetadas = cursor.rowcount
                entity = "funcionario"

            elif entity == "negociacao":
                # Se você tiver tela de update de negociação,
                # aqui você chamaria service.atualizar_negociacao(...)
                service.atualizar_negociacao(
                    cursor,
                    get_val("id"),
                    get_val("matricula"),
                    get_val("chassi"),
                    get_val("cpf"),
                    get_val("data"),
                    get_val("valor"),
                )
                linhas_afetadas = cursor.rowcount

            # Decisão da mensagem com base em linhas_afetadas
            if linhas_afetadas == 0:
                response = {
                    "message": f"Nenhum registro de {entity} encontrado para atualizar.",
                    "data": [],
                }
            else:
                response = {
                    "message": f"{entity.upper()} atualizado!",
                    "data": obter_dados_atualizados(entity),
                }

        # 5) DELETE
        elif action == "remove":
            id_value = get_val("id")
            linhas_afetadas = 0  # <<< chave do controle

            if entity == "cliente":
                service.deletar_cliente(cursor, id_value)
                linhas_afetadas = cursor.rowcount

            elif entity == "funcionario":
                service.deletar_funcionario(cursor, id_value)
                linhas_afetadas = cursor.rowcount

            elif entity == "carro":
                service.deletar_carro(cursor, id_value)
                linhas_afetadas = cursor.rowcount

            elif entity == "negociacao":
                service.deletar_negociacao(cursor, id_value)
                linhas_afetadas = cursor.rowcount

            elif entity == "telefone":
                # Aqui depende de como você quer identificar telefone.
                # Mantive a lógica antiga, mas agora respeitando rowcount.
                service.deletar_telefone(cursor, get_val("cpf"), get_val("numero"))
                linhas_afetadas = cursor.rowcount

            if linhas_afetadas == 0:
                response = {
                    "message": f"Nenhum registro de {entity} encontrado para remover.",
                    "data": obter_dados_atualizados(entity),
                }
            else:
                response = {
                    "message": f"{entity.upper()} removido!",
                    "data": obter_dados_atualizados(entity),
                }

        # 6) MASS LOAD
        elif action == "mass":
            if entity == "cliente":
                service.carga_clientes_em_massa(cursor, data.get("clientes", []))

            elif entity == "carro":
                service.carga_carros_em_massa(cursor, data.get("carros", []))

            elif entity == "funcionario":
                service.carga_funcionarios_em_massa(
                    cursor,
                    data.get("funcionarios", []),
                )

            elif entity == "negociacao":
                service.carga_negociacoes_em_massa(
                    cursor,
                    data.get("negociacoes", []),
                )

            response = {
                "message": "Carga em massa executada!",
                "data": obter_dados_atualizados(entity),
            }

        # 7) SUBSTRING
        elif action == "substring":
            termo = get_val("termo")
            if not termo:
                response = {"error": "Digite um termo."}
            else:
                if entity == "carro":
                    rows = service.buscar_carro_substring(cursor, termo)
                    response = {
                        "data": [
                            {"chassi": r[0], "modelo": r[1], "cor": r[2]} for r in rows
                        ]
                    }

                elif entity == "cliente":
                    rows = service.buscar_cliente_substring(cursor, termo)
                    response = {
                        "data": [
                            {"cpf": r[0], "nome": r[1], "endereco": r[2]} for r in rows
                        ]
                    }

                elif entity == "funcionario":
                    rows = service.buscar_funcionario_substring(cursor, termo)
                    response = {
                        "data": [
                            {"matricula": r[0], "nome": r[1], "salario": r[2]}
                            for r in rows
                        ]
                    }

                else:
                    response = {"error": "Entidade inválida para substring"}

        # 8) RELATÓRIO AVANÇADO (JOINS)
        elif action == "advanced":
            report_type = get_val("report_type")
            rows = []
            response_data = []

            if report_type == "inner":
                rows = service.relatorio_inner_join(cursor)
                response_data = [
                    {"id_venda": r[0], "vendedor": r[1], "valor": r[2]} 
                    for r in rows
                ]
            elif report_type == "left":
                rows = service.relatorio_left_join(cursor)
                response_data = [
                    {"funcionario": r[0], "id_venda": (r[1] or "-"), "valor": (r[2] or 0)} 
                    for r in rows
                ]
            elif report_type == "right":
                rows = service.relatorio_right_join_simulado(cursor)
                response_data = [
                    {"modelo": r[0], "cor": r[1], "data_venda": (r[2] or "-"), "status": r[3]} 
                    for r in rows
                ]
            else:
                rows = service.relatorio_inner_join(cursor)
                response_data = [{"id": r[0], "vendedor": r[1], "valor": r[2]} for r in rows]
            response = {"data": response_data}

        elif action == "quantifiers":
            type_quantifier = get_val("quantifier_type")
            if type_quantifier == "any" : 
                rows = service.consulta_quantificador_any(cursor)
                response = {"data": [{"nome_funcionario": r[0], "venda_valor": r[1]} for r in rows]} 
            elif type_quantifier == "all" :
                rows = service.consulta_quantificador_all(cursor)        
                response = {"data": [{"nome_funcionario": r[0], "venda_valor": r[1]} for r in rows]}

        elif action == "grouping":
            tipo = get_val("tipo")

            if tipo == "modelo":
                rows = service.relatorio_media_vendas_por_modelo(cursor)
                response = {
                    "data": [
                        {
                            "modelo": r[0],
                            "qtd_vendas": r[1],
                            "media_valor": r[2],
                        }
                        for r in rows
                    ]
                }

            elif tipo == "vendedor":
                rows = service.relatorio_vendas_vendedor(cursor)
                response = {
                    "data": [
                        {
                            "vendedor": r[0],
                            "qtd_vendas": r[1],
                            "total_faturado": r[2],
                        }
                        for r in rows
                    ]
                }

            elif tipo == "cor":
                rows = service.relatorio_vendas_por_cor(cursor)
                response = {
                    "data": [
                        {
                            "cor": r[0],
                            "qtd_vendas": r[1],
                            "total_faturado": r[2],
                        }
                        for r in rows
                    ]
                }

            elif tipo == "cliente":
                rows = service.relatorio_vendas_por_cliente(cursor)
                response = {
                    "data": [
                        {
                            "cliente": r[0],
                            "qtd_vendas": r[1],
                            "total_faturado": r[2],
                        }
                        for r in rows
                    ]
                }

            elif tipo == "funcionario":
                rows = service.relatorio_vendas_por_funcionario(cursor)
                response = {
                    "data": [
                        {
                            "funcionario": r[0],
                            "qtd_vendas": r[1],
                            "total_faturado": r[2],
                        }
                        for r in rows
                    ]
                }

            elif tipo == "data":
                rows = service.relatorio_vendas_por_data(cursor)
                response = {
                    "data": [
                        {
                            "data": r[0],
                            "qtd_vendas": r[1],
                            "total_faturado": r[2],
                        }
                        for r in rows
                    ]
                }

            else:
                response = {"error": "Tipo de agrupamento inválido."}

        elif action == "grouping_having":
            minimo_raw = get_val("minimo")
            try:
                minimo = float(minimo_raw) if minimo_raw not in (None, "") else 0.0
            except ValueError:
                minimo = 0.0

            rows = service.relatorio_vendas_vendedor_minimo(cursor, minimo)
            response = {
                "data": [
                    {
                        "vendedor": r[0],
                        "qtd_vendas": r[1],
                        "total_faturado": r[2],
                    }
                    for r in rows
                ]
            }

        elif action == "ordering":
            tipo = get_val("tipo") or "modelo"
            ordem = (get_val("ordem") or "DESC").upper()

            rows = service.relatorio_ordenado(cursor, tipo, ordem)

            if tipo == "modelo":
                response = {
                    "data": [
                        {
                            "modelo": r[0],
                            "qtd_vendas": r[1],
                            "media_valor": r[2],
                        }
                        for r in rows
                    ]
                }
            else:
                response = {
                    "data": [
                        {
                            "vendedor": r[0],
                            "qtd_vendas": r[1],
                            "total_faturado": r[2],
                        }
                        for r in rows
                    ]
                }

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
