import numpy as np
import pandas as pd
import datetime
import yfinance as yf
import pandas_datareader.data as web
import requests
#from datetime import datetime, timedelta
import os
import sys

import os
import sys


# ... continue with your script ...

def extract_features():

    return_period = 5
    
    START_DATE = (datetime.date.today() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    END_DATE = datetime.date.today().strftime("%Y-%m-%d")
    stk_tickers = ['MSFT', 'IBM', 'GOOGL']
    ccy_tickers = ['DEXJPUS', 'DEXUSUK']
    idx_tickers = ['SP500', 'DJIA', 'VIXCLS']
    
    stk_data = yf.download(stk_tickers, start=START_DATE, end=END_DATE, auto_adjust=False)
    #stk_data = web.DataReader(stk_tickers, 'yahoo')
    ccy_data = web.DataReader(ccy_tickers, 'fred', start=START_DATE, end=END_DATE)
    idx_data = web.DataReader(idx_tickers, 'fred', start=START_DATE, end=END_DATE)

    Y = np.log(stk_data.loc[:, ('Adj Close', 'MSFT')]).diff(return_period).shift(-return_period)
    Y.name = Y.name[-1]+'_Future'
    
    X1 = np.log(stk_data.loc[:, ('Adj Close', ('GOOGL', 'IBM'))]).diff(return_period)
    X1.columns = X1.columns.droplevel()
    X2 = np.log(ccy_data).diff(return_period)
    X3 = np.log(idx_data).diff(return_period)

    X = pd.concat([X1, X2, X3], axis=1)
    
    dataset = pd.concat([Y, X], axis=1).dropna().iloc[::return_period, :]
    Y = dataset.loc[:, Y.name]
    X = dataset.loc[:, X.columns]
    dataset.index.name = 'Date'
    #dataset.to_csv(r"./test_data.csv")
    features = dataset.sort_index()
    features = features.reset_index(drop=True)
    features = features.iloc[:,1:]
    return features


### Check original file for what was deleted

import requests
import pandas as pd

def get_bitcoin_historical_prices(days=60):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}

    r = requests.get(url, params=params, timeout=20)

    # If the HTTP call failed, raise a clear error
    if r.status_code != 200:
        raise RuntimeError(f"CoinGecko error {r.status_code}: {r.text[:300]}")

    data = r.json()

    # If the JSON isn't the expected format, raise a clear error
    if "prices" not in data:
        raise RuntimeError(f"Unexpected CoinGecko response keys: {list(data.keys())}. "
                           f"Response sample: {str(data)[:300]}")

    df = pd.DataFrame(data["prices"], columns=["Timestamp", "Price_USD"])
    df["Date"] = pd.to_datetime(df["Timestamp"], unit="ms").dt.normalize()
    df = df.drop(columns=["Timestamp"]).set_index("Date")
    return df

