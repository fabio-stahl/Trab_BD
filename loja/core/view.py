from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
import json
from backend import controller


def index(request):
    """Renderiza a página única do Frontend"""
    return render(request, 'index.html')


@csrf_exempt
def api_handler(request):
    """
    View ÚNICA que gerencia todas as requisições.
    Ela atua como uma ponte entre o JS (JSON) e o Controller (Python).
    """
    if request.method == 'POST':
        try:
            # 1. Converte o corpo da requisição de Bytes para Dicionário Python
            body = json.loads(request.body)
            
            # 2. Extrai os parâmetros enviados pelo main.js
            action = body.get('action')  # ex: 'add', 'remove', 'init_db'
            entity = body.get('entity')  # ex: 'cliente', 'carro'
            data = body.get('data')      # ex: {'nome': 'João', 'cpf': 123}

            # 3. Passa a responsabilidade para o Controller
            # O controller vai abrir o banco, executar e fechar.
            response_data = controller.handle_request(action, entity, data)

            # 4. Retorna a resposta do controller para o navegador
            # safe=False permite retornar listas se necessário
            return JsonResponse(response_data, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
        except Exception as e:
            # Captura qualquer erro inesperado e avisa o frontend
            print(f"ERRO NO SERVIDOR: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)
