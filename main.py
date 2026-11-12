import asyncio
import os
import re

from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

BOT = os.environ.get("BOT_USERNAME", "FAABOT")
CHANNEL_KEYWORD = os.environ.get("CHANNEL_KEYWORD", "talabatkom").lower()
BUTTON_TEXT = os.environ.get("BUTTON_TEXT", "استخدام كود")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
seen = set()
lock = asyncio.Lock()
CODE_RE = re.compile(r"الكود\s*[:：]\s*([A-Za-z0-9_-]+)")


async def redeem(code):
    async with lock:
        try:
            async with client.conversation(BOT, timeout=20) as conv:
                await conv.send_message("/start")
                menu = None
                for _ in range(3):
                    msg = await conv.get_response()
                    if msg.buttons:
                        menu = msg
                        break
                if not menu:
                    print("[!] menu with buttons not found", flush=True)
                    return
                await menu.click(text=lambda t: BUTTON_TEXT in t)
                try:
                    await conv.get_response(timeout=2)  # "send your code" prompt
                except asyncio.TimeoutError:
                    pass
                await conv.send_message(code)
                reply = await conv.get_response()
                print(f"[+] code {code} -> {reply.raw_text}", flush=True)
        except Exception as e:
            print(f"[!] error while redeeming {code}: {e}", flush=True)


@client.on(events.NewMessage)
async def handler(event):
    if not event.is_channel:
        return
    chat = await event.get_chat()
    title = (getattr(chat, "title", "") or "").lower()
    if CHANNEL_KEYWORD not in title:
        return
    match = CODE_RE.search(event.raw_text or "")
    if not match:
        return
    code = match.group(1)
    if code in seen:
        return
    seen.add(code)
    print(f"[*] new code detected: {code}", flush=True)
    await redeem(code)


async def health_server():
    # Tiny HTTP server so web hosts (e.g. Render free) see an open port
    # and an uptime pinger can keep the service awake.
    port = int(os.environ.get("PORT", "10000"))

    async def on_conn(reader, writer):
        try:
            await reader.read(1024)
            body = b"ok"
            writer.write(
                b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
                b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                b"Connection: close\r\n\r\n" + body
            )
            await writer.drain()
        finally:
            writer.close()

    server = await asyncio.start_server(on_conn, "0.0.0.0", port)
    print(f"[*] health server listening on port {port}", flush=True)
    return server


async def main():
    await health_server()
    await client.start()
    print("[*] voucher bot is running...", flush=True)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
