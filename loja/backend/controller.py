# backend/controller.py
import os
import sqlite3
from django.conf import settings
# Certifique-se que o service é importado de forma relativa, se estiver na mesma pasta
from . import service 

DB_PATH = os.path.join(settings.BASE_DIR, "db.sqlite3")

def handle_request(action, entity=None, data=None):
    conn = sqlite3.connect(DB_PATH)
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
                {"id": r[0], "matricula": r[1], "chassi": r[2], "cpf": r[3], "data": r[4], "valor": r[5]} 
                for r in rows
            ]
        
        elif entidade == "telefone":
             rows = service.listar_todos_telefones(cursor)
             registros = [{"numero": r[0], "cpf": r[1]} for r in rows]

        return registros

    try:
        # 1) INICIALIZAÇÃO
        if action == "init_db":
            service.criar_tabelas(cursor)
            response = {"message": "Tabelas e triggers criados!"}

        # 2) CREATE
        elif action == "add":
            if entity == "cliente":
                service.inserir_cliente(cursor, get_val("cpf"), get_val("nome"), get_val("endereco"))
            elif entity == "telefone":
                service.inserir_telefone(cursor, get_val("numero"), get_val("cpf"))
            elif entity == "funcionario":
                service.inserir_funcionario(cursor, get_val("matricula"), get_val("nome"), get_val("salario"))
            elif entity == "gerente":
                service.inserir_gerente(cursor, get_val("matricula"), get_val("vale_alimentacao"))
                entity = "funcionario" # Truque para atualizar a lista de funcionarios
            elif entity == "vendedor":
                service.inserir_vendedor(cursor, get_val("matricula"), get_val("vale_transporte"))
                entity = "funcionario" 
            elif entity == "carro":
                service.inserir_carro(cursor, get_val("chassi"), get_val("modelo"), get_val("cor"))
            elif entity == "negociacao":
                service.realizar_negociacao(cursor, get_val("matricula"), get_val("chassi"), get_val("cpf"), get_val("data"), get_val("valor"))

            # AQUI ESTÁ A MÁGICA: Retornamos mensagem E os dados atualizados
            response = {
                "message": f"{entity.upper()} inserido com sucesso!",
                "data": obter_dados_atualizados(entity)
            }

        # 3) SEARCH (Busca por ID)
        elif action == "search":
            pk = get_val("id")
            row = None
            lista_retorno = []

            if entity == "cliente":
                row = service.buscar_cliente(cursor, pk)
                if row: lista_retorno = [{"cpf": row[0], "nome": row[1], "endereco": row[2]}]
            elif entity == "funcionario":
                row = service.buscar_funcionario(cursor, pk)
                if row: lista_retorno = [{"matricula": row[0], "nome": row[1], "salario": row[2]}]
            elif entity == "carro":
                row = service.buscar_carro(cursor, pk)
                if row: lista_retorno = [{"chassi": row[0], "modelo": row[1], "cor": row[2]}]
            elif entity == "negociacao":
                row = service.buscar_negociacao(cursor, pk)
                if row: lista_retorno = [{"id": row[0], "matricula": row[1], "chassi": row[2], "cpf": row[3], "data": row[4], "valor": row[5]}]
            elif entity == "telefone":
                row = service.buscar_telefone(cursor, pk)
                if row: lista_retorno = [{"numero": row[0], "cpf": row[1]}]

            if not row:
                response = {"message": "Nenhum registro encontrado.", "data": []}
            else:
                # Retornamos uma lista mesmo sendo 1 item, para o front usar a mesma lógica de tabela
                response = {"data": lista_retorno}

        # 4) UPDATE
        elif action == "update":
            if entity == "cliente":
                service.atualizar_cliente(cursor, get_val("cpf"), get_val("nome"), get_val("endereco"))
            elif entity == "funcionario":
                service.atualizar_funcionario(cursor, get_val("matricula"), get_val("nome"), get_val("salario"))
            elif entity == "carro":
                service.atualizar_carro(cursor, get_val("chassi"), get_val("modelo"), get_val("cor"))
            elif entity == "vendedor":
                service.atualizar_vendedor(cursor, get_val("matricula"), get_val("vale_transporte"))
                entity = "funcionario"
            elif entity == "gerente":
                service.atualizar_gerente(cursor, get_val("matricula"), get_val("vale_alimentacao"))
                entity = "funcionario"
            
            response = {
                "message": f"{entity.upper()} atualizado!",
                "data": obter_dados_atualizados(entity)
            }

        # 5) DELETE
        elif action == "remove":
            id_value = get_val("id")   # <-- pega o valor correto enviado pelo React

            if entity == "cliente":
                service.deletar_cliente(cursor, id_value)
            elif entity == "funcionario":
                service.deletar_funcionario(cursor, id_value)
            elif entity == "carro":
                service.deletar_carro(cursor, id_value)
            elif entity == "negociacao":
                service.deletar_negociacao(cursor, id_value)
            elif entity == "telefone":
                service.deletar_telefone(cursor, get_val("cpf"), get_val("numero"))

            response = {
                "message": f"{entity.upper()} removido!",
                "data": obter_dados_atualizados(entity)
            }
        elif action == "quantifiers":
            qtype = get_val("type")  # vem do front: "ANY" ou "ALL"

            if not qtype:
                response = {"error": "Escolha o tipo: ANY ou ALL."}
            else:
                qtype = qtype.upper()

                if qtype == "ANY":
                    rows = service.consulta_quantificador_any(cursor)
                elif qtype == "ALL":
                    rows = service.consulta_quantificador_all(cursor)
                else:
                    response = {"error": f"Tipo inválido '{qtype}'. Use ANY ou ALL."}
                    return response

                # Monta o JSON de resposta
                response = {
                    "data": [
                        {"nome_funcionario": r[0], "venda_valor": r[1]}
                        for r in rows
                    ]
                }

        # 6) MASS LOAD
        elif action == "mass":
            if entity == "cliente":
                service.carga_clientes_em_massa(cursor, data.get('clientes', []))
            elif entity == "carro":            
                service.carga_carros_em_massa(cursor, data.get('carros', []))
            elif entity == "funcionario":
                service.carga_funcionarios_em_massa(cursor, data.get('funcionarios', []))
            elif entity == "negociacao":
                service.carga_negociacoes_em_massa(cursor, data.get('negociacoes', []))
            
            response = {
                "message": "Carga em massa executada!",
                "data": obter_dados_atualizados(entity)
            }

        # 7) SUBSTRING
        elif action == "substring":
            termo = get_val("termo")
            rows = []
            if not termo:
                response = {"error": "Digite um termo."}
            else:
                if entity == "carro":
                    rows = service.buscar_carro_substring(cursor, termo)
                    response = {"data": [{"chassi": r[0], "modelo": r[1], "cor": r[2]} for r in rows]}
                elif entity == "cliente":
                    rows = service.buscar_cliente_substring(cursor, termo)
                    response = {"data": [{"cpf": r[0], "nome": r[1], "endereco": r[2]} for r in rows]}
                elif entity == "funcionario":
                    rows = service.buscar_funcionario_substring(cursor, termo)
                    response = {"data": [{"matricula": r[0], "nome": r[1], "salario": r[2]} for r in rows]}
                else:
                    response = {"error": "Entidade inválida para substring"}

        # 8, 9, 10) RELATÓRIOS (Advanced, Quantifiers, Grouping)
        elif action == "advanced":
            rows = service.relatorio_avancado(cursor)
            response = {"data": [{"vendedor": r[0], "modelo": r[1], "valor": r[2]} for r in rows]}
              
        elif action == "grouping":
            tipo = get_val("tipo")
            if tipo == "modelo":
                rows = service.relatorio_media_vendas_por_modelo(cursor)
                response = {"data": [{"modelo": r[0], "qtd_vendas": r[1], "media_valor": r[2]} for r in rows]}
            else:
                rows = service.relatorio_vendas_vendedor(cursor)
                response = {"data": [{"vendedor": r[0], "qtd_vendas": r[1], "total_faturado": r[2]} for r in rows]}

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