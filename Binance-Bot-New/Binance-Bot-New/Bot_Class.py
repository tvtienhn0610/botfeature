from email import message
import os
import sys
import time
from markupsafe import soft_unicode
from ta.momentum import stochrsi_d, stochrsi_k, stoch, stoch_signal, rsi, awesome_oscillator
from ta.trend import ema_indicator, macd_signal, macd, sma_indicator, adx, sma_indicator, cci
from ta.volatility import average_true_range, bollinger_pband, bollinger_hband, bollinger_lband, bollinger_mavg
from ta.volume import ease_of_movement, on_balance_volume, force_index, money_flow_index
from ta.momentum import tsi
from ta.trend import stc
import numpy as np
import pandas as pd
import TradingStrats as TS
from Config_File import API_KEY, API_SECRET , token_telegram , chatId_telegram
from binance.client import Client
from Config_File import symbols
import Helper as help
from binance.exceptions import BinanceAPIException
import datetime 
import schedule
import requests

client = Client(api_key=API_KEY,
                api_secret=API_SECRET) 




def startProceess():
    try:
        print("start process tool every hour !!!")
        for symbol in symbols:
            processSymbol(symbol)
    except:
        print("Error start !!!")


def processSymbol(symbol):
    print("start process sysblo = "+symbol)
    start_string = "1 Jan 2022"
    massage = ""
    Date_temp, Open_temp, Close_temp, High_temp, Low_temp, Volume_temp = get_historical_new(symbol, start_string, Client.KLINE_INTERVAL_1HOUR)
    dataset = Dataset(symbol,Date_temp,Open_temp,Close_temp,High_temp,Low_temp,Volume_temp)
    message1h = Make_decision(dataset , "1h")
    if (len(message1h)) {
        message = message + "\n"+ message1h
    }

    Date_temp, Open_temp, Close_temp, High_temp, Low_temp, Volume_temp = get_historical_new(symbol, start_string, Client.KLINE_INTERVAL_2HOUR)
    dataset = Dataset(symbol,Date_temp,Open_temp,Close_temp,High_temp,Low_temp,Volume_temp)
    message2h = Make_decision(dataset , "2h")
    if (len(message2h)) {
        message = message + "\n"+ message2h
    }

    Date_temp, Open_temp, Close_temp, High_temp, Low_temp, Volume_temp = get_historical_new(symbol, start_string, Client.KLINE_INTERVAL_3HOUR)
    dataset = Dataset(symbol,Date_temp,Open_temp,Close_temp,High_temp,Low_temp,Volume_temp)
    message3h = Make_decision(dataset , "3h")
    if (len(message3h)) {
        message = message + "\n"+ message3h
    }

    Date_temp, Open_temp, Close_temp, High_temp, Low_temp, Volume_temp = get_historical_new(symbol, start_string, Client.KLINE_INTERVAL_4HOUR)
    dataset = Dataset(symbol,Date_temp,Open_temp,Close_temp,High_temp,Low_temp,Volume_temp)
    message4h = Make_decision(dataset , "4h")

    if (len(message4h)) {
        message = message + "\n"+ message4h
    }

    if(len(massage)){
        print("send messagr to user telegram !!!!")
        pusgMeassageTotele(massage)
    }
    
    
def get_historical_new(symbol , start_string , Interval):
    Open = []
    High = []
    Low = []
    Close = []
    Volume = []
    Date = []
    print("start download data sysbol :"+symbol)
    try:
        start_date = datetime.datetime.strptime(start_string, '%d %b %Y')
        today = datetime.datetime.now()
        klines = client.get_historical_klines(symbol, Interval, start_date.strftime("%d %b %Y %H:%M:%S"), today.strftime("%d %b %Y %H:00:00"), 100)
    #  ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
        for kline in klines:
            Date.append(datetime.datetime.fromtimestamp(kline[0]/1000).isoformat())
            Open.append(float(kline[1]))
            Close.append(float(kline[4]))
            High.append(float(kline[2]))
            Low.append(float(kline[3]))
            Volume.append(float(kline[5]))
        
    except BinanceAPIException as e:
        print(e)
    return Date, Open, Close, High, Low, Volume
        

def RSI(close):
    down = 0
    downcount = 0
    up = 0
    upcount = 0
    RSIval = None
    for i in range(1, len(close)):
        if close[i] - close[i - 1] < 0:
            down += abs(close[i] - close[i - 1])
            downcount += 1
        elif close[i] - close[i - 1] > 0:
            up += abs(close[i] - close[i - 1])
            upcount += 1
    if upcount != 0 and downcount != 0 and up != 0 and down != 0:
        AverageUp = up / upcount
        AverageDown = down / downcount
        RSIval = (100 - (100 / (1 + (AverageUp / AverageDown))))
    return RSIval

