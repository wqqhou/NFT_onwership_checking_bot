# Requests for API, Asyncio to call sleep() in async func
import asyncio
import okx.Account as Account
import okx.PublicData as Public
import okx.MarketData as MarketData
from timeit import default_timer as timer

# Aiogram
from aiogram import Bot

# We also need config here
import db
import config

accountAPI = Account.AccountAPI(config.API_KEY, config.API_SECRET_KEY, config.API_PASSPHRASE, False, flag="0")
publicAPI = Public.PublicAPI(config.API_KEY, config.API_SECRET_KEY, config.API_PASSPHRASE, False, flag="0")
marketDataAPI =  MarketData.MarketAPI(config.API_KEY, config.API_SECRET_KEY, config.API_PASSPHRASE, False, flag="0")



async def start():

    bot = Bot(token=config.BOT_TOKEN)

    while True:
        # 60 Seconds delay between checks
        start = timer()

        alert = False
        msg = '[Rate Alert]'

        try:
            resp_i = accountAPI.get_interest_rate()
            uid_list = db.get_subscribers()
        except:
            continue

        if not resp_i or resp_i['code'] != '0':
            continue

        for ccy in resp_i['data']:
            i_rate = float(ccy['interestRate']) * 876000

            if i_rate > 25:

                alert = True
                syb = ccy['ccy']
                inst = syb + '-USDT-SWAP'
                tik = syb + '-USDT'

                try:
                    resp_f = publicAPI.get_funding_rate(instId=inst)
                    f_rate = float(resp_f['data'][0]['fundingRate']) * 100
                    
                    resp_p = marketDataAPI.get_index_tickers(instId=tik)
                    price = resp_p['data'][0]['idxPx']

                    msg += f'\n\n{syb}:\nInterest Rate is {i_rate}%\nFunding Rate is {f_rate}%\nPrice is ${price}'

                except:
                    msg += f'\n\n{syb}: \nInterest Rate is {i_rate}%'

        if alert:        
            for uid in uid_list:
                try:
                   await bot.send_message(uid, msg)
                except:
                    pass

        end = timer()

        await asyncio.sleep(300 - (end - start))