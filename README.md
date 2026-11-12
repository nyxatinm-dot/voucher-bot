# voucher-bot

Telegram userbot (Telethon) that watches a channel for free-points codes
and redeems them in the target bot automatically.

## Setup
1. Run `python generate_session.py` once (Termux or PC) and copy the printed string.
2. On the host, set environment variables (see `.env.example`):
   API_ID, API_HASH, SESSION_STRING (required), the rest are optional.
3. Start command: `python main.py` (worker process, not web).
