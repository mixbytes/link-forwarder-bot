# Link Forwarder Bot
Telegram bot (actually user) which forwards message with links from one specific chat to another.

## Install
Just install requirements.txt for python
```bash
pip install -r requirements.txt
```

## Auth
Register app in my.telegram.org, get app id and app hash.
Set ENV variables:
- TG_PARSE_CHAT_ID
- TG_FORWARD_CHAT_ID
- TG_API_ID
- TG_API_HASH

First time login will require code from account. Then {sessionName}.session file will be created, with that file no login will be required.

## Run
```bash
python main.py
```