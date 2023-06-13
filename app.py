# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import json
import websocket
import time as t
RANGE=100000000

app = Dash(__name__)
server=app.server
websocket.enableTrace(True)
ws = websocket.WebSocket()
ws.connect("wss://i7kggwivc5.execute-api.us-west-2.amazonaws.com/production")

df_Inspiration_Flow = pd.DataFrame(columns=["Units","Inspiration_Flow"])
n=0
a=[]
counter=0

while True:
    
    try:    
        message = ws.recv()
        data = json.loads(message)

        if n<=160:
            if counter<9:
                a.append(data)
                print(a)
                counter=counter+1

            elif counter==9:
                counter = 0
                a.append(data)
                for i in range(10):    
                    df_Inspiration_Flow = df_Inspiration_Flow.append({"Units":n+i, "Inspiration_Flow": a[i]}, ignore_index=True)
                    fig = px.area(df_Inspiration_Flow,x="Units",y="Inspiration_Flow")
                     # Update the plot with the new data
                    app.layout = html.Div(children=[
    html.H1(children='Dorion Application'),
    html.Div(children='''
        A web application to display the ventilator data.
    '''),dcc.Graph(
        figure=fig.update_traces(line_color='orange').update_layout(yaxis_range=[0,120])
    )])
                a.clear()
                print("cleared the a")
                n=n+10
                if __name__ == '__main__':
                    app.run_server(debug=True)                
            elif n>160: 
                n=1 
            else:
                print("Data not received")
    except websocket.WebSocketConnectionClosedException:
        break
