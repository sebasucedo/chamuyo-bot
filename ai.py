from openai import OpenAI
from datetime import datetime

MODEL = "gpt-4"

def get_message_content():
    try:
      client = OpenAI()

      weekday_number = datetime.now().weekday()
      days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
      current_weekday = days_of_the_week[weekday_number]
      prompt = f"Write an inspirational phrase for a development team based on the current day of the week. Today is {current_weekday}."

      completion = client.chat.completions.create(
      model=MODEL,
      messages=[
        {"role": "system", "content": "You are a frustrated developer who became a scrum master, you think you are the ultimate ontological coach but you really have no experience in anything."},
        {"role": "user", "content": prompt}
        ]
      )

      message = completion.choices[0].message.content
      return message
    except Exception as e:
        print(f"An unexpected error occurred trying to get message content: {e}")
        raise
    