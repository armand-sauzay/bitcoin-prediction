import cbpro
import time
import pandas as pd
from websocket import create_connection
import json
import websocket
import requests
from firebase import firebase

class websocket_trades(cbpro.WebsocketClient):
    def on_open(self):
        print("-- wassup --")
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.firebase= firebase.FirebaseApplication('https://test-random-305921-default-rtdb.firebaseio.com/', None)
        self.products = ["BTC-USD"]
        self.message_count = 0
        self.channels=['matches']
        self.all=[]

    def on_message(self, msg):
        print(msg)
        self.all+=[msg]
        if msg['type']=='match':
          self.message_count += 1
          self.firebase.post('/websocket_trades', msg)


    def on_close(self):
        print("-- c u --")


wsClient = websocket_trades()
wsClient.start()