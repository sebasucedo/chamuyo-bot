from openai import OpenAI
from datetime import datetime

class InspirationalMessageGenerator:
  def __init__(self, model="gpt-4"):
    self.model = model
    self.client = OpenAI()


  def get_message_content(self):
    try:
      weekday_number = datetime.now().weekday()
      days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
      current_weekday = days_of_the_week[weekday_number]
      prompt = f"Write an inspirational phrase for a development team based on the current day of the week. Today is {current_weekday}."

      completion = self.client.chat.completions.create(
        model=self.model,
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


  def get_response(self, incoming_message):
    try:
      prompt = f"Respond briefly in a single line as if in a dialogue, the following telegram short message with the most extreme of purist agilism: {incoming_message}."

      completion = self.client.chat.completions.create(
        model=self.model,
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
