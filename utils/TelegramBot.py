import os
import requests
import asyncio
import aiohttp

class TelegramBot:
  def __init__(self):
    self.token = os.getenv('TELEGRAM_TOKEN')
    self.base_url = f"https://api.telegram.org/bot{self.token}"
    self.url_updates = f"{self.base_url}/getUpdates"
    self.url_send = f"{self.base_url}/sendMessage"


  def get_chats(self):
    response = requests.get(self.url_updates)
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


async def send_messages_async(self, chat_ids, message):
  async with aiohttp.ClientSession() as session:
    tasks = []
    for chat_id in chat_ids:
      task = asyncio.create_task(self.send_telegram_message_async(session, chat_id, message))
      print(f"Adding task to send message to chat_id: {chat_id}")
      tasks.append(task)

    responses = await asyncio.gather(*tasks)
    return responses


async def send_telegram_message_async(self, session, chat_id, message):
  payload = {"chat_id": chat_id, "text": message}

  try:
    async with session.post(self.url_send, data=payload) as response:
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


def send_messages(self, chat_ids, message):
  responses = []
  for chat_id in chat_ids:
    chat_id_str = str(chat_id)
    response = self.send_message(chat_id_str, message)
    responses.append(response)
  return responses 

    
def send_message(self, chat_id, message):
  payload = {"chat_id": chat_id, "text": message}

  try:
    response = requests.post(self.url_send, data=payload)
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
