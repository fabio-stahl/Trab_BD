# core/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backend.controller import handle_request 

@csrf_exempt 
def api_handler(request):

    if request.method != 'POST':
        
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
    
    resp = handle_request(action=action, entity=entity, data=data)

    return JsonResponse(resp, safe=not isinstance(resp, list), status=200)