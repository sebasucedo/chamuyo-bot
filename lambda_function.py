import os
import requests
import json
from openai import OpenAI
from datetime import datetime


def lambda_handler(event, context):

  chat_ids = get_chat_ids()

  message = get_message_from_ai()

  send_mesagges(chat_ids, message)

  return {
      'statusCode': 200,
      'body': json.dumps('Messages sent!')
  }


TOKEN_TELEGRAM = os.getenv('TELEGRAM_TOKEN')
URL_TELEGRAM_UPDATES= f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/getUpdates"


def send_mesagges(chat_ids, message):
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


def get_message_from_ai():
    client = OpenAI()

    weekday_number = datetime.now().weekday()
    days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    current_weekday = days_of_the_week[weekday_number]
    prompt = f"Write an inspirational phrase for a development team based on the current day of the week. Today is {current_weekday}."

    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
      {"role": "system", "content": "You are a frustrated developer who became a scrum master, you think you are the ultimate ontological coach but you really have no experience in anything."},
      {"role": "user", "content": prompt}
      ]
    )

    message = completion.choices[0].message.content
    return message


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


def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=payload)
    return response.json()


# lambda_handler(None, None)