import os
from telethon.sync import TelegramClient, events, types, functions
import logging
from datetime import date, datetime, timezone
import asyncio
from pathlib import Path

logging.basicConfig(filename="./logs.txt", filemode='a',
                    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

API_ID = os.environ["TG_API_ID"]
API_HASH = os.environ["TG_API_HASH"]
PARSE_CHAT_ID = int(os.environ["TG_PARSE_CHAT_ID"])
FORWARD_CHAT_ID = int(os.environ["TG_FORWARD_CHAT_ID"])
SESSION = "SOPHIEPALEOLOG"
INTERVAL_IN_SEC = 30
MESSAGE_MIN_LIVE_IN_SEC = 120
LAST_MESSAGE_ID = 0
GET_MESSAGE_CNT_LIMIT = 300
CLIENT_UPDATE_INTERVAL_IN_SEC = 10800

client = None
forward_chat = None
last_msg_file = Path("./lastmsg.txt")
last_client_update_time = datetime.now(timezone.utc)

# forward message if contains url
async def forward_message(message):
    for ent, _ in message.get_entities_text():
        if isinstance(ent, types.MessageEntityUrl) or isinstance(ent, types.MessageEntityTextUrl):
            try:
                await message.forward_to(forward_chat)
            except Exception as e:
                logging.error(e)
                logging.warning(message)
            finally:
                return

# gets now and date timedelta in seconds
def last_from_date_in_secs(date):
    return (datetime.now(timezone.utc) - date).seconds

def save_last_messsage_id():
    last_msg_file.write_text(str(LAST_MESSAGE_ID))

def get_last_message_id():
    global LAST_MESSAGE_ID
    if not last_msg_file.is_file():
        save_last_messsage_id()

    LAST_MESSAGE_ID = int(last_msg_file.read_text())

# check for new messages and if it lasts > MESSAGE_MIN_LIVE_IN_SEC and id > LAST_MESSAGE_ID
async def forward_new_messages():
    global LAST_MESSAGE_ID
    messages = [m async for m in client.iter_messages(PARSE_CHAT_ID, limit=GET_MESSAGE_CNT_LIMIT)
    if m.id > LAST_MESSAGE_ID and last_from_date_in_secs(m.date) > MESSAGE_MIN_LIVE_IN_SEC]
    for message in reversed(messages):
        await forward_message(message)

    if len(messages) > 0:
        LAST_MESSAGE_ID = messages[0].id
    save_last_messsage_id()

# update client and start because it somehow stops working
async def update_client():
    global last_client_update_time
    if last_from_date_in_secs(last_client_update_time) < CLIENT_UPDATE_INTERVAL_IN_SEC:
        return
    if client.is_connected():
        await client.start()
    last_client_update_time = datetime.now(timezone.utc)

async def main():
    global forward_chat, client, last_msg_file
    get_last_message_id()
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.start()
    forward_chat = await client.get_entity(FORWARD_CHAT_ID)

    while True:
        await asyncio.gather(
            asyncio.sleep(INTERVAL_IN_SEC),
            forward_new_messages(),
            update_client()
        )

if __name__ == '__main__':
    asyncio.run(main())