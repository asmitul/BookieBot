import re


def is_usdt_adress(address):
    # TRC20 addresses start with 'T' and are 34 characters long
    pattern = r'^T[1-9A-HJ-NP-Za-km-z]{33}$'
    return bool(re.match(pattern, address))