# Run this ONCE on your phone (Termux) or PC, not on the host.
# It prints a session string that you paste into the SESSION_STRING env var.
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("API_ID: ").strip())
api_hash = input("API_HASH: ").strip()

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("\nYour SESSION_STRING (keep it secret):\n")
    print(client.session.save())
