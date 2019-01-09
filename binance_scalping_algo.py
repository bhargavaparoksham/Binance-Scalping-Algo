#Author: Bhargav
#Binance Scalping Algo
#Note: This code doesn't include live trading functions, only for backtesting.

from binance.client import Client
from binance.helpers import date_to_milliseconds
import json
import datetime
import sys
import time
from calendar import monthrange


#api_key = 'Your_Key'
#api_secret = 'Your_Secret'

global present_candle_open
global present_candle_high
global present_candle_low
global present_candle_type
global present_candle_height


global buy_price
global sell_price

global hour_count

global symbol
#symbol = "BTCUSDT"

global year
global month
global day
global hour
global minute
global second

global price_monitor_status
global time_monitor_status
global profit_loss_status

global profit_percent
global loss_percent


global backtest_data 

global asset_size 
global order_status
global total_profit
global order_count
global trade_count

global prev_candle_open
global prev_candle_high
global prev_candle_low
global prev_candle_close
global prev_candle_vol
global prev_candle_type
global prev_candle_height
global prev_candle_body_height
global prev_candle_uppr_stm_ht
global prev_candle_lowr_stm_ht

global prev_candle_half_price

global buy_price
global sell_price

global order_type
global entry_price   #price at which an asset is last bought
global exit_price    #price at which an asset is last sold
global minute_count

global begin

total_profit = 0.00

asset_size = 2000
trade_count = 0


#client = Client(api_key, api_secret)


global prev_candle


def prev_candle():

    global minute_count
    global prev_candle_open
    global prev_candle_high
    global prev_candle_low
    global prev_candle_close
    global prev_candle_type
    global prev_candle_height
    global prev_candle_body_height
    global prev_candle_uppr_stm_ht
    global prev_candle_lowr_stm_ht
    global prev_candle_half_price
    global begin


    temp_var = 1
    minute_count = minute_count - 60
    if begin == 0:
        minute_count = minute_count + 60
        begin = 1

    while temp_var <=60:

        if temp_var == 1:
            prev_candle_open = round(float(backtest_data[minute_count+1][1]), 2)
            prev_candle_high = round(float(backtest_data[minute_count+1][2]), 2)
            prev_candle_low = round(float(backtest_data[minute_count+1][3]), 2)

        h = round(float(backtest_data[minute_count+1][2]), 2)
        if prev_candle_high < h:
            prev_candle_high = h

        l = low = round(float(backtest_data[minute_count+1][3]), 2)
        if prev_candle_low > l:
            prev_candle_low = l

        if temp_var == 60:
            prev_candle_close = round(float(backtest_data[minute_count+1][4]), 2)

        temp_var += 1
        minute_count += 1

    prev_candle_height = abs(prev_candle_high - prev_candle_low)
    prev_candle_body_height = abs(prev_candle_open - prev_candle_close)

    if (prev_candle_open <= prev_candle_close):
        prev_candle_type = 'GREEN'
        prev_candle_uppr_stm_ht = prev_candle_high - prev_candle_close
        prev_candle_lowr_stm_ht = prev_candle_open - prev_candle_low

        #bearish green candle

        if (prev_candle_uppr_stm_ht >= (prev_candle_body_height + prev_candle_lowr_stm_ht)):
            prev_candle_half_price = prev_candle_close - ((prev_candle_close - prev_candle_low)*0.8)

        #bullish green candle

        if (prev_candle_uppr_stm_ht < (prev_candle_body_height + prev_candle_lowr_stm_ht)):
            prev_candle_half_price = prev_candle_close - ((prev_candle_close - prev_candle_low)*0.45)

        #bullish green candle with price movement greater than 3 percent

        temp = prev_candle_height/prev_candle_low
        if temp > 0.03:
            prev_candle_half_price = prev_candle_close - ((prev_candle_close - prev_candle_low)*0.2)

        

    if (prev_candle_open > prev_candle_close):
        prev_candle_type = 'RED'
        prev_candle_uppr_stm_ht = prev_candle_high - prev_candle_open
        prev_candle_lowr_stm_ht = prev_candle_close - prev_candle_low

        #bearish Red candle

        if (prev_candle_lowr_stm_ht <= (prev_candle_body_height + prev_candle_uppr_stm_ht)):
            prev_candle_half_price = prev_candle_open - ((prev_candle_open - prev_candle_low)*0.8)

        #bullish Red candle

        if (prev_candle_lowr_stm_ht > (prev_candle_body_height + prev_candle_uppr_stm_ht)):
            prev_candle_half_price = prev_candle_open - ((prev_candle_open - prev_candle_low)*0.45)
 


    '''print(prev_candle_open)
    print(prev_candle_high)
    print(prev_candle_low)
    print(prev_candle_close)
    print(prev_candle_vol)'''


