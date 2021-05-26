#!/usr/bin/python

import serial
import time
import signal
import threading
#initialization and open the port

def readThread(ser):
    # 쓰레드 종료될때까지 계속 돌림
    while(True):
        ser.flushInput()  # flush input buffer, discarding all its contents
        response = ser.readline()
        response_text = response.decode('utf-8')
        try:
            print("read data: " + (response_text))
        except Exception as ee:
            print("error >>", ee)

def writeThread(ser):
    # 쓰레드 종료될때까지 계속 돌림
    ser.flushOutput()
    while (True):
        # write data
        ser.write(str.encode("AT+CSQ"))



if __name__ == "__main__":
    #종료 시그널 등록
    ser = serial.Serial()
    ser.port = "COM5"
    ser.baudrate = 9600
    ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
    ser.parity = serial.PARITY_NONE  # set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
    ser.timeout = 1  # non-block read
    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2  # timeout for write

    try:
        ser.open()
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()

    #시리얼 읽을 쓰레드 생성
    thread_read = threading.Thread(target=readThread, args=(ser,))

    # 시리얼 쓰기 쓰레드 생성
    thread_write = threading.Thread(target=writeThread, args=(ser,))

    #시작!
    thread_read.start()
    thread_write.start()