from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telebot.types import Update
from .bot import bot, TOKEN


@csrf_exempt
def web_hook(request, token):
    if token == TOKEN:
        if request.headers.get('content-type') == 'application/json':
            json_string = request.body.decode('utf-8')
            update = Update.de_json(json_string)
            bot.process_new_updates([update])
            return JsonResponse({'ok': True})
        else:
            return JsonResponse({'ok': False})
    else:
        return JsonResponse({'ok': False, 'description': "It is not working"})