global present_candle


def present_candle():

    global present_candle_open
    global present_candle_high
    global present_candle_low
    global present_candle_type
    global present_candle_height

    temp = int((minute_count)/60)
    candle_begin = (temp*60) + 1


    i = candle_begin
    present_candle_high = round(float(backtest_data[candle_begin+1][2]), 2)
    while i<=minute_count:
        t = round(float(backtest_data[i+1][2]), 2)
        if present_candle_high<t:
            present_candle_high = t
        i+=1

    i = candle_begin
    present_candle_low = round(float(backtest_data[candle_begin+1][3]), 2)
    while i<=minute_count:
        t = round(float(backtest_data[i+1][3]), 2)
        if present_candle_low>t:
            present_candle_low = t
        i+=1
    

    present_candle_open = prev_candle_close
    present_candle_close = current_price
    
    

    if (present_candle_open <= present_candle_close):
        present_candle_type = 'GREEN'

    if (present_candle_open > present_candle_close):
        present_candle_type = 'RED'

    present_candle_height = abs(present_candle_high - present_candle_low)



global current_datetime

def current_datetime():
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = now.hour
    minute = now.minute
    second = now.second




global asset_price

def asset_price(bridge):

    global current_price

    if bridge == 0:
        if (order_type == 'BUY') and (order_status != 'BUY'):
            stop_limit_buy(buy_price)
        if (order_type == 'SELL') and (order_status != 'SELL'):
            stop_limit_sell(sell_price)

    current_price = round(float(backtest_data[minute_count+1][4]), 2)

        
    

    # print(current_price)


global stop_limit_buy

def stop_limit_buy(val):

    global order_status
    global total_profit
    global order_type
    global entry_price   #price at which an asset is last bought
    global buy_price
    global hour_count
    global minute_count

    buy_price = val
    asset_price(1)
    if current_price>=buy_price:
        order_status = 'BUY'         #order_status gives what type of transaction happened last - BUY or SELL
        entry_price = round(buy_price, 2)
        order_type = 'NILL'          #order_type gives you the type of order in the orderbook
        print(hour_count, end=" ")
        print(minute_count, end=" ")
        print('En P: ', entry_price, end=" ")
        total_profit -= 1

global stop_limit_sell

def stop_limit_sell(val):

    global order_status
    global total_profit
    global order_type
    global exit_price    #price at which an asset is last sold
    global sell_price
    global order_count
    global trade_count

    sell_price = val
    asset_price(1)
    if current_price<=sell_price:
        order_status = 'SELL'
        exit_price = round(sell_price, 2)
        order_type = 'NILL'
        order_count = 1
        print('Ex P: ', exit_price, end=" ")
        trade_count += 1
        if entry_price<=exit_price:
            profit = round((((exit_price-entry_price)/entry_price)*asset_size), 2)
            print('P: ', profit, end=" ")
            total_profit = round((total_profit + profit), 2)
            print('T P: ', total_profit)

        if entry_price>exit_price:
            loss = round((((entry_price-exit_price)/entry_price)*asset_size), 2)
            print('L: ', loss, end=" ")
            total_profit = round((total_profit - loss), 2)
            print('T P: ', total_profit)


global order_cancel

def order_cancel():

    global order_type
    order_type = 'NILL'


global price_monitor

