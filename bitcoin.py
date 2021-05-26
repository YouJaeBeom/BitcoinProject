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
import bitcoin_api
import threading
import serial
import signal

class Bitcoin(tk.Frame):
    def __init__(self, master):
        super(Bitcoin, self).__init__(master)

        self.win = master
        self.win.title("tkinter sample")  # Add a title

        self.label_check = ttk.Label(self.win, text=" check")  # Create a label
        self.label_check.grid(column=0, row=0)  # Label's grid

        self.label_coinname = ttk.Label(self.win, text=" 코인명")  # Create a label
        self.label_coinname.grid(column=1, row=0)  # Label's grid

        self.label_price = ttk.Label(self.win, text=" 현재가")  # Create a label
        self.label_price.grid(column=2, row=0)  # Label's grid

        self.label_avg5 = ttk.Label(self.win, text=" 5분평균")  # Create a label
        self.label_avg5.grid(column=3, row=0)  # Label's grid

        self.label_avg10 = ttk.Label(self.win, text=" 10분평균")  # Create a label
        self.label_avg10.grid(column=4, row=0)  # Label's grid

        self.label_avg30 = ttk.Label(self.win, text=" 30분평균")  # Create a label
        self.label_avg30.grid(column=5, row=0)  # Label's grid

        self.label_avg60 = ttk.Label(self.win, text=" 1시간 평균")  # Create a label
        self.label_avg60.grid(column=6, row=0)  # Label's grid

        self.label_length = ttk.Label(self.win, text="길이")  # Create a label
        self.label_length.grid(column=7, row=0)  # Label's grid

        self.length = tk.IntVar()  # Integer variable
        #self.length.set(14)
        self.length_Entered = ttk.Entry(self.win, width=3, textvariable=self.length)  # Create a textbox
        self.length_Entered.grid(column=8, row=0)

        self.label_smoothk = ttk.Label(self.win, text="스무스K")  # Create a label
        self.label_smoothk.grid(column=9, row=0)  # Label's grid

        self.smoothk = tk.IntVar()  # Integer variable
        #self.smoothk.set(1)
        self.smoothk_Entered = ttk.Entry(self.win, width=3, textvariable=self.smoothk)  # Create a textbox
        self.smoothk_Entered.grid(column=10, row=0)

        self.label_smoothd = ttk.Label(self.win, text="스무스D")  # Create a label
        self.label_smoothd.grid(column=11, row=0)  # Label's grid

        self.smoothd = tk.IntVar()  # Integer variable
        #self.smoothd.set(3)
        self.smoothd_Entered = ttk.Entry(self.win, width=3, textvariable=self.smoothd)  # Create a textbox
        self.smoothd_Entered.grid(column=12, row=0)

        self.check_box = {}
        self.coinname_textboxs = {}
        self.coinname_textEntry = {}
        self.price_textboxs = {}
        self.price_textEntry = {}
        self.avg5_textboxs = {}
        self.avg5_textEntry = {}
        self.avg10_textboxs = {}
        self.avg10_textEntry = {}
        self.avg30_textboxs = {}
        self.avg30_textEntry = {}
        self.avg60_textboxs = {}
        self.avg60_textEntry = {}
        self.length_textboxs = {}
        self.length_textEntry = {}
        self.smoothk_textboxs = {}
        self.smoothk_textEntry = {}
        self.smoothd_textboxs = {}
        self.smoothd_textEntry = {}

        print(os.getcwd())
        self.f = open(os.getcwd() + "/coin.txt", 'r')
        self.lines = self.f.readline()
        self.lines = self.lines.split(",")

        for index, val in enumerate((self.lines)):
            value = tk.IntVar()
            self.check = tk.Checkbutton(
                self.win,
                variable=value
            )
            self.check.grid(column=0, row=index + 1)
            self.check_box[index] = self.check

            self.coinname_textEntry[index] = tk.StringVar()
            self.coinname_textEntry[index].set(val)
            self.coinname_textbox = ttk.Entry(self.win, width=15, textvariable=self.coinname_textEntry[index])
            self.coinname_textbox.grid(column=1, row=index + 1)
            self.coinname_textboxs[index] = self.coinname_textbox

            self.price_textEntry[index] = tk.StringVar()
            # price_textEntry[index].set(val)
            self.price_textbox = ttk.Entry(self.win, width=15, textvariable=self.price_textEntry[index])
            self.price_textbox.grid(column=2, row=index + 1)
            self.price_textboxs[index] = self.price_textbox

            self.avg5_textEntry[index] = tk.StringVar()
            # avg5_textEntry[index].set(val)
            self.avg5_textbox = ttk.Entry(self.win, width=15, textvariable=self.avg5_textEntry[index])
            self.avg5_textbox.grid(column=3, row=index + 1)
            self.avg5_textboxs[index] = self.avg5_textbox

            self.avg10_textEntry[index] = tk.StringVar()
            # avg10_textEntry[index].set(val)
            self.avg10_textbox = ttk.Entry(self.win, width=15, textvariable=self.avg10_textEntry[index])
            self.avg10_textbox.grid(column=4, row=index + 1)
            self.avg10_textboxs[index] = self.avg10_textbox

            self.avg30_textEntry[index] = tk.StringVar()
            # avg30_textEntry[index].set(val)
            self.avg30_textbox = ttk.Entry(self.win, width=15, textvariable=self.avg30_textEntry[index])
            self.avg30_textbox.grid(column=5, row=index + 1)
            self.avg30_textboxs[index] = self.avg30_textbox

            self.avg60_textEntry[index] = tk.StringVar()
            # avg60_textEntry[index].set(val)
            self.avg60_textbox = ttk.Entry(self.win, width=15, textvariable=self.avg60_textEntry[index])
            self.avg60_textbox.grid(column=6, row=index + 1)
            self.avg60_textboxs[index] = self.avg60_textbox

            self.length_textEntry[index] = tk.StringVar()
            # length_textEntry[index].set(val)
            self.length_textbox = ttk.Entry(self.win, width=10, textvariable=self.length_textEntry[index])
            self.length_textbox.grid(column=7, row=index + 1,columnspan=2)
            self.length_textboxs[index] = self.length_textbox

            self.smoothk_textEntry[index] = tk.StringVar()
            # smoothk_textEntry[index].set(val)
            self.smoothk_textbox = ttk.Entry(self.win, width=10, textvariable=self.smoothk_textEntry[index])
            self.smoothk_textbox.grid(column=9, row=index + 1,columnspan=2)
            self.smoothk_textboxs[index] = self.smoothk_textbox

            self.smoothd_textEntry[index] = tk.StringVar()
            # smoothd_textEntry[index].set(val)
            self.smoothd_textbox = ttk.Entry(self.win, width=10, textvariable=self.smoothd_textEntry[index])
            self.smoothd_textbox.grid(column=11, row=index + 1,columnspan=2)
            self.smoothd_textboxs[index] = self.smoothd_textbox

        self.scrt = tkst.ScrolledText(self.win, width=150, height=30, wrap=tk.WORD)  # Create a scrolledtext
        self.scrt.grid(column=1, row=len(self.lines) + 2, columnspan=11)
        self.scrt.focus_set()

        self.label_apiKey = ttk.Label(self.win, text="apiKey")  # Create a label
        self.label_apiKey.grid(column=0, row=len(self.lines) + 3 )  # Label's grid
        self.label_secretKey = ttk.Label(self.win, text="secretKey")  # Create a label
        self.label_secretKey.grid(column=1, row=len(self.lines) + 3 )  # Label's grid

        self.apiKey_textboxs = {}
        self.secretKey_textboxs = {}

        for index in range(0,5):
            ## API KEY setting gui
            self.apiKey_textbox = ttk.Entry(self.win, width=10, textvariable=str)
            self.apiKey_textbox.insert(0, "")
            self.apiKey_textbox.grid(column=0, row=len(self.lines) + 4+int(index))
            self.apiKey_textboxs[index] = self.apiKey_textbox

            self.secretKey_textbox = ttk.Entry(self.win, width=10, textvariable=str)
            self.secretKey_textbox.insert(0, "")
            self.secretKey_textbox.grid(column=1, row=len(self.lines) + 4+int(index))
            self.secretKey_textboxs[index] = self.secretKey_textbox

        self.label_portnumber = ttk.Label(self.win, text="포트번호")  # Create a label
        self.label_portnumber.grid(column=2, row=len(self.lines) + 3)  # Label's grid
        self.portnumber = tk.StringVar()  # String variable
        self.portnumberCombo = ttk.Combobox(self.win, width=6, textvariable=self.portnumber)  # Create a combobox
        self.portnumberCombo['values'] = (
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9")  # Combobox's items
        self.portnumberCombo.grid(column=2, row=len(self.lines) + 4)
        self.portnumberCombo.current(0)

        self.label_baudrate = ttk.Label(self.win, text="Baud Rate")  # Create a label
        self.label_baudrate.grid(column=3, row=len(self.lines) + 3)  # Label's grid
        self.baudrate = tk.StringVar()  # String variable
        self.baudrateCombo = ttk.Combobox(self.win, width=6, textvariable=self.baudrate)  # Create a combobox
        self.baudrateCombo['values'] = (
            "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200")  # Combobox's items
        self.baudrateCombo.grid(column=3, row=len(self.lines) + 4)
        self.baudrateCombo.current(0)

        self.start_action = ttk.Button(self.win, text="시작", command=self.clickOK)  # Create a button
        self.start_action.grid(column=5, row=len(self.lines) + 4)

        self.end_action = ttk.Button(self.win, text="종료", command=self.clickExit)  # Create a button
        self.end_action.grid(column=6, row=len(self.lines) + 4)

        self.buy_action = ttk.Button(self.win, text="구매", command=self.clickBUY)  # Create a button
        self.buy_action.grid(column=7, row=len(self.lines) + 4)

        self.sell_action = ttk.Button(self.win, text="판매", command=self.clickSELL)  # Create a button
        self.sell_action.grid(column=8, row=len(self.lines) + 4)

        self.menuBar = Menu(self.win)  # Create a menu
        self.win.config(menu=self.menuBar)

        self.fileMenu = Menu(self.menuBar, tearoff=0)  # Create the File Menu
        self.fileMenu.add_command(label="New")  # Add the "New" menu
        self.fileMenu.add_separator()  # Add a separator
        self.fileMenu.add_command(label="Exit", command=self.clickExit)  # Add the "Exit" menu and bind a function
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        self.win.resizable(0, 0)  # Disable resizing the GUI
        self.win.mainloop()  # Start GUI

    def pyserial_setting(self):
        self.ser = serial.Serial()
        self.ser.port = str(self.portnumberCombo.get())
        self.ser.baudrate = int(self.baudrateCombo.get())
        self.ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
        self.ser.parity = serial.PARITY_NONE  # set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
        self.ser.timeout = 1  # non-block read
        self.ser.xonxoff = False  # disable software flow control
        self.ser.rtscts = False  # disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2  # timeout for write

        try:
            print(self.ser.port,self.ser.baudrate)
            self.ser.open()
        except Exception as e:
            print("error open serial port: " + str(e))
            self.result = "error open serial port: " + str(e)+"\n"
            self.scrt.insert("end",(self.result))
            exit()

    def realtime_read(self):
        self.ser.flushInput()  # flush input buffer, discarding all its contents

        while (True):
            self.response = self.ser.readline()
            self.response_text = (self.response.decode('utf-8'))
            try :
                self.response_text = self.response_text.replace(">>","")
                self.response_text = self.response_text.replace("<<", "")
                self.coinname = self.response_text.split("/")[0]
                self.command = self.response_text.split("/")[1]
                print(self.coinname,self.command)
                if self.command =="bid":
                    for index in range(len(self.apiKey_textboxs)):
                        self.con_key = self.apiKey_textboxs[index].get()
                        self.sec_key = self.secretKey_textboxs[index].get()
                        self.buy_result = bitcoin_api.market_buy(self.con_key, self.sec_key, self.coinname)
                        self.scrt.insert("end", str(int(index)+1) +"번째 API KEY"+self.buy_result)
                elif self.command =="ask":
                    for index in range(len(self.apiKey_textboxs)):
                        self.con_key = self.apiKey_textboxs[index].get()
                        self.sec_key = self.secretKey_textboxs[index].get()
                        self.sell_result = bitcoin_api.market_sell(self.con_key, self.sec_key, self.coinname)
                        self.scrt.insert("end", str(int(index)+1) +"번째 API KEY"+self.sell_result)

            except Exception as e:
                pass



    def realtime_update(self):

        self.sto_length = int(self.length_Entered.get())
        self.sto_smoothk = int(self.smoothk_Entered.get())
        self.sto_smoothd = int(self.smoothd_Entered.get())
        if (self.sto_length ==0 and self.sto_smoothk==0 and self.sto_smoothd==0):
            self.scrt.insert("end", ("길이, 스무스 미설정 \n"))
        else :
            while True:
                for index, value in enumerate(self.lines):
                    self.closing_price,self.avg_5min_price,self.avg_10min_price,self.avg_30min_price,self.avg_1hour_price,self.length,self.smoothk,self.smoothd = bitcoin_api.coin_ticker_public(value,self.sto_length,self.sto_smoothk,self.sto_smoothd)

                    if (self.closing_price == 0
                            and self.avg_5min_price  ==0
                            and self.avg_10min_price  ==0
                            and self.avg_30min_price  ==0
                            and self.avg_1hour_price == 0
                    ):
                        continue
                    ## setting string formating
                    self.closing_price = format(float(self.closing_price), "014.3f")
                    self.avg_5min_price = format(float(self.avg_5min_price), "014.3f")
                    self.avg_10min_price = format(float(self.avg_10min_price), "014.3f")
                    self.avg_30min_price = format(float(self.avg_30min_price), "014.3f")
                    self.avg_1hour_price = format(float(self.avg_1hour_price), "014.3f")
                    self.length = format(int(self.length), "03d")
                    self.smoothk = format(int(self.smoothk), "03d")
                    self.smoothd = format(int(self.smoothd), "03d")

                    ## text setting
                    self.price_textEntry[index].set(self.closing_price)
                    self.avg5_textEntry[index].set(self.avg_5min_price)
                    self.avg10_textEntry[index].set(self.avg_10min_price)
                    self.avg30_textEntry[index].set(self.avg_30min_price)
                    self.avg60_textEntry[index].set(self.avg_1hour_price)
                    self.length_textEntry[index].set(self.length)
                    self.smoothk_textEntry[index].set(self.smoothk)
                    self.smoothd_textEntry[index].set(self.smoothd)


                    self.serial_protocol = (">>"+value+"__"+"/"+str(self.closing_price)
                                            +"/"+str(self.closing_price)
                                            +"/"+str(self.avg_5min_price)
                                            +"/"+str(self.avg_10min_price)
                                            +"/"+str(self.avg_30min_price)
                                            +"/"+str(self.avg_1hour_price)
                                            +"/"+str(self.length)
                                            +"/"+str(self.smoothk)
                                            +"/"+str(self.smoothd)
                                            +"/<<")
                    self.ser.flushOutput()
                    self.ser.write(str.encode(self.serial_protocol))
                    time.sleep(1)

    def clickOK(self):
        self.pyserial_setting()
        threading.Thread(target=self.realtime_update, daemon=True).start()
        threading.Thread(target=self.realtime_read, daemon=True).start()

    # Click a exit menu
    def clickExit(self):
        self.win.quit()
        self.win.destroy()
        self.exit()

    def clickBUY(self):
        self.con_key = self.apiKey_textbox.get()
        self.sec_key = self.secretKey_textbox.get()

        self.buy_result = bitcoin_api.market_buy(self.con_key,self.sec_key,"ETH")
        self.scrt.insert("end",self.buy_result)



    def clickSELL(self):
        self.con_key = self.apiKey_textbox.get()
        self.sec_key = self.secretKey_textbox.get()

        self.sell_result = bitcoin_api.market_sell(self.con_key, self.sec_key,"ETH")
        self.scrt.insert("end", self.sell_result)




if __name__ == '__main__':
    root = tk.Tk()
    bitcoin = Bitcoin(root)
    bitcoin.mainloop()












