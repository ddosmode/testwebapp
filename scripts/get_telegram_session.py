#!/usr/bin/env python3
"""Get Telegram session string for telegram-mcp.

Run this file locally. It will prompt for phone, Telegram confirmation code,
and 2FA password if needed, then save the session string to a file.
"""

import asyncio
import sys
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    PhoneCodeInvalidError,
    PasswordHashInvalidError,
    SessionPasswordNeededError,
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    FloodWaitError,
)

API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION_FILE = os.path.join(os.path.dirname(__file__), "telegram_session_string.txt")


def save_session(session_str: str) -> None:
    with open(SESSION_FILE, "w") as f:
        f.write(session_str.strip())
    print(f"\nSession string saved to: {SESSION_FILE}")


async def main() -> int:
    phone = input("Phone (international format, e.g. 48795940332): ").strip()
    if not phone:
        print("Phone is required.")
        return 1
    if phone.startswith("+"):
        phone = phone[1:]
        print(f"Stripped '+' from phone, using: {phone}")

    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        try:
            sent_code = await client.send_code_request(phone)
        except PhoneNumberInvalidError:
            print("Invalid phone number.")
            return 1
        except ApiIdInvalidError:
            print("Invalid API credentials.")
            return 1
        except FloodWaitError as e:
            print(f"Too many requests. Wait {e.seconds} seconds.")
            return 1

        print("\nCHECK YOUR OTHER TELEGRAM DEVICE/APP!")
        print("The confirmation code should appear there as a login alert/message.")
        print("Do NOT wait for SMS - look inside your Telegram app on another device.")
        print("If you don't see it within 60 seconds, press Enter to retry.\n")

        code = input("Telegram confirmation code: ").strip()
        if not code:
            print("\nRetrying code request...")
            try:
                sent_code = await client.send_code_request(phone)
            except FloodWaitError as e:
                print(f"Too many requests. Wait {e.seconds} seconds.")
                return 1
            print("Check your Telegram app again. Code sent.")
            code = input("Telegram confirmation code: ").strip()

        try:
            await client.sign_in(phone, code, phone_code_hash=sent_code.phone_code_hash)
        except SessionPasswordNeededError:
            password = input("2FA password: ")
            try:
                await client.sign_in(password=password)
            except PasswordHashInvalidError:
                print("Invalid 2FA password.")
                return 1
            except Exception as e:
                print(f"2FA error: {type(e).__name__}: {e}")
                return 1
        except PhoneCodeInvalidError:
            print("Invalid confirmation code. Restart and try again.")
            return 1
        except FloodWaitError as e:
            print(f"Too many requests. Wait {e.seconds} seconds.")
            return 1
        except Exception as e:
            print(f"Sign in error: {type(e).__name__}: {e}")
            return 1

    if not await client.is_user_authorized():
        print("Authorization failed.")
        return 1

    session_str = StringSession.save(client.session)
    save_session(session_str)
    me = await client.get_me()
    print(f"Authorized as: {me.first_name} (id={me.id})")
    await client.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