class Dataset: 
    def __init__(self ,symbol , Date , Open, Close, High, Low, Volume):
        self.symbol = symbol
        self.Open = Open
        self.Close = Close
        self.High = High
        self.Low = Low
        self.Volume = Volume
        self.Open_H = []
        self.Close_H = []
        self.High_H = []
        self.Low_H = []
        for i in range(len(self.Close)):
            self.Close_H.append((self.Open[i] + self.Close[i] + self.Low[i] + self.High[i]) / 4)
            if i == 0:
                self.Open_H.append((self.Close[i] + self.Open[i]) / 2)
                self.High_H.append(self.High[i])
                self.Low_H.append(self.Low[i])
            else:
                self.Open_H.append((self.Open_H[i - 1] + self.Close_H[i - 1]) / 2)
                self.High_H.append(max(self.High[i], self.Open_H[i], self.Close_H[i]))
                self.Low_H.append(min(self.Low[i], self.Open_H[i], self.Close_H[i]))
    
            
        
            
            
def Make_decision(self , Interval):
        ##Initialize vars:
        Trade_Direction = -99  ## Short (0), Long (1)
        stop_loss_val = -99  ##the margin of increase/decrease that would stop us out/ be our take profit, NOT the price target.
        take_profit_val = -99  # That is worked out later by adding or subtracting:
        curent_price = client.get_symbol_ticker(symbol=self.symbol)
        
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)
        print("current price :"+curent_price["price"])
        # datetime object containing current date and time
        ## Strategies found in TradingStrats.py:
        # print("start make decision StochRSIMACD sysbol :"+self.symbol)
        massage = ""
        Trade_Direction,stop_loss_val, take_profit_val = TS.StochRSIMACD(Trade_Direction, self.Close,self.High,self.Low)
        if(Trade_Direction == 1 or Trade_Direction == 0):
            print("Result StochRSIMACD result: {} |stop_loss_val : {} |take_profit_val: {}".format(repr(Trade_Direction),stop_loss_val,take_profit_val))
            mess = "|StochRSIMACD|{}".format(Trade_Direction)
            massage = massage + mess
        
        # print("start make decision tripleEMAStochasticRSIATR sysbol :"+self.symbol)
        Trade_Direction,stop_loss_val, take_profit_val = TS.tripleEMAStochasticRSIATR(self.Close,self.High,self.Low,Trade_Direction)
        if(Trade_Direction == 1 or Trade_Direction == 0):
            print("Result tripleEMAStochasticRSIATR result: {} |stop_loss_val : {} |take_profit_val: {}".format(repr(Trade_Direction),stop_loss_val,take_profit_val))
            mess = "|tripleEMAStochasticRSIATR|{}".format(Trade_Direction)
            massage = massage + mess
        
        # print("start make decision tripleEMA sysbol :"+self.symbol)
        Trade_Direction, stop_loss_val, take_profit_val = TS.tripleEMA(self.Close, self.High, self.Low, Trade_Direction)
        if(Trade_Direction == 1 or Trade_Direction == 0):
            print("Result tripleEMA result: {} |stop_loss_val : {} |take_profit_val: {}".format(repr(Trade_Direction),stop_loss_val,take_profit_val))
            mess = "|tripleEMA|{}".format(Trade_Direction)
            massage = massage + mess
        
        # print("start make decision breakout sysbol :"+self.symbol)
        Trade_Direction, stop_loss_val, take_profit_val = TS.breakout(Trade_Direction,self.Close,self.Volume,self.High, self.Low)
        if(Trade_Direction == 1 or Trade_Direction == 0):
            print("Result breakout result: {} |stop_loss_val : {} |take_profit_val: {}".format(repr(Trade_Direction),stop_loss_val,take_profit_val))
            mess = "|breakout|{}".format(Trade_Direction)
            massage = massage + mess
        
        # print("start make decision stochBB sysbol :"+self.symbol)
        Trade_Direction,stop_loss_val,take_profit_val = TS.stochBB(Trade_Direction,self.Close, self.High, self.Low)
        if(Trade_Direction == 1 or Trade_Direction == 0):
            print("Result stochBB result: {} |stop_loss_val : {} |take_profit_val: {}".format(repr(Trade_Direction),stop_loss_val,take_profit_val))
            mess = "|stochBB|{}".format(Trade_Direction)
            massage = massage + mess
        
        # print("start make decision goldenCross sysbol :"+self.symbol)
        Trade_Direction, stop_loss_val, take_profit_val = TS.goldenCross(Trade_Direction,self.Close, self.High, self.Low)
        if(Trade_Direction == 1 or Trade_Direction == 0):
            print("Result goldenCross result: {} |stop_loss_val : {} |take_profit_val: {}".format(repr(Trade_Direction),stop_loss_val,take_profit_val))
            mess = "|goldenCross|{}".format(Trade_Direction)
            massage = massage + mess

        # print("start make decision candle_wick sysbol :"+self.symbol)
        Trade_Direction , stop_loss_val, take_profit_val = TS.candle_wick(Trade_Direction,self.Close,self.Open,self.High,self.Low)
        if(Trade_Direction == 1 or Trade_Direction == 0):
            print("Result candle_wick result: {} |stop_loss_val : {} |take_profit_val: {}".format(repr(Trade_Direction),stop_loss_val,take_profit_val))
            mess = "|candle_wick|{}".format(Trade_Direction)
            massage = massage + mess
        
        # print("start make decision fibMACD sysbol :"+self.symbol)
        Trade_Direction,stop_loss_val,take_profit_val = TS.fibMACD(Trade_Direction, self.Close, self.Open,self.High,self.Low)
        if(Trade_Direction == 1 or Trade_Direction == 0):
            print("Result fibMACD result: {} |stop_loss_val : {} |take_profit_val: {}".format(repr(Trade_Direction),stop_loss_val,take_profit_val))
            mess = "|fibMACD|{}".format(Trade_Direction)
            massage = massage + mess
            
        
        if(len(massage)):
            massage = Interval +"|"+ dt_string + "|sysbol|{}|{}".format(self.symbol,curent_price["price"])+massage 
            print(massage)
        else :
            print("message null !!!!")
            
        

        ## need to set self.use_close_pos = True if you want to use the close position on condition functionality of the strategies below
        ##  And also need to uncomment the corresponding strategy below in check_close_pos()
        # self.use_close_pos = True
        # Trade_Direction, stop_loss_val, take_profit_val, sl = TS.heikin_ashi_ema2(self.Close, self.Open_H, self.High_H, self.Low_H, self.Close_H, Trade_Direction, stop_loss_val, take_profit_val, -99, 0)
        # print("SL heikin_ashi_ema2 {} | {} | {}".format(sl,Trade_Direction,stop_loss_val))
        #Trade_Direction,stop_loss_val,take_profit_val,_ = TS.heikin_ashi_ema(self.Close, self.Open_H, self.Close_H, Trade_Direction, stop_loss_val,take_profit_val, -99, 0)
        return message

