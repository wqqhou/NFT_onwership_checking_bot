import sys
import logging
import asyncio
from io import BytesIO
import qrcode
import proof
import requests
import check
import crypto

from pytoniq_core import Address
from pytonconnect import TonConnect

import config
from connector import get_connector

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import db

logger = logging.getLogger(__file__)

dp = Dispatcher()
bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    chat_id = message.chat.id
    connector = get_connector(chat_id)
    connected = await connector.restore_connection()
    db.check_user(chat_id)

    mk_b = InlineKeyboardBuilder()
    if connected:
        mk_b.button(text='Disconnect', callback_data='disconnect')
        await message.answer(text='You are already connected!', reply_markup=mk_b.as_markup())

    else:
        mk_b.button(text='Request to Join', url=config.GROUP_LINK)
        wallets_list = TonConnect.get_wallets()
        for wallet in wallets_list:
            mk_b.button(text=wallet['name'], callback_data=f'connect:{wallet["name"]}')
        mk_b.adjust(1, )
        await message.answer(text="💎Welcome to the Ton Market Maker Club!💎\n\nWe're happy to have you join us and hope you'll actively participate in building and sharing your thoughts with us. Everyone here is ready to help and support!✨\n\n🔔 Please follow the community guidelines and avoid unnecessary conflicts.\n\n🔵 Be Respectful: Stay polite and friendly, avoid insults or discrimination.\n🔵 No Ads: Don't advertise or promote commercially here. Contact our CM for queries.\n🔵 Sharing is caring: Join discussions, share valuable info, and help community growth.\n🔵 Protect Privacy: Don't share others' personal info without permission. Respecting the privacy rights of every member.\n\nThanks for your support! Let's keep our community positive and fun together!\n\n=============================\n\n💎歡迎加入Ton Market Maker Club ！💎\n\n我們很高興有你的加入，希望你在這裡能與我們一起共同建設以及隨時都可以分享你的想法以及提出疑問，大家將會在這裡提供幫助以及支持！✨\n\n🔔 請注意社群規範，謹慎遵守，避免引起不必要的爭議。詳細規定請查看下方規範\n\n🔵尊重他人：請保持禮貌和友善的態度，不要發表侮辱性、歧視性或攻擊性言論。\n🔵禁止廣告：請不要在社群中進行商業廣告或推銷行為，如有需要請洽談我們的CM。\n🔵共建共享：請積極參與社群討論，分享有價值的資訊和想法，共同促進社群的成長和發展。\n🔵尊重隱私：請不要在未經允許的情況下公開他人的個人資訊，保護每個成員的隱私權。\n\n感謝大家的配合和支持！讓我們一起維護社群的和諧氛圍，共同打造一個愉快的交流空間！")
        await message.answer(text='Plase request to join first, and then choose a wallet to connect.', reply_markup=mk_b.as_markup())

        


async def connect_wallet(message: Message, wallet_name: str):
    connector = get_connector(message.chat.id)
    proof_payload = proof.generate_payload(600)
    wallets_list = connector.get_wallets()
    wallet = None

    for w in wallets_list:
        if w['name'] == wallet_name:
            wallet = w

    if wallet is None:
        raise Exception(f'Unknown wallet: {wallet_name}')

    generated_url = await connector.connect(wallet, {
        'ton_proof': proof_payload
    })

    mk_b = InlineKeyboardBuilder()
    mk_b.button(text='Connect', url=generated_url)

    img = qrcode.make(generated_url)
    stream = BytesIO()
    img.save(stream)
    file = BufferedInputFile(file=stream.getvalue(), filename='qrcode')

    await message.answer_photo(photo=file, caption='Connect wallet within 3 minutes', reply_markup=mk_b.as_markup())

    mk_b = InlineKeyboardBuilder()
    mk_b.button(text='Disconnect', callback_data='disconnect')
    owner = False

    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                if proof.check_payload(proof_payload, connector.wallet):
                    nft_resp = requests.get(f'https://tonapi.io/v2/nfts/collections/{config.NFT_CONTRACT}/items?'
                                            f'api_key= "{config.API_KEY}"').json()
                    for items in nft_resp['nft_items']:
                         if wallet_address == crypto.account_forms(items['owner']['address']):

                             db.set_address(message.chat.id, wallet_address)
                             await message.answer(f'You are connected with address <code>{wallet_address}</code>', reply_markup=mk_b.as_markup())
                             logger.info(f'Connected with address: {wallet_address}')
                             owner = True
                             try:
                                 await bot.approve_chat_join_request(config.CHAT_ID, message.chat.id)
                             except Exception as e:
                                 print(e)
                                 mk_b = InlineKeyboardBuilder()
                                 mk_b.button(text='Request to Join', url=config.GROUP_LINK) 
                                 await message.answer(f'Either you are already in the chat, or you have not sent the join request. Please send the request and try again.', reply_markup=mk_b.as_markup())           
                    if not owner:
                        await message.answer(f'The address <code>{wallet_address}</code> does not possess any required NFT.', reply_markup=mk_b.as_markup())
                else:
                    await message.answer(f'Proof error!', reply_markup=mk_b.as_markup())
            return
    mk_b = InlineKeyboardBuilder()
    mk_b.button(text='Start', callback_data='start')
    await message.answer(f'Timeout error!', reply_markup=mk_b.as_markup())


async def disconnect_wallet(message: Message):
    connector = get_connector(message.chat.id)
    mk_b = InlineKeyboardBuilder()
    mk_b.button(text='Start', callback_data='start')
    await connector.restore_connection()
    await connector.disconnect()
    await message.answer('You have been successfully disconnected!', reply_markup=mk_b.as_markup())


@dp.callback_query(lambda call: True)
async def main_callback_handler(call: CallbackQuery):
    await call.answer()
    message = call.message
    data = call.data
    if data == "start":
        await command_start_handler(message)
    elif data == 'disconnect':
        try:
            await disconnect_wallet(message)
        except Exception as e:
            print(e)
            mk_b = InlineKeyboardBuilder()
            mk_b.button(text='Start', callback_data='start')
            await message.answer('You are not connected to any wallet.', reply_markup=mk_b.as_markup())
    else:
        data = data.split(':')
        if data[0] == 'connect':
            await connect_wallet(message, data[1])


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)  # skip_updates = True
    coro = check.start()
    task = asyncio.create_task(coro)
    await dp.start_polling(bot)
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
    