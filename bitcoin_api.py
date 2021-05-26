import requests
import json
import time
import datetime
import pandas as pd
from pybithumb.core import *
from xcoin_api_client import *
import pybithumb
import tkinter as tk
from tkinter import*
import tkinter.scrolledtext as tkst
from tkinter import Menu
from tkinter import ttk
import os
import bitcoin_api
import threading
from pybithumb import Bithumb

def trunc(number, ndigits):
    parts = str(number).split('.') # divides number into 2 parts. for ex: -5, and 4427926
    truncated_number = '.'.join([parts[0], parts[1][:ndigits]]) # We keep this first part, while taking only 2 digits from the second part. Then we concat it together to get '-5.44'
    return round(float(truncated_number), ndigits)  # This should return a float number, but to make sure it is roundded to 2 decimals.

def coin_ticker_public(coin_name,sto_N,sto_m,sto_t):
    try:
        bitcoin_api_url = 'https://api.bithumb.com/public/ticker/%s_%s'%(coin_name,"KRW")
        response = requests.get(bitcoin_api_url)
        time.sleep(1)
        response_json = response.json()

        closing_price = response_json['data']['closing_price']


        #print("closing_price",closing_price)

        ##
        bitcoin_api_url = 'https://api.bithumb.com/public/candlestick/%s_%s/%s' % (coin_name, "KRW", "1m")
        response = requests.get(bitcoin_api_url)
        time.sleep(1)
        response_json = response.json()
        df = pd.DataFrame(response_json['data'])
        df.set_index(0, inplace=True)
        df.columns = ["price", "close", "high", "low", "trade"]

        # 스토캐스틱 %K (fast %K) = (현재가격-N일중 최저가)/(N일중 최고가-N일중 최저가) ×100
        df["max%d" % sto_N] = (df["high"]).rolling(sto_N).max()
        df["min%d" % sto_N] = (df["low"]).rolling(sto_N).min()
        df["stochastic%K"] = df.apply(lambda x: 100 * (int(x["close"]) - x["min%d" % sto_N]) /
                                                (x["max%d" % sto_N] - x["min%d" % sto_N])
        if (x["max%d" % sto_N] - x["min%d" % sto_N]) != 0 else 50, 1)
        # 스토캐스틱 %D (fast %D) = m일 동안 %K 평균 = Slow %K
        # slow %K = 위에서 구한 스토캐스틱 %D
        df["slow_%K"] = df["stochastic%K"].rolling(sto_m).mean()
        # slow %D = t일 동안의 slow %K 평균
        df["slow_%D"] = df["slow_%K"].rolling(sto_t).mean()

        length = df.iloc[len(df) - 1]["stochastic%K"]
        smoothk = df.iloc[len(df) - 1]["slow_%K"]
        smoothd = df.iloc[len(df) - 1]["slow_%D"]

        ## 5분 평균
        avg_5mins = df.iloc[len(df['close']) - 5:]['close']
        total_5min_price = 0
        for avg_5min in avg_5mins:
            total_5min_price += float(avg_5min)
        avg_5min_price = total_5min_price / 5
        #print("avg_5min_price", avg_5min_price)

        ## 10분 평균
        avg_10mins = df.iloc[len(df['close']) - 10:]['close']
        total_10min_price = 0
        for avg_10min in avg_10mins:
            total_10min_price += float(avg_10min)
        avg_10min_price = total_10min_price / 10
        #print("avg_10min_price", avg_10min_price)

        ## 30분 평균
        avg_30mins = df.iloc[len(df['close']) - 30:]['close']
        total_30min_price = 0
        for avg_30min in avg_30mins:
            total_30min_price += float(avg_30min)
        avg_30min_price = total_30min_price / 30
        #print("avg_30min_price", avg_30min_price)

        ## 1시간 평균
        avg_1hours = df.iloc[len(df['close']) - 60:]['close']
        total_1hour_price = 0
        for avg_1hour in avg_1hours:
            total_1hour_price += float(avg_1hour)
        avg_1hour_price = total_1hour_price / 60
        #print("avg_1hour_price", avg_1hour_price)

        length = df.iloc[len(df) - 1]["stochastic%K"]
        #print("length", length)

        smoothk = df.iloc[len(df) - 1]["slow_%K"]
        #print("smoothk", smoothk)

        smoothd = df.iloc[len(df) - 1]["slow_%D"]
        #print("smoothd", smoothd)
    except Exception as ex:
        closing_price=0
        avg_5min_price=0
        avg_10min_price=0
        avg_30min_price=0
        avg_1hour_price=0
        length=0
        smoothk=0
        smoothd=0

    return closing_price,avg_5min_price,avg_10min_price,avg_30min_price,avg_1hour_price,length,smoothk,smoothd


def get_balance(con_key,sec_key):
    api = XCoinAPI(con_key, sec_key)

    parm = {
    }
    result = api.xcoinApiCall("/info/balance", parm)
    available_krw = result["data"]["available_krw"]

    return available_krw

def market_buy(con_key,sec_key,coin):
    bitcoin_api_url = 'https://api.bithumb.com/public/ticker/%s_%s' % (coin, "KRW")
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    closing_price = response_json['data']['closing_price']
    balance = float(closing_price)

    available_krw = float(get_balance(con_key,sec_key))
    #available_krw = float(trunc(available_krw,4))


    available_coin_count = float((available_krw * 0.7) / balance)

    available_coin_count = format(float(available_coin_count), ".8f")

    available_coin_count = float(trunc(available_coin_count,6))

    print("현재 사용가능원화",(available_krw))

    print("현재 시장가", (balance))

    print("현재 구매가능수량", (available_coin_count))

    bithumb = Bithumb(con_key, sec_key)
    result =bithumb.buy_market_order(coin,available_coin_count,"KRW")

    """api = XCoinAPI(con_key, sec_key)
    parm = {
        "order_currency": coin,
        "payment_currency": "KRW",
        "units" : (available_coin_count)
    }
    result = api.xcoinApiCall("/trade/market_buy", parm)"""
    print("response", result)
    return result

def get_account(con_key,sec_key,coin):
    api = XCoinAPI(con_key, sec_key)

    parm = {
        "order_currency": coin,
        "payment_currency": "KRW"
    }
    result = api.xcoinApiCall("/info/account", parm)
    balance = result['data']["balance"]
    return balance

def market_sell(con_key,sec_key,coin):
    balance = float(get_account(con_key,sec_key,coin))

    balance = float(format(float(balance), ".8f"))
    balance = float(trunc(balance, 4))


    print(coin,balance)
    api = XCoinAPI(con_key, sec_key)

    parm = {
        "order_currency": coin,
        "payment_currency": "KRW",
        "units": (balance)
    }
    result = api.xcoinApiCall("/trade/market_sell", parm)

    print("response", result)
    return result