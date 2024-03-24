import os
import sys
import json
import time
import requests
from websocket import create_connection

status = "online"  # online/dnd/idle

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

def run_joiner():
    os.system("cls")  # use cls for windows
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        ws = create_connection('wss://gateway.discordapp.com/?v=9&encoding=json')
        result = ws.recv()
        print(f"[INFO] Received message: {result}")

run_joiner()
