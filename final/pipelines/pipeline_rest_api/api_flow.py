import cbpro
import time
from datetime import datetime
import pandas as pd
import json
import websocket
import requests
from firebase import firebase

class TradeOrderBook:
    def __init__(self):
        self.public_client = cbpro.PublicClient()
        self.my_firebase = firebase.FirebaseApplication('https://test-random-305921-default-rtdb.firebaseio.com/', None) #where to load the data

    def get_trades_and_order_book(self, product, time_interval, time_total):

        start = time.time()
        trades = []
        order_book = []
        #get a list with all jsons
        time.sleep(time_interval)
        while (time.time() - start) < time_total:
            #OB
            ##ob to json all 
            msg_ob = self.public_client.get_product_order_book(product)
            msg_ob['time']=datetime.now()
            #order_book.append(msg_ob)
            ## ob to firebase
            firebase_log_ob = self.my_firebase.post('/order_book', msg_ob)
            print(firebase_log_ob)

            #T
            ##trades to json all 
            msg_trade = self.public_client.get_product_ticker(product_id=product)
            #trades.append(msg_trade)
            time.sleep(time_interval)

            ##trades to firebase
            firebase_log_trades = self.my_firebase.post('/trades', msg_trade)
            print(firebase_log_trades)

        #return trades, order_book

if __name__=="__main__":
    trade_order_book = TradeOrderBook()
    trades, order_book = trade_order_book.get_trades_and_order_book('BTC-USD', 2, 2592000) #1 month