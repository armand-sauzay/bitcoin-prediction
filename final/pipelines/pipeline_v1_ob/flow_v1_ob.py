import cbpro
import time
import pandas as pd
import json
import requests
from firebase import firebase
from datetime import date, timezone
import cbpro
import time
from datetime import datetime
import pandas as pd
import json
import websocket
import requests
from firebase import firebase

#public client instantiation



class TradeOrderBook:
    def __init__(self):
        self.public_client = cbpro.PublicClient()
        self.my_firebase = firebase.FirebaseApplication('https://test-random-305921-default-rtdb.firebaseio.com/', None) #where to load the data

    def get_order_book(self, product, time_interval, time_total):
        start = time.time()

        #order_book = []
        #get a list with all jsons
        time.sleep(time_interval)
        while (time.time() - start) < time_total:
            #OB
            ##ob to json all 
            msg_ob = self.public_client.get_product_order_book(product)
            msg_ob['time']=datetime.now()
            #order_book.append(msg_ob)
            ## ob to firebase
            
            today = datetime.now(timezone.utc).date()
            post_string='/order_book_v1_'+str(today)
            firebase_log_ob = self.my_firebase.post(post_string, msg_ob)
            print(firebase_log_ob)
            print(msg_ob)

            #T
            ##trades to json all 
            #msg_trade = self.public_client.get_product_ticker(product_id=product)
            #trades.append(msg_trade)
            time.sleep(time_interval)

            ##trades to firebase
            #firebase_log_trades = self.my_firebase.post('/trades', msg_trade)
            #print(firebase_log_trades)

        return order_book

if __name__=="__main__":
    order_book_obj = TradeOrderBook()
    order_book = order_book_obj.get_order_book('BTC-USD', 2, 2592000) #1 month
    print('order book rest api accessed')

