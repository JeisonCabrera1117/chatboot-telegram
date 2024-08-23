import openai
import requests
import time
import os
from openai import OpenAI
from dotenv import dotenv_values


config = dotenv_values(".env")

# key_api_openai = os.environ.get('OPENAI_API_KEY')
key_api_openai = config['OPENAI_API_KEY']
openai = OpenAI(api_key=key_api_openai)
# token = os.environ.get('TELEGRAM_TOKEN')
token = config['TELEGRAM_TOKEN']
model = config["MODEL"]

def get_updates(offset=None):
  url = f"https://api.telegram.org/bot{token}/getUpdates"
  params = {'offset': offset} if offset else {}
  response = requests.get(url, params=params)
  return response.json()["result"]

def send_messages(chat_id, text):
  url = f"https://api.telegram.org/bot{token}/sendMessage"
  params = {"chat_id": chat_id, "text": text}
  response = requests.post(url, params=params)
  return response

def get_openai_response(prompt):
  system = '''
        Eres un asistente de atención a clientes 
        y estudiantes de la plataforma de educación online en tecnología,  
        inglés y liderazgo llamada Platzi
        '''
  model_engine = model
  response = openai.chat.completions.create(
    model = model_engine,
    messages=[
            {"role": "system", "content" :f'{system}'},
            {"role": "user", "content" : f'{prompt}'}],
    max_tokens = 150,
    n = 1,
    temperature = 0.2
  )
  return response.choices[0].message.content.strip()

def main():
  print("Starting bot..")
  offset = 0
  while True:
    updates = get_updates(offset)
    if updates :
      for update in updates:
        offset = update["update_id"] +1
        chat_id = update["message"]["chat"]["id"]
        user_message = update["message"]["text"]
        print(f"Recived message: {user_message}")
        GPT = get_openai_response(user_message)
        send_messages(chat_id, GPT)
    time.sleep(1)

if __name__ == '__main__':
  main()