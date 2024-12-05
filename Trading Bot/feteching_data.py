import ccxt
import pandas as pd 
from pyti.simple_moving_average import simple_moving_average
import numpy
import time 
pd.set_option("display.max_rows",1000) # if u want to see the hole data frame u can use it 

exchange = ccxt.binance()
def fetching_ohlcv_data ():
    try:
        symbol = "BTC/USDT"
        ohlcv = exchange.fetch_ohlcv(symbol,timeframe="15m",limit=500)

        close_values = [ohlcv[i][4] for i in range(len(ohlcv))]
        ohlcv_df = pd.DataFrame(close_values)

        # print(ohlcv_df)
        return close_values 
    except:
        # Exception as 
        print("error fetching the data")
def sma (data):
    try:
        shoeter_sma = simple_moving_average(data,50)
        longer_sma = simple_moving_average (data,200)
    except:
        print("error getting the SMA")
    

    sma_value = pd.DataFrame({
        "Close_Value" : data ,
        "shoeter_sma" : shoeter_sma,
        "longer_sma"  : longer_sma         
              })
    sma_value.to_string(index=False)


    sma_value["Signal"] = numpy.where(sma_value["shoeter_sma"] > sma_value["longer_sma"],"buy","sell") 
    buy_locater = sma_value["Signal"].tail(1)
    price_locater = sma_value["Close_Value"].tail(1)
    print(price_locater)
    print(f" buy_signal : {str(buy_locater)}{sma_value.to_string(index=False)}")



def main():
    data = fetching_ohlcv_data()
    while True:
        time.sleep(10)
        sma(data)

main()


