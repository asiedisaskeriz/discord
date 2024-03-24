import os
import sys
import json
import time
import requests
from websocket import WebSocket
from keep_alive import keep_alive

status = "online" #online/dnd/idle

GUILD_ID = 1168551939299086386
CHANNEL_ID = 1170013140193390632
SELF_MUTE = False
SELF_DEAF = False

usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

userinfo = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def on_open(ws):
    auth = {
        "op": 2,
        "d": {
            "token": usertoken,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows"
            },
            "presence": {
                "status": status,
                "since": int(time.time() * 1000),
                "afk": False
            }
        },
        "s": None,
        "t": None
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

def on_error(ws, error):
    print(f"[ERROR] {error}")

def on_close(ws):
    print("[INFO] Connection closed.")

def on_message(ws, message):
    print(f"[INFO] Received message: {message}")

def run_joiner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        ws = WebSocket()
        ws.connect('wss://gateway.discordapp.com/?v=9&encoding=json')
        ws.on_message = on_message
        ws.on_error = on_error
        ws.on_close = on_close
        ws.on_open = on_open
        ws.run_forever()

keep_alive()
run_joiner()
