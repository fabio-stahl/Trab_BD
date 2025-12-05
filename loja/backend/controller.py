import sqlite3
from . import service

DB_PATH = 'db.sqlite3'

def handle_request(action, entity=None, data=None):
    """
    Controlador central. Recebe a ação da View, conecta no banco
    e delega para o Service.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    response_data = {}

    # Helper para extrair dados seguros do dicionário 'data'
    def get_val(key):
        return data.get(key) if data else None

    try:
        # --- 1. INICIALIZAÇÃO ---
        if action == 'init_db':
            service.criar_tabelas(cursor)
            response_data = {'message': 'Tabelas e Triggers criados com sucesso!'}

        # --- 2. CREATE (Adicionar Dados) ---
        elif action == 'add':
            if entity == 'cliente':
                service.inserir_cliente(cursor, get_val('cpf'), get_val('nome'), get_val('endereco'))
            
            elif entity == 'telefone':
                service.inserir_telefone(cursor, get_val('numero'), get_val('cpf'))
            
            elif entity == 'funcionario':
                service.inserir_funcionario(cursor, get_val('matricula'), get_val('nome'), get_val('salario'))
            
            elif entity == 'gerente':
                # Nota: Assumindo que o Funcionario já existe ou lógica em trigger
                service.inserir_gerente(cursor, get_val('matricula'), get_val('vale_alimentacao'))
            
            elif entity == 'vendedor':
                service.inserir_vendedor(cursor, get_val('matricula'), get_val('vale_transporte'))
            
            elif entity == 'carro':
                service.inserir_carro(cursor, get_val('chassi'), get_val('modelo'), get_val('cor'))
            
            elif entity == 'negociacao':
                service.realizar_negociacao(cursor, get_val('matricula'), get_val('chassi'), 
                                          get_val('cpf'), get_val('data'), get_val('valor'))
            
            response_data = {'message': f'Registro adicionado em {entity.upper()} com sucesso!'}

        # --- 3. READ (Pesquisar/Listar por ID) ---
        elif action == 'search':
            row = None
            pk = get_val('id') # O frontend envia o ID/Chave neste campo genérico

            if entity == 'cliente':
                row = service.buscar_cliente(cursor, pk)
                if row: response_data = {'cpf': row[0], 'nome': row[1], 'endereco': row[2]}
            
            elif entity == 'telefone':
                row = service.buscar_telefone(cursor, pk)
                if row: response_data = {'numero': row[0], 'cpf_dono': row[1]}
            
            elif entity == 'funcionario':
                row = service.buscar_funcionario(cursor, pk)
                if row: response_data = {'matricula': row[0], 'nome': row[1], 'salario': row[2]}

            elif entity == 'carro':
                row = service.buscar_carro(cursor, pk)
                if row: response_data = {'chassi': row[0], 'modelo': row[1], 'cor': row[2]}

            elif entity == 'negociacao':
                row = service.buscar_negociacao(cursor, pk)
                if row: response_data = {'id': row[0], 'matricula': row[1], 'chassi': row[2], 
                                       'cpf': row[3], 'data': row[4], 'valor': row[5]}

            if not row and not response_data:
                response_data = {'message': 'Nenhum registro encontrado com essa chave.'}

        # --- 4. UPDATE (Atualizar Dados) ---
        elif action == 'update':
            # Assume-se que 'id' é a chave para buscar e os outros campos são os novos valores
            pk = get_val('id')
            
            if entity == 'cliente':
                service.atualizar_cliente(cursor, pk, get_val('nome'), get_val('endereco'))
            
            elif entity == 'funcionario':
                service.atualizar_funcionario(cursor, pk, get_val('nome'), get_val('salario'))
            
            elif entity == 'carro':
                service.atualizar_carro(cursor, pk, get_val('modelo'), get_val('cor'))

            response_data = {'message': f'Registro {pk} em {entity} atualizado!'}

        # --- 5. DELETE (Remover Dados) ---
        elif action == 'remove':
            pk = get_val('id')

            if entity == 'cliente':
                service.deletar_cliente(cursor, pk)
            elif entity == 'funcionario':
                service.deletar_funcionario(cursor, pk)
            elif entity == 'carro':
                service.deletar_carro(cursor, pk)
            elif entity == 'negociacao':
                service.deletar_negociacao(cursor, pk)
            
            response_data = {'message': f'Registro {pk} removido de {entity}.'}

        # --- 6. OPERAÇÕES ESPECIAIS (Requisitos do PDF) ---
        
        elif action == 'mass':
            # Chama função que insere lista de objetos
            service.carga_em_massa(cursor)
            response_data = {'message': 'Carga em massa (Dummy Data) realizada!'}

        elif action == 'substring':
            # Busca substring (Case Insensitive)
            rows = service.buscar_carro_substring(cursor, get_val('termo'))
            response_data = [{'chassi': r[0], 'modelo': r[1], 'cor': r[2]} for r in rows]

        elif action == 'advanced':
            # Consulta com JOINs diferentes
            rows = service.relatorio_avancado(cursor)
            # Exemplo de retorno: Nome Funcionario, Modelo Carro, Valor
            response_data = [{'vendedor': r[0], 'modelo': r[1], 'valor': r[2]} for r in rows]

        elif action == 'quantifiers':
            # Consulta com ANY / ALL (Subconsulta correlacionada)
            rows = service.consulta_quantificador_any(cursor)
            response_data = [{'nome_funcionario': r[0]} for r in rows]

        elif action == 'grouping':
            # Group By, Having, Ordenação
            rows = service.relatorio_vendas_vendedor(cursor)
            response_data = [{'vendedor': r[0], 'qtd_vendas': r[1], 'total_faturado': r[2]} for r in rows]

        # Finaliza transação
        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()
        # Retorna erro amigável do SQLite (ex: constraints)
        response_data = {'error': f"Erro de Banco: {e}"}
    except Exception as e:
        conn.rollback()
        response_data = {'error': f"Erro Interno: {str(e)}"}
    finally:
        conn.close()
    
    return response_data