def check_close_pos(self, current_pos):
        ## need to uncomment corresponding strategy in here too if using close position on condition functionality
        close_pos = 0
        Trade_Direction = -99  ## Short (0), Long (1)
        stop_loss_val = -99  ##the margin of increase/decrease that would stop us out/ be our take profit, NOT the price target.
        take_profit_val = -99  # That is worked out later by adding or subtracting:
        #_, _, _, close_pos = TS.heikin_ashi_ema2(self.Close, self.Open_H, self.High_H, self.Low_H, self.Close_H, Trade_Direction, stop_loss_val, take_profit_val, current_pos, 0)
        #_,_,_,close_pos = TS.heikin_ashi_ema(self.Close, self.Open_H, self.Close_H, Trade_Direction, stop_loss_val,take_profit_val, current_pos, 0)
        return close_pos


class Bot:
    def __init__(self, symbol, Open, Close, High, Low, Volume, Date, OP, CP, index, generate_heikin_ashi, tick,
                 backtesting=0):
        self.symbol = symbol
        self.Open = Open
        self.Close = Close
        self.High = High
        self.Low = Low
        self.Volume = Volume
        self.Date = Date
        self.OP = OP
        self.CP = CP
        self.index = index
        self.add_hist_complete = 0
        self.new_data = 0
        self.generate_heikin_ashi = generate_heikin_ashi
        self.Open_H = []
        self.Close_H = []
        self.High_H = []
        self.Low_H = []
        self.tick_size = tick
        self.socket_failed = False
        self.backtesting = backtesting
        self.use_close_pos = False

    def add_hist(self, Date_temp, Open_temp, Close_temp, High_temp, Low_temp, Volume_temp):
        if not self.backtesting:
            while 0 < len(self.Date):
                if self.Date[0] > Date_temp[-1]:
                    Date_temp.append(self.Date.pop(0))
                    Open_temp.append(self.Open.pop(0))
                    Close_temp.append(self.Close.pop(0))
                    High_temp.append(self.High.pop(0))
                    Low_temp.append(self.Low.pop(0))
                    Volume_temp.append(self.Volume.pop(0))
                else:
                    self.Date.pop(0)
                    self.Open.pop(0)
                    self.Close.pop(0)
                    self.High.pop(0)
                    self.Low.pop(0)
                    self.Volume.pop(0)
            self.Date = Date_temp
            self.Open = Open_temp
            self.Close = Close_temp
            self.High = High_temp
            self.Low = Low_temp
            self.Volume = Volume_temp
        if self.generate_heikin_ashi:
            ##Create Heikin Ashi bars
            for i in range(len(self.Close)):
                self.Close_H.append((self.Open[i] + self.Close[i] + self.Low[i] + self.High[i]) / 4)
                if i == 0:
                    self.Open_H.append((self.Close[i] + self.Open[i]) / 2)
                    self.High_H.append(self.High[i])
                    self.Low_H.append(self.Low[i])
                else:
                    self.Open_H.append((self.Open_H[i - 1] + self.Close_H[i - 1]) / 2)
                    self.High_H.append(max(self.High[i], self.Open_H[i], self.Close_H[i]))
                    self.Low_H.append(min(self.Low[i], self.Open_H[i], self.Close_H[i]))
        self.add_hist_complete = 1

    def handle_socket_message(self, Data, Date=0, Close=0, Volume=0, Open=0, High=0, Low=0):
        try:
            if Data == -99:
                self.Date.append(Date)
                self.Close.append(Close)
                self.Volume.append(Volume)
                self.High.append(High)
                self.Low.append(Low)
                self.Open.append(Open)
                if self.add_hist_complete:
                    self.Date.pop(0)
                    self.Close.pop(0)
                    self.Volume.pop(0)
                    self.High.pop(0)
                    self.Low.pop(0)
                    self.Open.pop(0)
                    if self.generate_heikin_ashi:
                        self.Close_H.append((self.Open[-1] + self.Close[-1] + self.Low[-1] + self.High[-1]) / 4)
                        self.Open_H.append((self.Open_H[-2] + self.Close_H[-2]) / 2)
                        self.High_H.append(max(self.High[-1], self.Open_H[-1], self.Close_H[-1]))
                        self.Low_H.append(min(self.Low[-1], self.Open_H[-1], self.Close_H[-1]))
                        self.Open_H.pop(0)
                        self.Close_H.pop(0)
                        self.Low_H.pop(0)
                        self.High_H.pop(0)
                    self.new_data = 1
            elif Data['Date'] != -99:
                self.Date.append(Data['Date'])
                self.Close.append(Data['Close'])
                self.Volume.append(Data['Volume'])
                self.High.append(Data['High'])
                self.Low.append(Data['Low'])
                self.Open.append(Data['Open'])
                if self.add_hist_complete:
                    self.Date.pop(0)
                    self.Close.pop(0)
                    self.Volume.pop(0)
                    self.High.pop(0)
                    self.Low.pop(0)
                    self.Open.pop(0)
                    if self.generate_heikin_ashi:
                        self.Close_H.append((self.Open[-1] + self.Close[-1] + self.Low[-1] + self.High[-1]) / 4)
                        self.Open_H.append((self.Open_H[-2] + self.Close_H[-2]) / 2)
                        self.High_H.append(max(self.High[-1], self.Open_H[-1], self.Close_H[-1]))
                        self.Low_H.append(min(self.Low[-1], self.Open_H[-1], self.Close_H[-1]))
                        self.Open_H.pop(0)
                        self.Close_H.pop(0)
                        self.Low_H.pop(0)
                        self.High_H.pop(0)
                    self.new_data = 1
        # except Exception as e:
        #     print(e)
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print(exc_type, fname, exc_tb.tb_lineno) ## Can add this except statement in to code to figure out what line the error was thrown on
        except Exception as e:
            print(f"Error in {self.symbol}.handle_socket_message(): ", e)
            self.socket_failed = True

def pusgMeassageTotele(message):
    print("send message to telegram "+message)
    url = "https://api.telegram.org/bot" + token_telegram + "/sendMessage"
    data = {
        "chat_id": chatId_telegram,
        "text": message
    }

    response = requests.request(
        "GET",
        url,
        params=data
    )
            
            
startProceess()
if __name__ == '__main__':
    # schedule.every(1).minute.do(testschedule)
    schedule.every(22).minutes.do(startProceess)

    while True:
        schedule.run_pending()
        time.sleep(5)

