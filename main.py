import os
import requests
from openai import OpenAI

TOKEN_TELEGRAM = os.getenv('TELEGRAM_TOKEN')
URL_TELEGRAM_UPDATES= f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/getUpdates"


def obtener_ids_chats():
    respuesta = requests.get(URL_TELEGRAM_UPDATES)
    updates = respuesta.json().get('result', [])

    ids_chats = {
        'grupos': [],
        'directos': []
    }
    for update in updates:
        chat_info = None

        if 'my_chat_member' in update:
            chat_info = update['my_chat_member']['chat']
            chat_type = chat_info['type']
            if chat_type in ['group', 'supergroup']:
                ids_chats['grupos'].append(chat_info['id'])

        elif 'message' in update:
            chat_info = update['message']['chat']
            chat_type = chat_info['type']
            if chat_type == 'private':
                ids_chats['directos'].append(chat_info['id'])
            elif chat_type in ['group', 'supergroup']:
                ids_chats['grupos'].append(chat_info['id'])

    ids_chats['grupos'] = list(set(ids_chats['grupos']))
    ids_chats['directos'] = list(set(ids_chats['directos']))

    return ids_chats


def enviar_mensaje_telegram(chat_id, mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    datos = {"chat_id": chat_id, "text": mensaje}

    response = requests.post(url, data=datos)
    return response.json()





client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a frustrated developer who became a scrum master, you think you are the ultimate ontological coach but you really have no experience in anything."},
    {"role": "user", "content": "Write an inspirational phrase for a development team based on the current the day of the week."}
  ]
)

mensaje = completion.choices[0].message.content
# print(mensaje)



ids_chats = obtener_ids_chats()

ids_directos = ids_chats['directos']
for chat_id in ids_directos:
    chat_id_str = str(chat_id)
    respuesta = enviar_mensaje_telegram(chat_id_str, mensaje)
    # print(f"Respuesta para el chat {chat_id_str}: {respuesta}")

ids_grupos = ids_chats['grupos']
for chat_id in ids_grupos:
    chat_id_str = str(chat_id)
    respuesta = enviar_mensaje_telegram(chat_id_str, mensaje)
    # print(f"Respuesta para el chat {chat_id_str}: {respuesta}")
