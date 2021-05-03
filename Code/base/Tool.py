

def filterUSDT(ex):
    markets =ex.fetch_markets()
    lst = []
    for marketObj in markets:
        if 'DOWN/USDT' in marketObj['symbol']:
            continue
        if 'UP/USDT' in marketObj['symbol']:
            continue
        if '/USDT' in marketObj['symbol']:
            lst.append(marketObj['symbol'])
    return lst