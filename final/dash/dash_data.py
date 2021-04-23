import random
from collections import deque
from apscheduler.schedulers.blocking import BlockingScheduler
import pickle
from datetime import datetime 
from datetime import timedelta,date, timezone
from firebase import firebase
import cbpro
import time

import requests


import cbpro
import time

import pandas as pd
import dash

'''my_firebase = firebase.FirebaseApplication('https://test-random-305921-default-rtdb.firebaseio.com/', None)
trades=my_firebase.get('/websocket_trades_v1_2021-03-13', '')
df=pd.DataFrame(trades).T.reset_index(drop=True)

df=pd.read_csv('data_03_13_dash.csv')
df.time=pd.to_datetime(df.time)
df["price"] = df.price.astype(float)
df["last_size"] = df['last_size'].astype(float)
df["best_bid"] = df['best_bid'].astype(float)
df["best_ask"] = df['best_ask'].astype(float)


def ohlc_transformation(df, column, time_period):
    temp = df.resample(rule=time_period, on='time')[column].ohlc()
    return temp

def ohlc_viz(df_ohlc):
    #figure plot
    fig = go.Figure(data=[go.Candlestick(x=df_ohlc.index,
                open=df_ohlc.open,
                high=df_ohlc.high,
                low=df_ohlc.low,
                close=df_ohlc.close)])
    
    fig.show()
    return(fig)
'''

class websocket_trades(cbpro.WebsocketClient):
    def on_open(self):
        print("-- wassup --")
        self.url = "wss://ws-feed.pro.coinbase.com/"
        #self.firebase= firebase.FirebaseApplication(
        self.products = ["BTC-USD"]
        self.message_count = 0
        self.channels=['ticker']
        self.prices=deque(maxlen=1000)
        self.times=deque(maxlen=1000)
        self.sides=deque(maxlen=10)
        self.all=deque(maxlen=10)

    def on_message(self, msg):
        #print(msg)
        #print(type(msg))
        

        if msg['type']=='ticker':
            self.prices.append(msg['price'])
            self.sides.append(msg['side'])
            self.times.append(
                datetime.strptime(msg['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                )
            self.all.append(msg)
          #self.message_count += 1
          #today = datetime.now(timezone.utc).date()
          #postt_string='/websocket_trades_v1_'+str(t
          #self.firebase.post(postt_string, msg)
          
        #print(msg)
          
         


trades = websocket_trades()
trades.start()
# set time interval variable for apsceduler module
number_seconds = 3
'''
# create lists with deque as sentdex showed
X = deque(maxlen=1000)
X.append(df['time'][0])
Y = deque(maxlen=1000)
Y.append(df["price"][0])
i = deque(maxlen=1000)
i.append(1)

# make tuple of lists for storing in pickle file
data_X_Y = (X, Y)
print(data_X_Y)'''

# store tuple in pickle
#pickle.dump(data_X_Y, open("data_X_Y.p", "wb"))

# function for getting data within Dash callback
'''def get_data():
    # initiate blockingscheduler
    sched = BlockingScheduler()
    # decorater in which you define the number of seconds see https://www.youtube.com/watch?v=FsAPt_9Bf3U&t=1s for good explanation decorators
    @sched.scheduled_job('interval', seconds=number_seconds, start_date=datetime.now() - timedelta(seconds=(number_seconds - 1)))
    def update_data_4_graph():
        # these are the lines of codes that were in the function of the callback of Sentdex
        X=trades.times
        Y=trades.prices

        #i.append(i[-1]+1)
        #X.append(df["time"][i[-1]*1000])
        #Y.append(df["price"][i[-1]*1000])

        # again make a tuple of lists and store the tuples in the a pickle file
        data_X_Y = (X, Y)
        print(data_X_Y)
        pickle.dump(data_X_Y, open("data_X_Y.p", "wb"))

    # start the apscheduler module
    sched.start()'''

def get_data():
    sched = BlockingScheduler()
    @sched.scheduled_job('interval', seconds=number_seconds, start_date=datetime.now() - timedelta(seconds=(number_seconds - 1)))
    def update_data_4_graph():
    # these are the lines of codes that were in the function of the callback of Sentdex
        times=trades.times
        prices=trades.prices
        sides=trades.sides
        alls=trades.all

        data_times_prices = (times, prices)
        data_sides = sides
        data_all = alls
        #print(data_X_Y)
        pickle.dump(data_times_prices, open("data_times_prices.p", "wb"))
        pickle.dump(data_sides, open("data_sides.p", "wb"))
        pickle.dump(data_all, open("data_all.p", "wb"))

    sched.start()