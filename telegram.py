import os
import requests

TOKEN_TELEGRAM = os.getenv('TELEGRAM_TOKEN')
URL_TELEGRAM_UPDATES= f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/getUpdates"

def get_chat_ids():

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
                chat_ids['groups'].append(chat_info['id'])

        elif 'message' in update:
            chat_info = update['message']['chat']
            chat_type = chat_info['type']
            if chat_type == 'private':
                chat_ids['directs'].append(chat_info['id'])
            elif chat_type in ['group', 'supergroup']:
                chat_ids['groups'].append(chat_info['id'])

    chat_ids['groups'] = list(set(chat_ids['groups']))
    chat_ids['directs'] = list(set(chat_ids['directs']))

    return chat_ids


def send_messages(chat_ids, message):
    directs_ids = chat_ids['directs']
    for chat_id in directs_ids:
        chat_id_str = str(chat_id)
        response = send_telegram_message(chat_id_str, message)
        print(response)

    groups_ids = chat_ids['groups']
    for chat_id in groups_ids:
        chat_id_str = str(chat_id)
        response = send_telegram_message(chat_id_str, message)
        print(response)

def send_telegram_message(chat_id, message):
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

    return {"error": f"An error occurred while sending the message to chat_id: {chat_id}."}