def price_monitor():
    # price monitor triggers when price reaches different points relative to prev_candle
    # keeping in mind the asset order status (sold, not sold, partially sold, where it is sold etc)

    global price_monitor_status
    global time_monitor_status
    global profit_loss_status

    global profit_percent
    global loss_percent
    global order_type
    global minute_count
    global order_count
    
    total_minutes = 1
    prev_candle()
    '''print('Candle open: ',prev_candle_open, end=" ")
    print('Candle high: ', prev_candle_high, end=" ")'''
    

    while total_minutes<=60:

        asset_price(0)
        present_candle()
        change = 0

        if total_minutes == 1:
            time_monitor_status = 'START'
            change += 1

        if total_minutes > 1:
            time_monitor_status = 'START2'
            change += 1

        #IMPORTANT NOTE: The order in which the below 4 if's are arranged is important
        
        if current_price < prev_candle_half_price:
            price_monitor_status = 'CANDLE_HALF'
            change += 1

        if current_price < prev_candle_low:
            price_monitor_status = 'CANDLE_LOW'
            change += 1

        if (prev_candle_type == 'RED') and (current_price > prev_candle_open):
            price_monitor_status = 'CANDLE_RED_OPEN'
            change += 1

        if current_price > prev_candle_high:
            price_monitor_status = 'CANDLE_HIGH'
            change += 1

        '''if total_minutes == 30:
            print('Open: ', present_candle_open, end=" ")
            print('High: ', present_candle_high)'''

        if total_minutes > 30:
            time_monitor_status = 'MIDDLE'
            change += 1
        
        if total_minutes > 45:
            time_monitor_status = 'END'
            change += 1

        if  (order_status == 'BUY') and (current_price < entry_price):
            profit_loss_status = 'LOSS'
            loss_percent = (entry_price - current_price)/entry_price
            change += 1

        if  (order_status == 'BUY') and (current_price >= entry_price):
            profit_loss_status = 'PROFIT'
            #profit percent is position of current price relative to present candle high
            if (present_candle_high == present_candle_low):       #throw exception
                profit_percent = 0.99
            if(present_candle_high != present_candle_low):
                profit_percent = (current_price - present_candle_low)/(present_candle_high - present_candle_low)
            change += 1

        if change > 0:
            asset_manager()
        
        if total_minutes == 60:
            if (order_status == 'BUY') and (order_type == 'NILL'):
                stop_limit_sell(current_price)
                order_type = 'SELL'
            if (order_type == 'BUY') or (order_type == 'SELL'):
                order_cancel()
            order_count = 0

        total_minutes += 1
        minute_count += 1

           


global asset_manager

def asset_manager():
    # manages the purchases & sales of the assest, based on price monitor inputs, prev_candle_type & time
    global order_type

    if (time_monitor_status == 'START') and (order_type == 'NILL'):
        if prev_candle_type == 'GREEN':
            t = prev_candle_high - 0*prev_candle_uppr_stm_ht
            stop_limit_buy(t)
            order_type = 'BUY'

        if prev_candle_type == 'RED':
            t = prev_candle_open - 0.2*prev_candle_body_height
            stop_limit_buy(t)
            order_type = 'BUY'

    if (price_monitor_status == 'CANDLE_HALF') and (order_status != 'BUY') and (order_count == 0):     #error when red - prev_candle_close
        if prev_candle_type == 'GREEN':
            order_cancel()
            stop_limit_buy(prev_candle_close - 0*prev_candle_body_height)
            order_type = 'BUY'

        if prev_candle_type == 'RED':
            order_cancel()
            stop_limit_buy(prev_candle_open)
            order_type = 'BUY'

    '''if (price_monitor_status == 'CANDLE_LOW') and (order_status == 'NO'):
        order_cancel()
        stop_limit_buy(prev_candle_half_price)'''
        
    
    if (profit_loss_status == 'PROFIT') and (order_status == 'BUY'):
        if time_monitor_status == 'END':
            if profit_percent < 0.9:
                stop_limit_sell(current_price)
                order_type = 'SELL'

        if (time_monitor_status == 'MIDDLE'):
            if profit_percent < 0.4:               #default: 0.38
                stop_limit_sell(current_price)
                order_type = 'SELL'
                

    if (profit_loss_status == 'LOSS') and (order_status == 'BUY'):
        if loss_percent > 0.0023:       #default: 0.005
            stop_limit_sell(current_price)
            order_type = 'SELL'



backtest_data = json.load(open('Binance_BTCUSDT_1m_2018_3_20-2018_4_20.json'))

minute_count = 1
hour_count = 1
order_status = 'NILL'
order_type = 'NILL'
profit_loss_status = 'NILL'
price_monitor_status = 'NILL'
order_count = 0
begin = 0

while hour_count <= 672:

    price_monitor()
    #print(minute_count)
    hour_count += 1
    #time.sleep(0.5)
    #if hour_count == 15:
        #print('Trade count: ', trade_count)
        #sys.exit(0)
