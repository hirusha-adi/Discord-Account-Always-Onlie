import discord, os, platform, nacl
from discord.ext import commands
from keep_alive import keep_alive
try:
  if platform.system().lower().startswith('win'):
    os.system("pip install pynacl")
  else:
    os.system("pip3 install pynacl")
except Exception as e:
  print("Error:", e)
  exit()

client = commands.Bot(">>", self_bot=True)
token = os.environ['TOKEN']

@client.event
async def on_ready():
  print(f"[+] Discord.py API version: {discord.__version__}")
  print(f'[+] Python version: {platform.python_version()}\n')
  print(f"[+] Logged in as {client.user.name} | {client.user} | {client.user.id}")
  print("[+] Account is online!")
  print("\n[~] Changing account activity")
  await client.change_presence(activity=discord.Streaming(name="Hackor Master", url="https://youtube.com"))
  print("[+] Changed account activity!")
  vc = client.get_channel(871428065652269063)
  await vc.connect()
  print("[+] Connected to Voice Channel")

keep_alive()
client.run(token, bot=False)
