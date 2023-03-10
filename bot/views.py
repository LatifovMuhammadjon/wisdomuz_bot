from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telebot.types import Update
from .bot import bot, TOKEN
# import requests
# from bs4 import BeautifulSoup as bs
# from .models import User,Pocket
# cookies = {
#     'ajs_anonymous_id': '4f4c5b31-cf14-4d82-9b14-63cdeb16e10b',
#     'ajs_user_id': '60a57694-4358-401e-8e9e-13eae5a1f69a',
#     '__stripe_mid': '15c4ec8b-fb44-4da5-97b5-f2adaae07fc6518f1e',
#     'csrftoken': '1dWv1RIbnEbmcJlsD7vzrjmS7i9BAvd7MVMHmCDktZqpgaYukm8V2yE3BrRccgxk',
#     'sessionid': '5kgouah6prxtjjbsk3hzotglfr76fnid',
#     '_hp2_id.3707852831': '%7B%22userId%22%3A%225185324494454043%22%2C%22pageviewId%22%3A%221905206836660659%22%2C%22sessionId%22%3A%226304981499720554%22%2C%22identity%22%3A%2260a57694-4358-401e-8e9e-13eae5a1f69a%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D',
# }

# headers = {
#     'authority': 'wisdomuzbot-production.up.railway.app',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
#     # 'cookie': 'ajs_anonymous_id=4f4c5b31-cf14-4d82-9b14-63cdeb16e10b; ajs_user_id=60a57694-4358-401e-8e9e-13eae5a1f69a; __stripe_mid=15c4ec8b-fb44-4da5-97b5-f2adaae07fc6518f1e; csrftoken=1dWv1RIbnEbmcJlsD7vzrjmS7i9BAvd7MVMHmCDktZqpgaYukm8V2yE3BrRccgxk; sessionid=5kgouah6prxtjjbsk3hzotglfr76fnid; _hp2_id.3707852831=%7B%22userId%22%3A%225185324494454043%22%2C%22pageviewId%22%3A%221905206836660659%22%2C%22sessionId%22%3A%226304981499720554%22%2C%22identity%22%3A%2260a57694-4358-401e-8e9e-13eae5a1f69a%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D',
#     'referer': 'https://wisdomuzbot-production.up.railway.app/dashboard/',
#     'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
# }
# def main():
#     for i in range(2370,2373):
#         try:
#             cnt = requests.get(f"https://wisdomuzbot-production.up.railway.app/dashboard/bot/user/{i}/change/",cookies=cookies,headers=headers)
#             cnt.encoding = "utf-8"
#             # print(cnt.text)
#             content = bs(cnt.text, "html.parser")
#             user_id = content.find("div", {"class": "form-row field-user_id"}).find("div", {"class": "readonly"}).text
#             full_name = content.find("div", {"class": "form-row field-full_name"}).find("div", {"class": "readonly"}).text
#             # print(type(full_name))
#             energy = content.find("div", {"class": "form-row field-energy"}).find("div", {"class": "readonly"}).text
#                 # id = content.find("div", {"class": "form-row field-user_id"}).find("div", {"class": "readonly"}).text
#             # tg_id = content
#             # print(user_id)
#             User.objects.create(user_id=user_id,full_name=full_name,energy=energy)
#             print(user_id,i)
#         except Exception as e:
#             print(e.args,i)

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

# def mainpoint():
    # for i in range(163848,163848+1):
    #     cnt = requests.get(f"https://wisdomuzbot-production.up.railway.app/dashboard/bot/pocket/{i}/change/",cookies=cookies,headers=headers)
    #     cnt.encoding = "utf-8"
    #     # print(cnt.text)
    #     content = bs(cnt.text, "html.parser")
    #     point = content.find("input", {"class": "vIntegerField"})["value"]
        
    #     user_id = content.find("option", {"selected": True})["value"]
    #     if int(point) > 0:
    #         Pocket.objects.create(user_id=user_id,diamonds=point)
    #         print(i)