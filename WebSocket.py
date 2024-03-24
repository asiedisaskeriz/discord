import os
import sys
import json
import time
import requests
import websocket

def on_open(ws):
    auth = {"op": 2,"d": {"token": usertoken,"properties": {"$os": "Windows 10","$browser": "Google Chrome","$device": "Windows"},"presence": {"status": status,"afk": False}},"s": None,"t": None}
    vc = {"op": 4,"d": {"guild_id": GUILD_ID,"channel_id": CHANNEL_ID,"self_mute": SELF_MUTE,"self_deaf": SELF_DEAF}}
    ws.send(json.dumps(auth))
    ws.send(json.dumps(vc))
    time.sleep(30)
    ws.close()

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
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discordapp.com/?v=9&encoding=json')
        ws.run_forever(on_open=on_open, on_error=on_error, on_close=on_close, on_message=on_message)
        time.sleep(30)

run_joiner()
