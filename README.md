# TON NFT-Gated Telegram Bot

A Telegram bot that verifies TON wallet ownership and NFT holdings before granting access to a private community.

## What it does

- Connects users to TON wallets through TonConnect and generates QR/deep-link connection requests.
- Verifies signed wallet proofs with expiring payloads before accepting a connection.
- Queries a specified TON NFT collection and checks whether the connected wallet owns a qualifying NFT.
- Automatically approves Telegram join requests for verified NFT holders.
- Stores Telegram-user and wallet-address mappings in SQLite and periodically rechecks recorded ownership.

## Technical focus

**Python, aiogram, TonConnect, TON API, SQLite, asyncio, QR-code generation, cryptographic proof verification**

The project demonstrates event-driven bot development, external API integration, persistent user state, and token-gated access control.


Insert your own OKX API & Telegram bot credentials in the config file. 
````
nano config.py
````

Start the bot
````
python3 bot.py
````
