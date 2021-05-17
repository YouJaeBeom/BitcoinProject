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
    # Click OK button
    def clickOK():
        text = "Your gender is " + gender.get()
        text = text + "\nYou are " + str(age.get()) + " years old.\n"
        scrt.insert(tk.INSERT, text)  # insert text in a scrolledtext
        scrt.see(tk.END)

    # Click radio buttons
    def clickRadio():
        scrt.insert(tk.INSERT, value3.get())
        scrt.see(tk.END)

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

    for index in range(1,10):
        value2 = tk.IntVar()
        check2 = tk.Checkbutton(win, variable=value2)  # Create a check button
        check2.grid(column=0, row=index)

        coinname_textbox = ttk.Entry(win, width=10, textvariable=str)
        coinname_textbox.grid(column=1, row=index)

        price_textbox = ttk.Entry(win, width=10, textvariable=str)
        price_textbox.grid(column=2, row=index)

        avg5_textbox = ttk.Entry(win, width=10, textvariable=str)
        avg5_textbox.grid(column=3, row=index)

        avg10_textbox = ttk.Entry(win, width=10, textvariable=str)
        avg10_textbox.grid(column=4, row=index)

        avg30_textbox = ttk.Entry(win, width=10, textvariable=str)
        avg30_textbox.grid(column=5, row=index)

        avg60_textbox = ttk.Entry(win, width=10, textvariable=str)
        avg60_textbox.grid(column=6, row=index)

        length_textbox = ttk.Entry(win, width=10, textvariable=str)
        length_textbox.grid(column=7, row=index)

        smoothk_textbox = ttk.Entry(win, width=10, textvariable=str)
        smoothk_textbox.grid(column=9, row=index)

        smoothd_textbox = ttk.Entry(win, width=10, textvariable=str)
        smoothd_textbox.grid(column=11, row=index)

    ## API KEY setting gui
    label_apiKey = ttk.Label(win, text="apiKey")  # Create a label
    label_apiKey.grid(column=0, row=11)  # Label's grid
    apiKey_textbox = ttk.Entry(win, width=10, textvariable=str)
    apiKey_textbox.grid(column=0, row=12)

    label_secretKey = ttk.Label(win, text="secretKey")  # Create a label
    label_secretKey.grid(column=1, row=11)  # Label's grid
    secretKey_textbox = ttk.Entry(win, width=10, textvariable=str)
    secretKey_textbox.grid(column=1, row=12)

    label_portnumber = ttk.Label(win, text="포트번호")  # Create a label
    label_portnumber.grid(column=2, row=11)  # Label's grid
    portnumber = tk.StringVar()  # String variable
    portnumberCombo = ttk.Combobox(win, width=6, textvariable=portnumber)  # Create a combobox
    portnumberCombo['values'] = ("COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9")  # Combobox's items
    portnumberCombo.grid(column=2, row=12)
    portnumberCombo.current(0)

    start_action = ttk.Button(win, text="시작", command=clickOK)  # Create a button
    start_action.grid(column=5, row=12)

    end_action = ttk.Button(win, text="종료", command=clickOK)  # Create a button
    end_action.grid(column=6, row=12)



    """
    gender = tk.StringVar()  # String variable
    genderCombo = ttk.Combobox(win, width=6, textvariable=gender)  # Create a combobox
    genderCombo['values'] = ("Female", "Male")  # Combobox's items
    genderCombo.grid(column=0, row=1)
    genderCombo.current(0)

    age = tk.IntVar()  # Integer variable
    ageEntered = ttk.Entry(win, width=3, textvariable=age)  # Create a textbox
    ageEntered.grid(column=1, row=1)
    """

    """action = ttk.Button(win, text="OK", command=clickOK)  # Create a button
    action.grid(column=2, row=1)

    scrt = tkst.ScrolledText(win, width=33, height=3, wrap=tk.WORD)  # Create a scrolledtext
    scrt.grid(column=0, row=2, columnspan=3)
    scrt.focus_set()  # Default focus

    value1 = tk.IntVar()
    check1 = tk.Checkbutton(win, text="Disabled", variable=value1, state='disabled')  # Create a check button
    check1.select()
    check1.grid(column=0, row=3)

    value2 = tk.IntVar()
    check2 = tk.Checkbutton(win, text="UnChecked", variable=value2)  # Create a check button
    check2.grid(column=1, row=3)

    value3 = tk.StringVar()
    rad1 = tk.Radiobutton(win, text="Radio1", variable=value3, value="Clicked a Radio1.\n",
                          command=clickRadio)  # Create a radio button
    rad1.select()
    rad1.grid(column=2, row=3)
    rad2 = tk.Radiobutton(win, text="Radio2", variable=value3, value="Clicked a Radio2.\n",
                          command=clickRadio)  # Create a radio button
    rad2.grid(column=2, row=4)"""

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










