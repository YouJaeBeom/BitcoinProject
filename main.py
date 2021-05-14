# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json
import time
import datetime
import pandas as pd
from pybithumb.core import *
from xcoin_api_client import *
import pybithumb
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext



def coin_ticker_public(coin_name_list):

    for coin_name in coin_name_list :
        bitcoin_api_url = 'https://api.bithumb.com/public/ticker/%s_%s'%(coin_name,"KRW")
        response = requests.get(bitcoin_api_url)
        time.sleep(1)
        response_json = response.json()

        opening_price = response_json['data']['opening_price']
        closing_price = response_json['data']['closing_price']
        min_price = response_json['data']['min_price']
        max_price = response_json['data']['max_price']
        units_traded = response_json['data']['units_traded']
        acc_trade_value = response_json['data']['acc_trade_value']
        prev_closing_price = response_json['data']['prev_closing_price']
        units_traded_24H = response_json['data']['units_traded_24H']
        acc_trade_value_24H = response_json['data']['acc_trade_value_24H']
        fluctate_24H = response_json['data']['fluctate_24H']
        fluctate_rate_24H = response_json['data']['fluctate_rate_24H']
        date = response_json['data']['date']

        print("closing_price",closing_price)







def coin_candlestick(coin_name_list,chart_intervals_list,sto_N,sto_m,sto_t):

    for coin_name in coin_name_list:

        for chart_intervals in chart_intervals_list :

            bitcoin_api_url = 'https://api.bithumb.com/public/candlestick/%s_%s/%s' % (coin_name, "KRW",chart_intervals)
            response = requests.get(bitcoin_api_url)
            time.sleep(1)
            response_json = response.json()
            df = pd.DataFrame(response_json['data'])
            df.set_index(0, inplace=True)
            df.columns = ["price", "close", "high","low","trade"]

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


            ## 5분 평균
            avg_5mins = df.iloc[len(df['close']) - 5:]['close']
            total_5min_price = 0
            for avg_5min in avg_5mins:
                total_5min_price += float(avg_5min)
            avg_5min_price = total_5min_price / 5
            print("avg_5min_price",avg_5min_price)

            ## 10분 평균
            avg_10mins = df.iloc[len(df['close']) - 10:]['close']
            total_10min_price = 0
            for avg_10min in avg_10mins:
                total_10min_price += float(avg_10min)
            avg_10min_price = total_10min_price / 10
            print("avg_10min_price",avg_10min_price)

            ## 30분 평균
            avg_30mins = df.iloc[len(df['close']) - 30:]['close']
            total_30min_price = 0
            for avg_30min in avg_30mins:
                total_30min_price += float(avg_30min)
            avg_30min_price = total_30min_price / 30
            print("avg_30min_price",avg_30min_price)


            ## 1시간 평균
            avg_1hours = df.iloc[len(df['close']) - 60:]['close']
            total_1hour_price = 0
            for avg_1hour in avg_1hours:
                total_1hour_price += float(avg_1hour)
            avg_1hour_price = total_1hour_price/60
            print("avg_1hour_price",avg_1hour_price)

            print(df)
            print(df.iloc[len(df)-1]["stochastic%K"])
            result.config(text=answer)

def get_account(coin):
    api = XCoinAPI(con_key, sec_key)

    parm = {
        "order_currency": coin,
        "payment_currency": "KRW"
    }
    result = api.xcoinApiCall("/info/account", parm)
    balance = result['data']["balance"]
    return balance

def get_balance():
    api = XCoinAPI(con_key, sec_key)

    parm = {
    }
    result = api.xcoinApiCall("/info/balance", parm)
    available_krw = result["data"]["available_krw"]

    return available_krw

def market_buy(coin):
    bitcoin_api_url = 'https://api.bithumb.com/public/ticker/%s_%s' % (coin, "KRW")
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    closing_price = response_json['data']['closing_price']
    balance = float(closing_price)
    available_krw = get_balance()

    available_coin_count = (float(available_krw)*0.95/balance)

    available_coin_count = format(float(available_coin_count), ".3f")

    print("available_coin_count",available_coin_count,available_krw)


    api = XCoinAPI(con_key, sec_key)

    parm = {
        "order_currency": coin,
        "payment_currency": "KRW",
        "units" : (available_coin_count)
    }
    result = api.xcoinApiCall("/trade/market_buy", parm)

    print("response", result)

def market_sell(coin):
    balance = get_account(coin)
    balance = format(float(balance), ".4f")
    print(coin,balance)
    api = XCoinAPI(con_key, sec_key)

    parm = {
        "order_currency": coin,
        "payment_currency": "KRW",
        "units": (balance)
    }
    result = api.xcoinApiCall("/trade/market_sell", parm)

    print("response", result)

def gui():
    win = tk.Tk()

    win.title("Python GUI")

    a_label = ttk.Label(win, text="A Label")
    a_label.grid(column=0, row=0)

    def click_me():
        action.configure(text='Hello ' + name.get() + ' ' + number_chosen.get())

    ttk.Label(win, text="Enter a name:").grid(column=0, row=0)

    name = tk.StringVar()
    name_entered = ttk.Entry(win, width=12, textvariable=name)
    name_entered.grid(column=0, row=1)

    action = ttk.Button(win, text="Click Me!", command=click_me)
    action.grid(column=2, row=1)  # <= change column to 2

    ttk.Label(win, text="Choose a number:").grid(column=1, row=0)
    number = tk.StringVar()
    number_chosen = ttk.Combobox(win, width=12, textvariable=number, state='readonly')
    number_chosen['values'] = (1, 2, 4, 42, 100)
    number_chosen.grid(column=1, row=1)
    number_chosen.current(0)

    chVarDis = tk.IntVar()
    check1 = tk.Checkbutton(win, text="Disabled", variable=chVarDis, state='disabled')
    check1.select()
    check1.grid(column=0, row=4, sticky=tk.W)

    chVarUn = tk.IntVar()
    check2 = tk.Checkbutton(win, text="UnChecked", variable=chVarUn)
    check2.deselect()
    check2.grid(column=1, row=4, sticky=tk.W)

    chVarEn = tk.IntVar()
    check3 = tk.Checkbutton(win, text="Enabled", variable=chVarEn)
    check3.deselect()
    check3.grid(column=2, row=4, sticky=tk.W)



    # 스크롤 텍스트
    scrol_w = 50
    scrol_h = 3
    scr = scrolledtext.ScrolledText(win, width=scrol_w, height=scrol_h, wrap=tk.WORD)
    scr.grid(column=0, columnspan=3)

    name_entered.focus()

    win.mainloop()




if __name__ == '__main__':
    gui()

    #coin_name_list = ["BTC", "XRP", "ETH"]
    coin_name_list = ["BTC"]
    #chart_intervals_list = ['1m', '3m', '5m', '10m', '30m', '1h', '6h', '12h', '24h']
    chart_intervals_list = ['1m']

    chart_intervals_list = ['1m']

    sto_N = 14
    sto_m = 1
    sto_t = 3

    #coin_ticker_public(coin_name_list)

    coin_candlestick(coin_name_list,chart_intervals_list,sto_N,sto_m,sto_t)

    global con_key
    con_key="92ccf25a931830a4c3dd664662d22011"
    global sec_key
    sec_key="007734825a89b23735232c9aff5e38a9"



    #market_buy("ETC")
    #market_sell("ETC")










