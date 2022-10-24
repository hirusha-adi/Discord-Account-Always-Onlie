
import os
import json
import platform
from threading import Thread

def pip_install(pkg: str):
    if os.name == 'nt':
        os.system('py -m pip install -U {pkg}'.format(pkg=pkg))
    else:
        os.system('python3 -m pip install -U {pkg}'.format(pkg=pkg))

try:
    import discord
    from discord.ext import commands
except:
    pip_install('discord')
finally:
    import discord
    from discord.ext import commands

try:
    import nacl
except:
    pip_install('pynacl')
finally:
    import nacl

try:
    from flask import Flask
except:
    pip_install('flask')
finally:
    from flask import Flask

class Settings:
    def __init__(self, filename="settings.json") -> None:
        with open(filename, "r", encoding="utf-8") as _file:
            self.data = json.load(_file)
            
    @property
    def token(self) -> str:
        return str(self.data['bot']['token'])
    
    @property
    def prefix(self) -> str:
        return str(self.data['bot']['prefix'])
    
    @property
    def presence_change(self) -> bool:
        return bool(self.data['bot']['presence']['change'])

    @property
    def presence_value(self) -> str:
        return str(self.data['bot']['presence']['value'])

    @property
    def voice_connect(self) -> bool:
        return bool(self.data['bot']['voice']['connect'])

    @property
    def voice_id(self) -> int:
        return int(self.data['bot']['voice']['id'])

    @property
    def web_server_start(self) -> bool:
        return bool(self.data['web_server']['start'])

    @property
    def web_server_content(self) -> str:
        return str(self.data['web_server']['content'])
    


settings = Settings(filename="settings.json")

if settings.web_server_start:
    app = Flask('')

    @app.route('/')
    def home():
        return f"{settings.web_server_content}"

    def _start_web_server():
        app.run(host='0.0.0.0', port=8080)
        
    def start_web_server():
        t = Thread(target=_start_web_server)
        t.start()

client = commands.Bot(settings.prefix, self_bot=True, intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f"[+] Discord.py API version: {discord.__version__}")
    print(f'[+] Python version: {platform.python_version()}')
    print(f"[+] Logged in as {client.user.name} | {client.user} | {client.user.id}")
    print("[+] Account is online!")
    print("\n[~] Changing account activity")
    
    if settings.presence_change:
        await client.change_presence(
            activity=discord.Streaming(
                name="Hackor Master", 
                url="https://youtube.com"
                )
            )
        print("[+] Changed account activity!")
    
    if settings.voice_connect:
        vc = client.get_channel(settings.voice_id)
        await vc.connect()
        print("[+] Connected to Voice Channel")

if __name__ == "__main__":
    
    if settings.web_server_start:
        start_web_server()
    client.run(settings.token, bot=False)
