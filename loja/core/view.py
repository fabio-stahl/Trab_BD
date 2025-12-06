# core/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backend.controller import handle_request # Importação ajustada para backend.controller

@csrf_exempt 
def api_handler(request):
    """
    View responsável por receber as requisições POST da API 
    e delegar a lógica ao Controller.
    """
    if request.method != 'POST':
        # Definindo endpoints mais claros para API (ex: /api/v1/...) é melhor,
        # mas por enquanto, manteremos o POST para a rota 'execute'.
        return JsonResponse({'error': 'Método não permitido. Use POST.'}, status=405)

    try:
        # Tenta decodificar o corpo do request (JSON)
        body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)

    action = body.get('action')
    entity = body.get('entity')
    data = body.get('data', {})

    if not action:
        return JsonResponse({'error': 'Campo "action" é obrigatório.'}, status=400)
    
    # Delega a requisição para o seu Controller de Negócio
    resp = handle_request(action=action, entity=entity, data=data)

    # Retorna a resposta (JSON) do Controller ao Frontend
    # safe=False permite que listas (arrays) sejam retornadas como JSON de nível superior
    return JsonResponse(resp, safe=not isinstance(resp, list), status=200)