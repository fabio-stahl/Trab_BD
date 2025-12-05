from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .controller import handle_request

@csrf_exempt  # depois podemos tratar CSRF de forma mais fina
def api_execute(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido. Use POST.'}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)

    action = body.get('action')
    entity = body.get('entity')
    data = body.get('data', {})

    if not action:
        return JsonResponse({'error': 'Campo "action" é obrigatório.'}, status=400)
    
    # delega tudo para o seu controller
    resp = handle_request(action=action, entity=entity, data=data)

    # aqui você já tem um dicionário pronto para virar JSON
    return JsonResponse(resp, safe=not isinstance(resp, list), status=200)




