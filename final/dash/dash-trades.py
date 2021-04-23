import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import pickle
import threading as Threading

from dash_data import get_data

# Create a thread for "getting data" in these python files the data is actually created instead of retrieved,
# from somewhere else but i call the function get_data because in real life you want to probably get data from
# a sensor, csv file, sql table or whatever. This is the moment where the old code could get you into trouble...
# Btw for a tutorial about threading see https://www.youtube.com/watch?v=IEEhzQoKtQU&t=493s
t1 = Threading.Thread(target=get_data)
t1.start()

def count(dq, item):
    return sum(elem == item for elem in dq)

def tfi(dall):
    tfi=0
    for el in dall:
        if el['side']=='buy':
            tfi+=float(el['last_size'])
        else:
            tfi-=float(el['last_size'])
    #res=sum(elem == item for elem in dq)
    return(tfi)

# Unchanged dash app layout
app = dash.Dash(__name__)
app.layout = html.Div(
    [   
        html.H1('Live prices '),
        dcc.Graph(id='graph-trades', animate=True),
        dcc.Interval(
            id='graph-trades-update',
            interval=1*3000
        ),

        html.H1('Last 10 sides'),
        html.H2('a buy indicates an uptick (taker side)'),
        dcc.Graph(id='graph-sides', animate=True),
        dcc.Interval(
            id='graph-sides-update',
            interval=1*3000
),
        
    ]
)

# New adjusted callback
@app.callback(Output('graph-trades', 'figure'),
              [Input('graph-trades-update', 'n_intervals')])
def update_graph_trades(input_data):
    # get the data from a pickle file
    data_times_prices = pickle.load(open("data_times_prices.p", "rb"))
    #print(data_times_prices)
    X = data_times_prices[0]
    Y = data_times_prices[1]
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[float(min(Y)),(max(Y)),]))}

@app.callback(Output('graph-sides', 'figure'),
              [Input('graph-sides-update', 'n_intervals')])
def update_graph_sides(input_data):
    # get the data from a pickle file
    data_sides = pickle.load(open("data_sides.p", "rb"))
    data_all = pickle.load(open("data_all.p", "rb"))
    value_buys=count(data_sides, 'buy')
    value_sells=count(data_sides, 'sell')
    value_tfi=tfi(data_all)
    
    fig =go.Figure() 

    fig.add_trace(go.Indicator(
                    mode = "gauge+number+delta",
                    value = value_buys,
                    #domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "# of buys"},
                    delta = {'reference': 5},
                    gauge = {'axis': {'range': [0, 10]}},
                    domain = {'row': 0, 'column': 0})
                    )

    fig.add_trace(go.Indicator(
                mode = "gauge+number+delta",
                value = value_sells,
                #domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "# of sells"},
                delta = {'reference': 5},
                gauge = {'axis': {'range': [0, 10]}},
                domain = {'row': 0, 'column': 1})
                )
    
    fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = value_tfi,
            #domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "TFI"},
            delta = {'reference': 5},
            #gauge = {'axis': {'range': [0, 10]}},
            domain = {'row': 1, 'column': 0})
            )
    fig.update_layout(
        grid = {'rows': 2, 'columns': 2, 'pattern': "independent"})
        #template = {'data' : {'indicator': [{
        #'title': {'text': "Speed"},
        #'mode' : "number+delta+gauge",
        #'delta' : {'reference': 90}}]
        #                 
    return fig
       
       
     
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080 ,debug=True)



