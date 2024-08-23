import requests
import time
import os

def get_updates(token, offset=None):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {'offset': offset} if offset else {}
    response = requests.get(url, params=params)
    return response.json()

def print_new_messages(token):
    offset = None
    while True:
        updates = get_updates(token, offset)
        if "result" in updates:
            for update in updates["result"]:
                message = update["message"]
                user_id = message["from"]["id"]
                username = message["from"]["first_name"]
                text = message.get("text")
                print(f"Usuario: {username} ({user_id})")
                print(f"Mensaje: {text}")
                print("---")
                offset = update["update_id"] + 1
        time.sleep(0.1)  # Esperar 1 segundo antes de obtener nuevas actualizaciones

# Obtén el valor del token desde las variables de entorno
token = os.environ.get('TELEGRAM_TOKEN')

# Verifica si el token es None
if token is None:
    print("Error: La variable de entorno TELEGRAM_TOKEN no está configurada.")
else:
    print_new_messages(token)