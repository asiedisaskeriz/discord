import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

keep_alive()

status = "dnd"  # online/dnd/idle

GUILD_ID = 1168551939299086386
CHANNEL_ID = 1170013140193390632
SELF_MUTE = False
SELF_DEAF = False

usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def joiner(token, status):
    ws = websocket.WebSocketApp('wss://gateway.discord.gg/?v=9&encoding=json')
    
    def on_message(ws, message):
        print("Received:", message)
        # Burada mesajları işleyebilirsiniz

    def on_error(ws, error):
        print("Error:", error)

    def on_close(ws):
        print("Connection closed")

    def on_open(ws):
        print("Connected")
        auth = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "Windows 10",
                    "$browser": "Google Chrome",
                    "$device": "Windows"
                },
                "presence": {
                    "status": status,
                    "afk": False
                }
            }
        }
        vc = {
            "op": 4,
            "d": {
                "guild_id": GUILD_ID,
                "channel_id": CHANNEL_ID,
                "self_mute": SELF_MUTE,
                "self_deaf": SELF_DEAF
            }
        }
        ws.send(json.dumps(auth))
        ws.send(json.dumps(vc))
    
    ws.on_message = on_message
    ws.on_error = on_error
    ws.on_close = on_close
    ws.on_open = on_open
    
    ws.run_forever()

def run_joiner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        joiner(usertoken, status)
        time.sleep(30)

keep_alive()
run_joiner()
