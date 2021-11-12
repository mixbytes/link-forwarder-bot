import os
from telethon.sync import TelegramClient, events, types
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

API_ID = os.environ["TG_API_ID"]
API_HASH = os.environ["TG_API_HASH"]
PARSE_CHAT_ID = int(os.environ["TG_PARSE_CHAT_ID"])
FORWARD_CHAT_ID = int(os.environ["TG_FORWARD_CHAT_ID"])
SESSION = "SOPHIEPALEOLOG"

forward_chat = None

async def handler(message):
    if message.chat_id != PARSE_CHAT_ID:
        return
    for ent, _ in message.get_entities_text():
        if isinstance(ent, types.MessageEntityUrl) or isinstance(ent, types.MessageEntityTextUrl):
            try:
                await message.forward_to(forward_chat)
            except Exception as e:
                logging.error(e)
                logging.warning(message)
            finally:
                return
    
def main():
    global forward_chat
    with TelegramClient(SESSION, API_ID, API_HASH) as client:
        forward_chat = client.get_entity(FORWARD_CHAT_ID)
        client.add_event_handler(handler, events.NewMessage)
        client.run_until_disconnected()

if __name__ == '__main__':
    main()