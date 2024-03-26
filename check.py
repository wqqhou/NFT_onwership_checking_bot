import requests
import config
import db
import crypto
import asyncio

async def start():
    while True:
        asyncio.sleep(5)
        try:
            nft_resp = requests.get(f'https://tonapi.io/v2/nfts/collections/{config.NFT_CONTRACT}/items?'
                                    f'api_key= "{config.API_KEY}"').json()
            if not nft_resp['nft_items']:
                continue
        except: 
            continue
        users = db.get_addresses()
        for wallet_address in users:
            ownership = False
            for items in nft_resp['nft_items']:
                if wallet_address[0] == crypto.account_forms(items['owner']['address']):
                    ownership = True
                    break
            if not ownership:
                uid = db.find_user(wallet_address[0])[0][0]
                print(f'{uid} does not have the nft') 
        
