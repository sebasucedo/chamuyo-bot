import os
import requests
import asyncio
import aiohttp

TOKEN_TELEGRAM = os.getenv('TELEGRAM_TOKEN')
URL_TELEGRAM_UPDATES= f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/getUpdates"

def get_chats():
    response = requests.get(URL_TELEGRAM_UPDATES)
    updates = response.json().get('result', [])

    chat_ids = {
        'groups': [],
        'directs': []
    }
    for update in updates:
        chat_info = None

        if 'my_chat_member' in update:
            chat_info = update['my_chat_member']['chat']
            chat_type = chat_info['type']
            if chat_type in ['group', 'supergroup']:
                chat_ids['groups'].append({'id': chat_info['id'], 'name': chat_info.get('title'), 'type': "group"})

        elif 'message' in update:
            chat_info = update['message']['chat']
            chat_type = chat_info['type']
            if chat_type == 'private':
                chat_ids['directs'].append({'id': chat_info['id'], 'name': chat_info.get('username'), 'type': "direct"})
            elif chat_type in ['group', 'supergroup']:
                chat_ids['groups'].append({'id': chat_info['id'], 'name': chat_info.get('title'), 'type': "group"})

    unique_group_ids = {each['id']: each for each in chat_ids['groups']}.values()
    chat_ids['groups'] = list(unique_group_ids)

    unique_direct_ids = {each['id']: each for each in chat_ids['directs']}.values()
    chat_ids['directs'] = list(unique_direct_ids)

    return chat_ids


async def send_messages_async(chat_ids, message):
    async with aiohttp.ClientSession() as session:
      tasks = []
      for chat_id in chat_ids:
          task = asyncio.create_task(send_telegram_message(session, chat_id, message))
          print(f"Adding task to send message to chat_id: {chat_id}")
          tasks.append(task)

      responses = await asyncio.gather(*tasks)
      return responses

async def send_telegram_message_async(session, chat_id, message):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    try:
      async with session.post(url, data=payload) as response:
          return await response.json() 
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred while making the request: {req_err}")

    return {"error": f"An error occurred while sending the message to chat_id: {chat_id}."}


def send_messages(chat_ids, message):
    for chat_id in chat_ids:
        chat_id_str = str(chat_id)
        response = send_message(chat_id_str, message)
        print(response) 
    
def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred while making the request: {req_err}")
