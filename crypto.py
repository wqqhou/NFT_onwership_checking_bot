import base64

bounceable_tag, non_bounceable_tag = b'\x11', b'\x51'
b64_abc = set(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890+/')
b64_abc_urlsafe = set(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-')


def calcCRC(message):
    poly = 0x1021
    reg = 0
    message += b'\x00\x00'
    for byte in message:
        mask = 0x80
        while(mask > 0):
            reg <<= 1
            if byte & mask:
                reg += 1
            mask >>= 1
            if reg > 0xffff:
                reg &= 0xffff
                reg ^= poly
    return reg.to_bytes(2, "big")


def account_forms(raw_form, test_only=False):
    workchain, address = raw_form.split(":")
    workchain, address = int(workchain), int(address, 16)
    address = address.to_bytes(32, "big")
    workchain_tag = b'\xff' if workchain == - \
        1 else workchain.to_bytes(1, "big")
    btag = bounceable_tag
    nbtag = non_bounceable_tag
    # if test_only:
    #  btag = (btag[0] | 0x80).to_bytes(1,'big')
    #  nbtag = (nbtag[0] | 0x80).to_bytes(1,'big')
    preaddr_b = btag + workchain_tag + address
    preaddr_u = nbtag + workchain_tag + address
    b64_b = base64.b64encode(preaddr_b+calcCRC(preaddr_b)).decode('utf8')
    b64_u = base64.b64encode(preaddr_u+calcCRC(preaddr_u)).decode('utf8')
    b64_b_us = base64.urlsafe_b64encode(
        preaddr_b+calcCRC(preaddr_b)).decode('utf8')
    b64_u_us = base64.urlsafe_b64encode(
        preaddr_u+calcCRC(preaddr_u)).decode('utf8')
    return b64_u_us