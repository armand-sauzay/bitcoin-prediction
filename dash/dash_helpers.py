from firebase import firebase
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

my_firebase = firebase.FirebaseApplication('https://test-random-305921-default-rtdb.firebaseio.com/', None)
trades=my_firebase.get('/websocket_trades_v1_2021-03-13', '')
df=pd.DataFrame(trades).T.reset_index(drop=True)

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

fig = ohlc_viz(ohlc_transformation(df, column='price', time_period='Min'))

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
