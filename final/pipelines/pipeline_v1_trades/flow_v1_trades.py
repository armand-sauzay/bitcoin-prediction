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


class websocket_trades(cbpro.WebsocketClient):
    def on_open(self):
        print("-- wassup --")
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.firebase= firebase.FirebaseApplication('https://test-random-305921-default-rtdb.firebaseio.com/', None)
        self.products = ["BTC-USD"]
        self.message_count = 0
        self.channels=['ticker']
        #self.all=[]

    def on_message(self, msg):
        print(msg)
        #self.all+=[msg]
        
        if msg['type']=='ticker':
          #self.message_count += 1
          today = datetime.now(timezone.utc).date()
          postt_string='/websocket_trades_v1_'+str(today)
          self.firebase.post(postt_string, msg)


    def on_close(self):
        print("-- c u --")

if __name__=="__main__":
    #get trades
    wsClientTrades = websocket_trades()
    wsClientTrades.start()
    print('ws trades started')

