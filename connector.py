from pytonconnect import TonConnect
import config

def get_connector(chat_id: int):
    return TonConnect(config.MANIFEST_URL)