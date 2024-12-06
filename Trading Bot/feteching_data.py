import ccxt
import pandas as pd 
from pyti.simple_moving_average import simple_moving_average
import numpy
import time
import logging

logging.basicConfig(filename="Trading Bot",filemode="w")

pd.set_option("display.max_rows",1000) # if u want to see the hole data frame u can use it 
symbol = "ETH/USD"

exchange = ccxt.binance()
def fetching_ohlcv_data ():
    try:
        ohlcv = exchange.fetch_ohlcv(symbol,timeframe="15m",limit=500)
        logging.info("Feteched Data sussecfully")

        close_values = [ohlcv[i][4] for i in range(len(ohlcv))]
        return close_values 
    except:
        logging.error("Error fetching the data")
        print("error")
def sma (data):
    try:
        shoeter_sma = simple_moving_average(data,50)
        longer_sma = simple_moving_average (data,200)
        logging.info("SMA featched")
    except Exception as e:
        logging.critical(f"cant get SMA {e}")
        return None
    
    sma_value = pd.DataFrame({
        "Close_Value" : data ,
        "shoeter_sma" : shoeter_sma,
        "longer_sma"  : longer_sma         
              })
    sma_value.to_string(index=False)


    sma_value["Signal"] = numpy.where(sma_value["shoeter_sma"] > sma_value["longer_sma"],"✅","❌") 

    buy_locater = sma_value["Signal"].tail(1).to_string(index=False)
    price_locater = sma_value["Close_Value"].tail(1).to_string(index=False)


    print(f"Price: {price_locater}  buy_signal : {str(buy_locater)}")



def main():
    while True:
        data = fetching_ohlcv_data()
        time.sleep(10) # for testing it is 10 but try to do 15 mins accoding to your time frame  
        # set it to 900 
        sma(data)

main()

