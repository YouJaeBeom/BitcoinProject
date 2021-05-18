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
from tkinter import*
import tkinter.scrolledtext as tkst
from tkinter import Menu
from tkinter import ttk
import os
import threading



def coin_ticker_public(coin_name):

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

    return closing_price


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
    # Click OK button

    def realtime_update():
        while True:
            for index,value in enumerate(lines):
                closing_price = coin_ticker_public(value)
                price_textEntry[index].set(closing_price)

    def clickOK():
        global con_key
        con_key = apiKey_textbox.get()
        global sec_key
        sec_key = secretKey_textbox.get()

        threading.Thread(target=realtime_update, daemon=True).start()


    # Click a exit menu
    def clickExit():
        win.quit()
        win.destroy()
        exit()

    win = tk.Tk()  # Create instance
    win.title("tkinter sample")  # Add a title

    label_check = ttk.Label(win, text=" check")  # Create a label
    label_check.grid(column=0, row=0)  # Label's grid

    label_coinname = ttk.Label(win, text=" 코인명")  # Create a label
    label_coinname.grid(column=1, row=0)  # Label's grid

    label_price = ttk.Label(win, text=" 현재가")  # Create a label
    label_price.grid(column=2, row=0)  # Label's grid

    label_avg5 = ttk.Label(win, text=" 5분평균")  # Create a label
    label_avg5.grid(column=3, row=0)  # Label's grid

    label_avg10 = ttk.Label(win, text=" 10분평균")  # Create a label
    label_avg10.grid(column=4, row=0)  # Label's grid

    label_avg30 = ttk.Label(win, text=" 30분평균")  # Create a label
    label_avg30.grid(column=5, row=0)  # Label's grid

    label_avg60 = ttk.Label(win, text=" 1시간 평균")  # Create a label
    label_avg60.grid(column=6, row=0)  # Label's grid

    label_length = ttk.Label(win, text="길이")  # Create a label
    label_length.grid(column=7, row=0)  # Label's grid

    length = tk.IntVar()  # Integer variable
    length_Entered = ttk.Entry(win, width=3, textvariable=length)  # Create a textbox
    length_Entered.grid(column=8, row=0)

    label_smoothk = ttk.Label(win, text="스무스K")  # Create a label
    label_smoothk.grid(column=9, row=0)  # Label's grid

    smoothk = tk.IntVar()  # Integer variable
    smoothk_Entered = ttk.Entry(win, width=3, textvariable=smoothk)  # Create a textbox
    smoothk_Entered.grid(column=10, row=0)

    label_smoothd = ttk.Label(win, text="스무스D")  # Create a label
    label_smoothd.grid(column=11, row=0)  # Label's grid

    smoothd = tk.IntVar()  # Integer variable
    smoothd_Entered = ttk.Entry(win, width=3, textvariable=smoothd)  # Create a textbox
    smoothd_Entered.grid(column=12, row=0)

    check_box = {}
    coinname_textboxs ={}
    coinname_textEntry = {}
    price_textboxs={}
    price_textEntry = {}
    avg5_textboxs={}
    avg5_textEntry = {}
    avg10_textboxs={}
    avg10_textEntry = {}
    avg30_textboxs={}
    avg30_textEntry = {}
    avg60_textboxs={}
    avg60_textEntry = {}
    length_textboxs={}
    length_textEntry = {}
    smoothk_textboxs={}
    smoothk_textEntry = {}
    smoothd_textboxs={}
    smoothd_textEntry = {}



    print(os.getcwd())
    f = open(os.getcwd()+"/coin.txt", 'r')
    lines = f.readline()
    lines = lines.split(",")

    for index,val in enumerate((lines)):
        value = tk.IntVar()
        check = tk.Checkbutton(
            win,
            variable=value
        )
        check.grid(column=0, row=index+1)
        check_box[index] = check

        coinname_textEntry[index] = tk.StringVar()
        coinname_textEntry[index].set(val)
        coinname_textbox = ttk.Entry(win, width=10, textvariable=coinname_textEntry[index])
        coinname_textbox.grid(column=1, row=index+1)
        coinname_textboxs[index] = coinname_textbox

        price_textEntry[index] = tk.StringVar()
        #price_textEntry[index].set(val)
        price_textbox = ttk.Entry(win, width=10, textvariable=price_textEntry[index])
        price_textbox.grid(column=2, row=index+1)
        price_textboxs[index] = price_textbox

        avg5_textEntry[index] = tk.StringVar()
        #avg5_textEntry[index].set(val)
        avg5_textbox = ttk.Entry(win, width=10, textvariable=avg5_textEntry[index])
        avg5_textbox.grid(column=3, row=index+1)
        avg5_textboxs[index] = avg5_textbox

        avg10_textEntry[index] = tk.StringVar()
        #avg10_textEntry[index].set(val)
        avg10_textbox = ttk.Entry(win, width=10, textvariable=avg10_textEntry[index])
        avg10_textbox.grid(column=4, row=index+1)
        avg10_textboxs[index] = avg10_textbox

        avg30_textEntry[index] = tk.StringVar()
        #avg30_textEntry[index].set(val)
        avg30_textbox = ttk.Entry(win, width=10, textvariable=avg30_textEntry[index])
        avg30_textbox.grid(column=5, row=index+1)
        avg30_textboxs[index] = avg30_textbox

        avg60_textEntry[index] = tk.StringVar()
        #avg60_textEntry[index].set(val)
        avg60_textbox = ttk.Entry(win, width=10, textvariable=avg60_textEntry[index])
        avg60_textbox.grid(column=6, row=index+1)
        avg60_textboxs[index] = avg60_textbox

        length_textEntry[index] = tk.StringVar()
        #length_textEntry[index].set(val)
        length_textbox = ttk.Entry(win, width=10, textvariable=length_textEntry[index])
        length_textbox.grid(column=7, row=index+1)
        length_textboxs[index] = length_textbox

        smoothk_textEntry[index] = tk.StringVar()
        #smoothk_textEntry[index].set(val)
        smoothk_textbox = ttk.Entry(win, width=10, textvariable=smoothk_textEntry[index])
        smoothk_textbox.grid(column=9, row=index+1)
        smoothk_textboxs[index] = smoothk_textbox

        smoothd_textEntry[index] = tk.StringVar()
        #smoothd_textEntry[index].set(val)
        smoothd_textbox = ttk.Entry(win, width=10, textvariable=smoothd_textEntry[index])
        smoothd_textbox.grid(column=11, row=index+1)
        smoothd_textboxs[index] = smoothd_textbox

    ## API KEY setting gui
    label_apiKey = ttk.Label(win, text="apiKey")  # Create a label
    label_apiKey.grid(column=0, row=len(lines)+1)  # Label's grid
    apiKey_textbox = ttk.Entry(win, width=20, textvariable=str)
    apiKey_textbox.insert(0, "")
    apiKey_textbox.grid(column=0, row=len(lines)+2)

    label_secretKey = ttk.Label(win, text="secretKey")  # Create a label
    label_secretKey.grid(column=1, row=len(lines)+1)  # Label's grid
    secretKey_textbox = ttk.Entry(win, width=20, textvariable=str)
    secretKey_textbox.insert(0, "")
    secretKey_textbox.grid(column=1, row=len(lines)+2)

    label_portnumber = ttk.Label(win, text="포트번호")  # Create a label
    label_portnumber.grid(column=2, row=len(lines)+1)  # Label's grid
    portnumber = tk.StringVar()  # String variable
    portnumberCombo = ttk.Combobox(win, width=6, textvariable=portnumber)  # Create a combobox
    portnumberCombo['values'] = ("COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9")  # Combobox's items
    portnumberCombo.grid(column=2, row=len(lines)+2)
    portnumberCombo.current(0)

    start_action = ttk.Button(win, text="시작", command=clickOK)  # Create a button
    start_action.grid(column=5, row=len(lines)+2)

    end_action = ttk.Button(win, text="종료", command=clickExit)  # Create a button
    end_action.grid(column=6, row=len(lines)+2)

    menuBar = Menu(win)  # Create a menu
    win.config(menu=menuBar)

    fileMenu = Menu(menuBar, tearoff=0)  # Create the File Menu
    fileMenu.add_command(label="New")  # Add the "New" menu
    fileMenu.add_separator()  # Add a separator
    fileMenu.add_command(label="Exit", command=clickExit)  # Add the "Exit" menu and bind a function
    menuBar.add_cascade(label="File", menu=fileMenu)

    win.resizable(0, 0)  # Disable resizing the GUI
    win.mainloop()  # Start GUI




if __name__ == '__main__':
    gui()

    #coin_name_list = ["BTC", "XRP", "ETH"]
    coin_name_list = ["BTC"]
    #chart_intervals_list = ['1m', '3m', '5m', '10m', '30m', '1h', '6h', '12h', '24h']
    chart_intervals_list = ['1m']

    sto_N = 14
    sto_m = 1
    sto_t = 3

    #coin_ticker_public(coin_name_list)
    #coin_candlestick(coin_name_list,chart_intervals_list,sto_N,sto_m,sto_t)

    """
    global con_key
    con_key="92ccf25a931830a4c3dd664662d22011"
    global sec_key
    sec_key="007734825a89b23735232c9aff5e38a9"
    """



    #market_buy("ETC")
    #market_sell("ETC")










