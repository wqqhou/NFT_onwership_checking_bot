from datetime import datetime
from nacl.utils import random
from pytonconnect.parsers import WalletInfo


def generate_payload(ttl: int) -> str:
    payload = bytearray(random(8))

    ts = int(datetime.now().timestamp()) + ttl
    payload.extend(ts.to_bytes(8, 'big'))

    return payload.hex()


def check_payload(payload: str, wallet_info: WalletInfo):
    if len(payload) < 32:
        print('Payload length error')
        return False
    if not wallet_info.check_proof(payload):
        print('Check proof failed')
        return False
    ts = int(payload[16:32], 16)
    if datetime.now().timestamp() > ts:
        print('Request timeout error')
        return False
    return True