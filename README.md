# binance-bot

Algorithmic trading bot for Binance exchange which uses Talib indicators

##DISCLAIMER

I am not responsible for any money you lose with this bot. Use it at your own risk.

## Installation

## Requirements
* python
* TA-Lib
`$ pip install TA-Lib`


## Usage

You should insert your Binance API Key and Secret into binance_bot/account_info in the following format:

```
'API Key'
'API Secret'
```

Put currencies you would like to trade into coins array

```
coins = ['ETHBTC', 'LTCBTC', 'BNBBTC', 'NEOBTC', 'BCCBTC', 'GASBTC']
```
Put maximum money you would like to spend per currency into maxSpendInBTC.
```
maxSpendInBTC = 0.002
```

Put maximum number of currencies you would like to trade into maxNumberOfCurrencies
```
maxNumberOfCurrencies = 15
```

Select the time interval for your technical analysis
```
interval = ["15m"]
```

Run the bot.py to start the bot.

Current strategy uses the combination of John Carter's Squeeze Momentum and Welles Wilder's Relative Strength Index

## Donate

If this project helped you out feel free to donate.

* BTC: 1DQcKJHGwefzdQnJ4cpPGgBA7gTYUpmGia
* ETH: 0x757b7354d894c41d08f468e373ef2f1b49960d0d
* LTC: LLbAeE6AwmKJ88rewLxYnDk2LV4wJfXm6V
* NEO: AeX1bFJ6fDEGK32MKpsZkf24F9y1J9Z5Hu
* EOS: 0x757b7354d894c41d08f468e373ef2f1b49960d0d

If you have any suggested strategy for this Binance bot, you may reach me from my email.
