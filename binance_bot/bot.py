import time

import numpy as np
import pandas as pd
import talib as talib
import talib.abstract as tb
from binance.client import Client


class Bot:
    coins = ['ETHBTC', 'LTCBTC', 'BNBBTC', 'NEOBTC', 'BCCBTC', 'GASBTC', 'HSRBTC', 'MCOBTC', 'WTCBTC', 'LRCBTC',
             'QTUMBTC', 'YOYOBTC', 'OMGBTC', 'ZRXBTC', 'STRATBTC', 'SNGLSBTC', 'BQXBTC', 'KNCBTC', 'FUNBTC', 'SNMBTC',
             'IOTABTC', 'LINKBTC', 'XVGBTC', 'CTRBTC', 'SALTBTC', 'MDABTC', 'MTLBTC', 'SUBBTC', 'EOSBTC', 'SNTBTC',
             'ETCBTC', 'MTHBTC', 'ENGBTC', 'DNTBTC', 'ZECBTC', 'BNTBTC', 'ASTBTC', 'DASHBTC', 'OAXBTC', 'ICNBTC',
             'BTGBTC', 'XRPBTC', 'EVXBTC', 'REQBTC', 'VIBBTC', 'TRXBTC', 'POWRBTC', 'ARKBTC', 'MODBTC', 'ENJBTC',
             'STORJBTC', 'VENBTC', 'KMDBTC', 'RCNBTC', 'NULSBTC', 'RDNBTC', 'XMRBTC', 'DLTBTC', 'AMBBTC', 'BATBTC',
             'BCPTBTC', 'ARNBTC', 'GVTBTC', 'CDTBTC', 'GXSBTC', 'POEBTC', 'QSPBTC', 'BTSBTC', 'XZCBTC', 'LSKBTC',
             'TNTBTC', 'FUELBTC', 'MANABTC', 'BCDBTC', 'DGDBTC', 'ADXBTC', 'ADABTC', 'PPTBTC', 'CMTBTC', 'XLMBTC',
             'CNDBTC', 'LENDBTC', 'WABIBTC', 'TNBBTC', 'WAVESBTC', 'GTOBTC', 'ICXBTC', 'OSTBTC', 'ELFBTC', 'AIONBTC',
             'NEBLBTC', 'BRDBTC', 'EDOBTC', 'WINGSBTC', 'NAVBTC',
             'LUNBTC', 'TRIGBTC', 'APPCBTC']

    min_amount_dict = {'ETHBTC': '3', 'LTCBTC': '2', 'BNBBTC': '0', 'NEOBTC': '2', 'GASBTC': '2', 'BCCBTC': '3',
                       'MCOBTC': '2', 'WTCBTC': '0', 'QTUMBTC': '2', 'OMGBTC': '2', 'ZRXBTC': '0', 'STRATBTC': '2',
                       'SNGLSBTC': '0', 'BQXBTC': '0', 'KNCBTC': '0', 'FUNBTC': '0', 'SNMBTC': '0', 'LINKBTC': '0',
                       'XVGBTC': '0', 'CTRBTC': '0', 'SALTBTC': '2', 'IOTABTC': '0', 'MDABTC': '0', 'MTLBTC': '0',
                       'SUBBTC': '0', 'EOSBTC': '0', 'SNTBTC': '0', 'ETCBTC': '2', 'MTHBTC': '0', 'ENGBTC': '0',
                       'DNTBTC': '0', 'BNTBTC': '0', 'ASTBTC': '0', 'DASHBTC': '3', 'ICNBTC': '0', 'OAXBTC': '0',
                       'BTGBTC': '2', 'EVXBTC': '0', 'REQBTC': '0', 'LRCBTC': '0', 'VIBBTC': '0', 'HSRBTC': '0',
                       'TRXBTC': '0', 'POWRBTC': '0', 'ARKBTC': '2', 'YOYOBTC': '0', 'XRPBTC': '0', 'MODBTC': '0',
                       'ENJBTC': '0', 'STORJBTC': '0', 'VENBTC': '0', 'KMDBTC': '0', 'RCNBTC': '0', 'NULSBTC': '0',
                       'RDNBTC': '0', 'XMRBTC': '3', 'DLTBTC': '0', 'AMBBTC': '3', 'BATBTC': '0', 'ZECBTC': '3',
                       'BCPTBTC': '0', 'ARNBTC': '0', 'GVTBTC': '2', 'CDTBTC': '0', 'GXSBTC': '2', 'POEBTC': '0',
                       'QSPBTC': '0', 'BTSBTC': '0', 'XZCBTC': '2', 'LSKBTC': '2', 'TNTBTC': '0', 'FUELBTC': '0',
                       'MANABTC': '0', 'BCDBTC': '3', 'DGDBTC': '3', 'ADXBTC': '0', 'ADABTC': '0', 'PPTBTC': '2',
                       'CMTBTC': '0', 'XLMBTC': '0', 'CNDBTC': '0', 'LENDBTC': '0', 'WABIBTC': '0', 'TNBBTC': '0',
                       'WAVESBTC': '2', 'ICXBTC': '2', 'GTOBTC': '0', 'OSTBTC': '0', 'ELFBTC': '0', 'AIONBTC': '0',
                       'NEBLBTC': '0', 'BRDBTC': '0', 'EDOBTC': '0', 'WINGSBTC': '0', 'NAVBTC': '0', 'LUNBTC': '0',
                       'TRIGBTC': '0', 'APPCBTC': '0'}

    maxSpendInBTC = 0.002
    maxNumberOfCurrencies = 15
    interval = ["15m"]

    def __init__(self):

        f = open("account_info.txt", 'r')
        message = f.read().split("\n")

        self.client = Client(message[0], message[1])
        self.BTC = 0  # available USD dollars
        self.balance = []  # shows currencies with amounts(0.0 currencies are also included)
        self.available_currencies = []  # shows only available currencies
        self.refreshBalance()

        print("Bot initialized")

    def run(self):
        print("Bot is running")
        while True:
            for coin in self.coins:
                try:
                    klines = self.client.get_klines(symbol=coin, interval=Bot.interval)
                    array = np.array(klines, dtype='f8')
                    df = pd.DataFrame(data=array[:, 0:6], columns=["date", "open", "high", "low", "close", "volume"])
                    plus_di = tb.PLUS_DI(df, timeperiod=20)
                    minus_di = tb.MINUS_DI(df, timeperiod=20)
                    upperBB, lowerBB, old_upperBB, old_lowerBB = self.BBANDS(df, length=20, mult=1.75)
                    upperKC, lowerKC, old_upperKC, old_lowerKC = self.KELCH(df, length=20, mult=1.5)
                    plus = plus_di[len(plus_di) - 2]
                    old_plus = plus_di[len(plus_di) - 1]
                    minus = minus_di[len(minus_di) - 2]
                    old_minus = minus_di[len(minus_di) - 1]
                    print(coin, plus, minus, lowerKC, lowerBB, upperBB, upperKC)
                    if plus > minus and old_plus > old_minus and plus > 27 and old_plus > 27 and \
                                    lowerBB < lowerKC and old_lowerBB < old_lowerKC and \
                                    upperBB > upperKC and old_upperBB > old_upperKC:
                        self.buyCoin(coin, df)
                    if (plus < minus and old_plus < old_minus) or (plus < 20 and old_plus < 20):
                        self.sellCoin(coin, df)

                except Exception as ex:
                    print("Exception", ex)
                    time.sleep(60.0)
                    pass

            time.sleep(60 * 10)

    def buyCoin(self, coin, df):
        self.refreshBalance()

        if (coin not in self.available_currencies):
            print("Buying coin attempt: " + coin)
            print("Available currencies: " + str(self.available_currencies))

            if float(self.BTC) < 0.0011:
                print("Less than 0.001 BTC", self.BTC)
                min_coin = ""
                min_plus = 100
                min_df = None

                for curr_coin in self.available_currencies:
                    klines = self.client.get_klines(symbol=curr_coin, interval=Bot.interval)
                    array = np.array(klines, dtype='f8')
                    df = pd.DataFrame(data=array[:, 0:6], columns=["date", "open", "high", "low", "close", "volume"])
                    plus_di = tb.PLUS_DI(df, timeperiod=20)
                    minus_di = tb.MINUS_DI(df, timeperiod=20)
                    upperBB, lowerBB, old_upperBB, old_lowerBB = self.BBANDS(df, length=20, mult=1.75)
                    upperKC, lowerKC, old_upperKC, old_lowerKC = self.KELCH(df, length=20, mult=1.5)
                    plus = plus_di[len(plus_di) - 2]

                    if min_plus > plus and lowerBB > lowerKC and upperBB < upperKC:
                        min_coin = curr_coin
                        min_plus = plus
                        min_df = df

                    if min_plus < 25:
                        self.sellCoin(min_coin, min_df)
                        self.refreshBalance()
                        time.sleep(30.0)

            else:
                price = df["close"][len(df) - 1]
                min_amount = int(Bot.min_amount_dict[coin])
                amount = self.maxSpendInBTC / float(price)
                amount = round(amount, min_amount)
                while amount * price < 0.001:
                    amount += pow(10, -min_amount)
                print("Buying", amount, coin, "at", price)
                self.client.create_order(symbol=coin, side="BUY", type="MARKET", quantity=amount)
                self.refreshBalance()

    def sellCoin(self, coin, df):
        self.refreshBalance()
        if (coin in self.available_currencies):
            print("Selling coin attempt: " + coin)
            print("Available currencies: " + str(self.available_currencies))
            amount = 0
            min_amount = int(Bot.min_amount_dict[coin])
            for dict in self.balance:
                if dict["asset"] == coin:
                    print("Asset found")
                    amount = dict["free"]
                    amount = round(amount, min_amount)
                    if amount > dict["free"]:
                        amount = dict["free"] - pow(10, -min_amount)
                        amount = round(amount, min_amount)
            price = df["close"][len(df) - 1]
            print("Selling", amount, coin, "at", price)
            print("Selling", amount, coin)
            self.client.create_order(symbol=coin, side="SELL", type="MARKET", quantity=amount)
            self.refreshBalance()

    def refreshBalance(self):
        balance = self.client.get_account()["balances"]
        if (balance != None):
            self.available_currencies = []
            self.balance = []
            for dict in balance:
                dict["free"] = float(dict["free"])
                dict["locked"] = float(dict["locked"])
                if dict["asset"] == "BTC":
                    self.BTC = float(dict["free"])
                elif (dict["free"] > 0.0):
                    min_amount = pow(10, -int(Bot.min_amount_dict[dict["asset"] + "BTC"]))
                    if (dict["free"] >= min_amount):
                        dict["asset"] = dict["asset"] + "BTC"
                        self.available_currencies.append(dict["asset"])
                        self.balance.append(dict)

    def BBANDS(self, df, length, mult):
        bbands = tb.BBANDS(df * 100000, nbdevup=mult, nbdevdn=mult, timeperiod=length)
        upperBB = bbands["upperband"] / 100000
        lowerBB = bbands["lowerband"] / 100000
        return upperBB[len(upperBB) - 1], lowerBB[len(lowerBB) - 1], upperBB[len(upperBB) - 2], lowerBB[
            len(lowerBB) - 2]

    def KELCH(self, df, length, mult):
        ma = tb.MA(df, timeperiod=length)
        range = tb.TRANGE(df)
        rangema = talib.MA(np.array(range), timeperiod=length)
        upperKC = ma + rangema * mult
        lowerKC = ma - rangema * mult
        return upperKC[len(upperKC) - 1], lowerKC[len(lowerKC) - 1], upperKC[len(upperKC) - 2], lowerKC[
            len(lowerKC) - 2]
